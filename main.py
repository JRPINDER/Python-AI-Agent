import os
import argparse
import json

from prompts import system_prompt

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.write_file import schema_write_file, write_file
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file

from dotenv import load_dotenv
from openai import OpenAI

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("no API key found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    available_functions = [
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file
    ]
    
    response = client.chat.completions.create(
        model = "openrouter/free",
        temperature = 0,
        messages = messages,
        tools=available_functions
    )

    if not response.usage:
        raise RuntimeError("no response usage found")

    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")

    if args.verbose:
        print(f"User prompt: {messages[0]["content"]}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print(f"Response: \n{response.choices[0].message.content}")



if __name__ == "__main__":
    main()
