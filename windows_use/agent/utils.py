from langchain_core.messages import BaseMessage,HumanMessage
from windows_use.agent.views import AgentData, Action
import ast
import re

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def extract_agent_data(message: BaseMessage) -> AgentData:
    text = message.content
    # Dictionary to store extracted values
    result = {}
    # Extract Memory
    memory_match = re.search(r"<memory>(.*?)<\/memory>", text, re.DOTALL)
    if memory_match:
        result['memory'] = memory_match.group(1).strip()
    # Extract Evaluate
    evaluate_match = re.search(r"<evaluate>(.*?)<\/evaluate>", text, re.DOTALL)
    if evaluate_match:
        result['evaluate'] = evaluate_match.group(1).strip()
    # Extract Thought
    thought_match = re.search(r"<thought>(.*?)<\/thought>", text, re.DOTALL)
    if thought_match:
        result['thought'] = thought_match.group(1).strip()
    # Extract Action-Name
    action_name_match = re.search(r"<action_name>(.*?)<\/action_name>", text, re.DOTALL)
    if action_name_match:
        # If action_name is found, initialize the action dict
        if 'action' not in result:
            result['action'] = {}
        result['action']['name'] = action_name_match.group(1).strip()
    # Extract and convert Action-Input to a dictionary
    action_input_match = re.search(r"<action_input>(.*?)<\/action_input>", text, re.DOTALL)
    if action_input_match:
        if 'action' not in result:
            result['action'] = {}
        action_input_str = action_input_match.group(1).strip()

        # --- FIX: Handle 'null' string explicitly ---
        if action_input_str == "null":
            result['action']['params'] = None
        elif not action_input_str:
            result['action']['params'] = {}
        else:
            try:
                result['action']['params'] = ast.literal_eval(action_input_str)
            except (ValueError, SyntaxError):
                result['action']['params'] = action_input_str

    # If no action was found at all, set it to None before validating
    if 'action' not in result:
        result['action'] = None

    return AgentData.model_validate(result)

def image_message(prompt,image)->HumanMessage:
    return HumanMessage(content=[
        {
            "type": "text",
            "text": prompt,
        },
        {
            "type": "image_url",
            "image_url": image
        },
    ])
