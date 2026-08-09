import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"

        if not os.path.isdir(target_dir):
            return f"Error: \"{directory}\" is not a directory"

        directory_list = os.listdir(target_dir)
        return_string = ""

        for file in directory_list:
            try:
                name = file 
                is_dir = os.path.isdir(os.path.join(target_dir, file))
                size = os.path.getsize(os.path.join(target_dir, file))
                return_string += f"{name}: file_size={size}bytes, is_dir={is_dir}\n"
            except Exception as e:
                return f"Error: {e}"

        return return_string

    except Exception as e:
        return f"Error: {e}"
