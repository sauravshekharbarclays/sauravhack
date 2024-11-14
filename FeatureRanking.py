import requests
import json

# Configuration
API_KEY = "00019e9b4c9d4176803380030dbeb562"

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

customer_id = 371759785
interaction_file_path = "data/user_interaction_data.json"
properties_file_path = "data/user_properties_data.json"

def load_customer_data(customer_id, interaction_file_path, properties_file_path):
    # Load user interaction data
    with open(interaction_file_path, 'r') as f:
        interaction_data = json.load(f)

    # Load user properties data
    with open(properties_file_path, 'r') as f:
        properties_data = json.load(f)
    return interaction_data, properties_data


def query_model_for_customer_rank(customer_id, interaction_file, properties_file):
    interaction_data, properties_data = load_customer_data(customer_id, interaction_file, properties_file)
    
    # Payload for the request
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI agent. Based on the following customer data, predict the features that user with customer ID {customer_id} is likely to be interested in:" 
                        + "\n" + "\n"
                        + "Interaction History:" + "\n" +  json.dumps(interaction_data, indent=2)
                        + "\n" + "\n"
                        + "Customer Details:" + "\n" +  json.dumps(properties_data, indent=2)
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Provide the output as JSON array which element having'feature name' and 'feature rank', where 1 is the most likely feature to be used by the user id in request"
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    ENDPOINT = "https://genai-openai-fincrafters.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

    # Send request
    try:
      response = requests.post(ENDPOINT, headers=headers, json=payload)
      response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
      raise SystemExit(f"Failed to make the request. Error: {e}")
    # Handle the response as needed (e.g., print or process)
    aiResponse = response.json()['choices'][0]['message']['content']
    print(aiResponse)
    save_to_json(response.json(), 'feature_rank_output_' + str(customer_id) + '.json')
    return aiResponse

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


query_model_for_customer_rank(customer_id=371759785, interaction_file=interaction_file_path,properties_file=properties_file_path)
