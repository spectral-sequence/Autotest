# openai_integration.py
import openai

def query_openai_assistant(assistant_id, data, openai_api_key):
    openai.api_key = openai_api_key
    prompt = f"Analyze the data {data} and provide suggestions."
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        user=assistant_id
    )
    return response.choices[0].text.strip()