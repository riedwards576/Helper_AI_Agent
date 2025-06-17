import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.join(abs_working_directory, file_path)

    #print("Absolute WorkingDir:",abs_workingDirectory)
    #print("Absolute File Path:", abs_filePath)

    #2.If the file_path is outside of working_directory, return a string with error:
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    
    #3.If the file_path doesn't exist, create it. If there are errors, return a string representing the error, prefixed with "Error:".
    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(abs_file_path)
        except Exception as e:
            return f"Error: {e}"
    
    else:
        with open(abs_file_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to or overwrite a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to the content will be written into.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written into the specified file.",
            ),
        },
    ),
)