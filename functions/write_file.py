import os 

def writefile(working_directory: str, filepath: str, content: str) -> str:
    try:
            working_dir_abs = os.path.abspath(working_directory)
            target_path = os.path.normpath(os.path.join(working_dir_abs, filepath))
            valid_target_file = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

            if not valid_target_file:
                        return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"

            if os.path.isdir(target_path):
                        return f"Error: Cannot write to \"{file_path}\" as is a directory"

            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            with open(target_path, "w") as f:
                        f.write(content)

            return f"Successfully wrote to \"{filepath}\" ({len(content)} characters written)"

    except Exception as e:
            return f"Error: writing to file: {e}"