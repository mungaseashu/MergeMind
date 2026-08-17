import os
import hashlib
from typing import List, Dict, Any
from pathlib import Path

DEFAULT_IGNORE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    "dist", "build", "coverage", ".cache", ".idea", ".vscode"
}

def calculate_file_hash(filepath: str) -> str:
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return ""

class RepositoryScanner:
    def __init__(self, repo_path: str, ignore_dirs: set = None):
        self.repo_path = Path(repo_path).resolve()
        self.ignore_dirs = ignore_dirs or DEFAULT_IGNORE_DIRS

    def scan(self) -> Dict[str, Any]:
        """
        Scans the repository and returns a dictionary of directories and files.
        """
        directories = []
        files = []

        for root, dirs, filenames in os.walk(self.repo_path):
            # Modify dirs in-place to ignore specified directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            rel_root = Path(root).relative_to(self.repo_path)
            if str(rel_root) != ".":
                directories.append({
                    "path": str(rel_root).replace("\\", "/"),
                    "name": rel_root.name
                })

            for filename in filenames:
                file_path = Path(root) / filename
                rel_path = file_path.relative_to(self.repo_path)
                
                # Basic metadata
                try:
                    stats = file_path.stat()
                    size_bytes = stats.st_size
                    last_modified = stats.st_mtime
                except Exception:
                    size_bytes = 0
                    last_modified = 0

                # Detect language (simplified)
                extension = file_path.suffix.lower()
                language = "unknown"
                if extension == ".py":
                    language = "python"
                elif extension in [".js", ".jsx"]:
                    language = "javascript"
                elif extension in [".ts", ".tsx"]:
                    language = "typescript"

                file_info = {
                    "path": str(rel_path).replace("\\", "/"),
                    "name": filename,
                    "extension": extension,
                    "language": language,
                    "size_bytes": size_bytes,
                    "last_modified": last_modified,
                    "absolute_path": str(file_path)
                }
                files.append(file_info)

        return {
            "directories": directories,
            "files": files
        }

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    scanner = RepositoryScanner(path)
    result = scanner.scan()
    print(f"Found {len(result['directories'])} dirs and {len(result['files'])} files.")
