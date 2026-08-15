import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieves the content of a specified file relative to the working directory, with a maximum character limit",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to file relative to the working directory",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, filepath: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, filepath))
        valid_target_file = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

        if not valid_target_file:
            return f"Error: Cannot read \"{filepath}\" as it is outside the permitted working directory"

        if not os.path.isfile(target_path):
            return f"Error: File not found or is not a regular file: \"{filepath}\""

        with open(target_path, "r") as f:
            file_string = f.read(MAX_CHARS)
            if not f.read(1) == "":
                file_string += f'[...File "{filepath}" truncated at {MAX_CHARS} characters]'

    except Exception as e:
        return f"Error: {e}"

    return file_string  
    
