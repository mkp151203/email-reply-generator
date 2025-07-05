import requests

# Step 1: Get IAM token using IBM Cloud API Key
def get_iam_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}"
    
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

# Step 2: Format the instruction-based prompt
def build_prompt(email_text, tone):
    instructions = {
        "Formal": "Write a formal, professional reply.",
        "Friendly": "Write a friendly and warm reply.",
        "Concise": "Write a brief, to-the-point reply."
    }
    return f"""Instruction: You are an assistant. {instructions[tone]}

Original Email:
{email_text}

Reply:"""

# Step 3: Call the IBM Granite 13B Instruct model
def generate_reply(email_text, tone, token, project_id):
    url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "model_id": "ibm/granite-13b-instruct-v2",
        "input": build_prompt(email_text, tone),
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "temperature": 0.1
        },
        "project_id": project_id
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["results"][0]["generated_text"]
