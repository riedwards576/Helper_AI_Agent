import os
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_workingDirectory = os.path.abspath(working_directory)
    abs_filePath = os.path.join(abs_workingDirectory, file_path)

    #print("Absolute WorkingDir:",abs_workingDirectory)
    #print("Absolute File Path:", abs_filePath)

    if not abs_filePath.startswith(abs_workingDirectory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
    elif not os.path.isfile(abs_filePath):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000
    try:
        with open(abs_filePath, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        
    except Exception as e:
        return f"Error reading file: {e}"
    
    #character count & truncation
    if os.path.getsize(abs_filePath) > MAX_CHARS:
        return f"{file_content_string}\n[...File {abs_filePath} truncated at 10000 characters]"
    
    return f"{file_content_string}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to read the content from.",
            ),
        },
    ),
)