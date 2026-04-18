#!/usr/bin/env python3

import os
from fastmcp import FastMCP

(TRANSPORT, PORT) = ("http", 3000)

# Initialize the MCP with a descriptive name
mcp = FastMCP("file-lister-mcp")
  
@mcp.tool
def list_files(directory_path: str) -> list[str]:
    """
    Lists all files and subdirectories within the specified directory path.
    Returns a list of strings, where each string is an item found in the path.
    """
    
    # Check if the path exists and is a directory
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(
            f"Error: The path '{directory_path}' is not a valid directory or does not exist."
        )
    
    try:
        # os.listdir() returns a list of names of the entries in the directory
        file_list = os.listdir(directory_path)
        return file_list
    except Exception as e:
        # Catch other potential errors (e.g., permission denied)
        raise Exception(f"An unexpected error occurred while listing files: {e}")
  
if __name__ == "__main__":
    # When running the script, start the MCP server
    print("Starting File Lister MCP on http://0.0.0.0:%d" % PORT)
    mcp.run(transport=TRANSPORT, host="0.0.0.0", port=PORT)
