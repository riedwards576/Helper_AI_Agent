import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from call_function import call_function, available_functions

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

Where possible, use bullet points and concise language when constructing final responses.
"""

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    MAX_ITERATIONS = 20

    for step in range(MAX_ITERATIONS):
        if verbose:
            print(f"\n--- Iteration {step + 1} ---")

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        # Log tokens
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        # Append all candidate content responses to the conversation
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        # If no function call, print final response and exit loop
        if not response.function_calls:
            print("\n Final LLM response:")
            print(response.text)
            break

        # Process function calls and append results to messages
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)

            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("Empty function call result")

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response['result']}")

            messages.append(function_call_result)  # Append function response to conversation

    else:
        # Reached max iterations without resolving
        print("\n Max iterations reached without completion.")



if __name__ == "__main__":
    main()