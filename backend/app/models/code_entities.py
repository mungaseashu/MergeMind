from pydantic import BaseModel
from typing import List, Optional, Literal

class CodeEntity(BaseModel):
    id: str

class DirectoryModel(CodeEntity):
    repository_id: str
    path: str
    name: str

class FileModel(CodeEntity):
    repository_id: str
    path: str
    name: str
    extension: str
    language: str
    size_bytes: int
    line_count: int
    hash: str
    last_modified: float

class ClassModel(CodeEntity):
    name: str
    file_id: str
    start_line: int
    end_line: int
    docstring: Optional[str] = None
    inherits: List[str] = []

class FunctionModel(CodeEntity):
    name: str
    file_id: str
    class_id: Optional[str] = None
    start_line: int
    end_line: int
    docstring: Optional[str] = None
    is_async: bool = False

class EndpointModel(CodeEntity):
    method: str
    path: str
    file_id: str
    function_id: str
    framework: str = "fastapi"

class ImportModel(BaseModel):
    file_id: str
    module: str
    name: Optional[str] = None
    line: int

class CallModel(BaseModel):
    function_id: str
    called_name: str
    line: int

class PullRequestModel(CodeEntity):
    pr_number: int
    title: str
    author: str
    status: Literal["OPEN", "MERGED", "CLOSED"] = "OPEN"
    base_branch: str
    head_branch: str
    repository_id: str
    github_url: str
    created_at: int  # unix timestamp in ms

class PullRequestFileModel(BaseModel):
    """Represents a single file changed in a Pull Request."""
    filename: str
    status: Literal["added", "modified", "removed", "renamed"]
    pr_id: str
    file_id: str  # The corresponding File node id in Neo4j (if it exists)

