import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
	abs_workingDirectory = os.path.abspath(working_directory)
	
	abs_filePath = os.path.join(abs_workingDirectory, file_path)
	abs_filePath = os.path.realpath(abs_filePath)
	
	real_working_directory = os.path.realpath(abs_workingDirectory)

	#2. If the file_path is outside working directory, return a string with an error:
	if not abs_filePath.startswith(real_working_directory):
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

	#3. If the file_path doesn't exist, return an error string:
	if not os.path.exists(abs_filePath):
		return f'Error: File "{file_path}" not found.'
    
	#4. If the file doesn't end with ".py", return an error string:
	if not file_path.endswith(".py"):
		return f'Error: "{file_path}" is not a Python file.'
	
	try:
		result = subprocess.run(['python3', abs_filePath], timeout=30, capture_output=True, cwd=real_working_directory)

		# Format single-string output
		if result.stdout == "" and result.stderr == "":
			return "No output produced."

		output = []

		if result.stdout != "":
			stdout = result.stdout.decode('utf-8')
			output.append(f"STDOUT: {stdout}")

		if result.stderr != "":
			stderr = result.stderr.decode('utf-8')
			output.append(f"STDERR: {stderr}")

		output.append(f"Process exited with code {result.returncode}")

		return '\n'.join(output)

	except Exception as e:
		return f"Error: executing Python file: {e}"
	

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to be executed.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments passed from the user prompt into the executable file.",
            ),
        },
    ),
)