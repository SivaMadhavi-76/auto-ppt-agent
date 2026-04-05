from fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("filesystem-server")

BASE_DIR = Path("workspace")
BASE_DIR.mkdir(exist_ok=True)


@mcp.tool()
def write_file(filename: str, content: str) -> str:
    """
    Write content to a file inside the workspace folder.

    Args:
        filename: Name of the file to create.
        content: Text content to write into the file.

    Returns:
        Path of the saved file.
    """
    file_path = BASE_DIR / filename
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


@mcp.tool()
def read_file(filename: str) -> str:
    """
    Read content from a file inside the workspace folder.

    Args:
        filename: Name of the file to read.

    Returns:
        File content as text.
    """
    file_path = BASE_DIR / filename
    return file_path.read_text(encoding="utf-8")


@mcp.tool()
def list_files() -> list[str]:
    """
    List all files inside the workspace folder.

    Returns:
        List of file names.
    """
    return [p.name for p in BASE_DIR.iterdir() if p.is_file()]