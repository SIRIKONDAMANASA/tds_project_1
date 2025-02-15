# /// script
# dependencies = [
#   "fastapi",
#   "requests",
#   "python-dotenv",
#   "uvicorn",
#   "python-dotenv",
#   "beautifulsoup4",
#   "markdown",
#   "requests<3",
#   "duckdb",
#   "numpy",
#   "python-dateutil",
#   "docstring-parser",
#   "httpx",
#   "scikit-learn",
#   "pydantic",
# ]
# ///
import traceback
import json
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
import os
import logging
from typing import Dict, Callable
from tasks import (
    beautify_code_file,
    transform_function_to_schema,
    interact_with_gpt,
    process_image_with_gpt,
    execute_db_operation,
    process_text_with_ai,
    compute_text_embeddings,
    extract_image_data,
    build_content_index,
    parse_log_files,
    sort_json_content,
    analyze_text_patterns,
    deploy_script_package,
    handle_git_ops,
    scrape_web_content,
    convert_md_format,
    fetch_api_content,
    filter_csv_content,
    convert_audio_text,
    resize_image_file,
    execute_sql_operation,
    verify_path_location
)


load_dotenv()
API_KEY = os.getenv("AIPROXY_TOKEN")
URL_CHAT = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
URL_EMBEDDING = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"
app = FastAPI()

RUNNING_IN_CODESPACES = "CODESPACES" in os.environ
RUNNING_IN_DOCKER = os.path.exists("/.dockerenv")
logging.basicConfig(level=logging.INFO)

def ensure_local_path(path: str) -> str:
    return verify_path_location(path)

function_mappings: Dict[str, Callable] = {
    "deploy_script_package": deploy_script_package,
    "beautify_code_file": beautify_code_file,
    "execute_db_operation": execute_db_operation,
    "process_text_with_ai": process_text_with_ai,
    "compute_text_embeddings": compute_text_embeddings,
    "extract_image_data": extract_image_data,
    "build_content_index": build_content_index,
    "parse_log_files": parse_log_files,
    "sort_json_content": sort_json_content,
    "analyze_text_patterns": analyze_text_patterns,
    "handle_git_ops": handle_git_ops,
    "scrape_web_content": scrape_web_content,
    "convert_md_format": convert_md_format,
}

def parse_task_description(task_description: str, tools: list):
    response = requests.post(
        URL_CHAT,
        headers={"Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{
                        'role': 'system',
                        'content':"You are intelligent agent that understands and parses tasks. You quickly identify the best tool functions to use to give the desired results"
                            },
                            {
                            "role": "user",
                            "content": task_description
                            }],
                            "tools": tools,
                            "tool_choice":"required",
                }
    )
    logging.info("TASK PARSING COMPLETED" * 3)
    print(response.json())
    logging.info("PARSER RESPONSE RECEIVED" * 3)
    return response.json()["choices"][0]["message"]


def execute_function_call(function_call):
    logging.info(f"Inside execute_function_call with function_call: {function_call}")
    try:
        function_name = function_call["name"]
        function_args = json.loads(function_call["arguments"])
        function_to_call = function_mappings.get(function_name)
        logging.info("PRINTING RESPONSE:::"*3)
        print('Calling function:', function_name)
        print('Arguments:', function_args)
        logging.info("PRINTING RESPONSE:::"*3)
        if function_to_call:
            function_to_call(**function_args)
        else:
            raise ValueError(f"Function {function_name} not found")
    except Exception as e:
        error_details = traceback.format_exc()
        raise HTTPException(status_code=500, 
                            detail=f"Error executing function in execute_function_call: {str(e)}",
                            headers={"X-Traceback": error_details}
                            )


@app.post("/run")
async def run_task(task: str = Query(..., description="Plain-English task description")):
    tools = [transform_function_to_schema(func) for func in function_mappings.values()]
    logging.info(len(tools))
    logging.info(f"Inside run_task with task: {task}")
    try:
        # Ensure no function description exceeds 1024 characters
        # for tool in tools:
        #        if len(tool['function']['description']) > 1024:
        #              tool['function']['description'] = tool['function']['description'][:1021] + "..."  # Indicate truncation

        function_call_response_message = parse_task_description(task,tools) #returns  message from response
        if function_call_response_message["tool_calls"]:
            for tool in function_call_response_message["tool_calls"]:
                execute_function_call(tool["function"])
        return {"status": "success", "message": "Task executed successfully"}
    except Exception as e:
        error_details = traceback.format_exc()
        raise HTTPException(status_code=500, 
                            detail=f"Error executing function in run_task: {str(e)}",
                            headers={"X-Traceback": error_details}
                            )

@app.get("/read",response_class=PlainTextResponse)
async def read_file(path: str = Query(..., description="Path to the file to read")):
    logging.info(f"Inside read_file with path: {path}")
    output_file_path = ensure_local_path(path)
    if not os.path.exists(output_file_path):
        raise HTTPException(status_code=500, detail=f"Error executing function in read_file (GET API")
    with open(output_file_path, "r") as file:
        content = file.read()
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
