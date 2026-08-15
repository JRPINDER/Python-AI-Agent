import os 
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file in the specified directory with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to file relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional list of arguments to pass to the Python file",
                }
            },
        },
    },
}

def run_python_file(working_directory: str, filepath: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, filepath))
        valid_target_file = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

        if not valid_target_file:
            return f"Error: Cannot execute \"{filepath}\" as it is outside the permitted working directory"

        if not os.path.isfile(target_path):
            return f"Error: \"{filepath}\" does not exist or is not a regular file"

        if filepath[-3:] != ".py":
            return f"Error: \"{filepath}\" is not a Python file"

        command = ["python", target_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command, 
            timeout = 30, 
            cwd = working_dir_abs,
            capture_output = True,
            text = True
        )

        if result.returncode != 0:
            return f"Error: process exited with code {result.returncode}"

        if not (result.stdout or result.stderr):
            return "No output produced"

        return f"STDOUT:{result.stdout}\nSTDERR:{result.stderr}"      

    except Exception as e:
        return f"Error: executing python file: {e}"