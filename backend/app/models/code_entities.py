from pydantic import BaseModel
from typing import List, Optional

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
