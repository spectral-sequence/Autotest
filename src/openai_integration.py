import openai
import os
import xml.etree.ElementTree as ET

def query_openai_assistant(prompt: str, assistant_id: str) -> str:
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.organization = os.getenv("OPENAI_ORG")
        openai.api_key = openai_api_key

        response = openai.Completion.create(
            model=assistant_id,
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip() if response.choices else "No response generated."
    except openai.error.OpenAIError as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Failed to connect to OpenAI API."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred during the API request."

def parse_xml_config(file_path: str):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        description = root.find('description').text.strip()
        objective = root.find('instructions/objective').text.strip()
        priorities = [p.text.strip() for p in root.findall('instructions/key_priorities/priority')]
        return {
            "description": description,
            "objective": objective,
            "priorities": priorities
        }
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return None

def create_custom_prompt(base_prompt: str, xml_config: dict) -> str:
    if xml_config:
        return f"{xml_config['description']} {xml_config['objective']} {base_prompt}"
    return base_prompt

def query_with_custom_prompt(file_path: str, base_prompt: str, assistant_id: str) -> str:
    xml_config = parse_xml_config(file_path)
    custom_prompt = create_custom_prompt(base_prompt, xml_config)
    return query_openai_assistant(custom_prompt, assistant_id)

# Example usage
xml_file_path = "config/cr-agent-xml-assistant-v0.2.xml"
base_prompt = "Please provide a detailed explanation."
assistant_id = "text-davinci-003"

response = query_with_custom_prompt(xml_file_path, base_prompt, assistant_id)
print(response)
