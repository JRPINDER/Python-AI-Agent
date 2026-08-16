import os 

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Directory path to file relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                }
            },
        },
    },
}

def write_file(working_directory: str, filepath: str, content: str) -> str:
    try:
            working_dir_abs = os.path.abspath(working_directory)
            target_path = os.path.normpath(os.path.join(working_dir_abs, filepath))
            valid_target_file = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

            if not valid_target_file:
                        return f"Error: Cannot write to \"{filepath}\" as it is outside the permitted working directory"

            if os.path.isdir(target_path):
                        return f"Error: Cannot write to \"{filepath}\" as is a directory"

            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            with open(target_path, "w") as f:
                        f.write(content)

            return f"Successfully wrote to \"{filepath}\" ({len(content)} characters written)"

    except Exception as e:
            return f"Error: writing to file: {e}"