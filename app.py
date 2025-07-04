import streamlit as st
import requests
import json


API_KEY = "zPhBdlG1nNh_bvWS3pMBzEfsA09FNJbeqprI3HHLsjj1"
PROJECT_ID = "2c0ccefb-ce25-4fa9-816b-af1ef05cba09"
REGION = "eu-de"  # Frankfurt region


st.set_page_config(
    page_title="AI Email Reply Generator",
    page_icon="✉️",
    layout="centered"
)


st.title("📬 AI-Powered Email Reply Generator")
st.markdown("Generate professional, friendly, or concise replies using IBM Granite 13B Instruct model.")

tone = st.selectbox("✒️ Select reply tone:", ("Formal", "Friendly", "Concise"))

email_text = st.text_area(
    "📩 Paste the incoming email below:",
    height=200,
    placeholder="Hi there, I wanted to check if you're available for a quick call tomorrow..."
)

# IBM Token Fetch
@st.cache_resource
def get_iam_token():
    try:
        url = "https://iam.cloud.ibm.com/identity/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            st.error(f"Failed to get token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting token: {str(e)}")
        return None

# Format prompt for Granite 13B Instruct 
def format_granite_instruct_prompt(email_content, tone):
    """
    Format prompt specifically for IBM Granite 13B Instruct model
    """
    tone_instructions = {
        "Formal": "Write a professional and formal email reply. Use business language, maintain a respectful tone, and include appropriate greetings and closings.",
        "Friendly": "Write a warm and friendly email reply. Use a conversational tone while remaining professional and approachable.",
        "Concise": "Write a brief and to-the-point email reply. Keep it short but polite, professional, and include all necessary information."
    }
    
    prompt = f"""Instruction: You are a professional email assistant. {tone_instructions[tone]}

Original email to reply to:
{email_content}

Task: Write an appropriate email reply that addresses the content of the original email.

Email Reply:"""
    
    return prompt


def clean_response(response):
    """Clean up the generated response"""
    response = response.strip()
    
    # Remove instruction echoes if present
    if "Instruction:" in response:
        parts = response.split("Email Reply:")
        if len(parts) > 1:
            response = parts[-1].strip()
    
    # Remove other common artifacts
    lines = response.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not any(skip in line.lower() for skip in [
            "original email to reply to:",
            "task:",
            "instruction:",
            "email reply:"
        ]):
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def generate_reply_granite(email_content, tone):
    token = get_iam_token()
    if not token:
        return "Error: Could not obtain authentication token"
    
    url = f"https://{REGION}.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    

    formatted_prompt = format_granite_instruct_prompt(email_content, tone)
    
    payload = {
        "model_id": "ibm/granite-13b-instruct-v2",
        "input": formatted_prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "temperature": 0.1,  # Low temperature for focused responses
            "top_p": 1.0,
            "top_k": 50,
            "stop_sequences": ["Instruction:", "Original email:", "Task:", "\n\n\n"]
        },
        "project_id": PROJECT_ID
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # Debug information
        st.write(f"🔍 Model: ibm/granite-13b-instruct-v2")
        st.write(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            json_response = response.json()
            
            if "results" in json_response and len(json_response["results"]) > 0:
                raw_response = json_response["results"][0]["generated_text"]
                cleaned_response = clean_response(raw_response)
                return cleaned_response
            else:
                st.json(json_response)
                return "Error: No results in response"
        else:
            json_response = response.json()
            st.json(json_response)
            return f"Error: {json_response.get('message', 'Unknown error')}"
            
    except Exception as e:
        st.error(f"Exception occurred: {str(e)}")
        return f"Error: {str(e)}"

# ---- Test connection ----
def test_connection():
    """Test if the API connection works"""
    token = get_iam_token()
    if token:
        st.success("✅ Successfully obtained authentication token")
        return True
    else:
        st.error("❌ Failed to get authentication token")
        return False

# Main App
st.sidebar.header("🔧 Connection Test")
if st.sidebar.button("Test API Connection"):
    test_connection()

st.sidebar.header("📋 Model Info")
st.sidebar.info("""
**Model**: IBM Granite 13B Instruct v2
**Best for**: Following instructions, structured tasks
**Region**: EU-DE (Frankfurt)
""")


if st.button("✨ Generate Reply"):
    if email_text.strip() == "":
        st.warning("Please enter an email to generate a reply.")
    else:
        with st.spinner("Generating reply using IBM Granite 13B Instruct..."):
            try:
                result = generate_reply_granite(email_text.strip(), tone)
                
                if not result.startswith("Error:"):
                    st.success("✅ Here is your AI-generated reply:")
                    st.text_area("✉️ Generated Reply", value=result, height=150, key="reply_output")
                    
                    # Copy-friendly format
                    st.markdown("### 📋 Copy-friendly format:")
                    st.code(result, language="text")
                    
                else:
                    st.error(result)
                    
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")


st.markdown("---")
st.subheader("💡 Example Usage")

example_email = """Hi John,

I hope you're doing well. I wanted to follow up on our meeting last week about the project timeline. Could you please send me the updated schedule when you have a chance? 

Also, let me know if you need any additional resources from my team to meet the deadline.

Best regards,
Sarah"""

if st.button("Try Example Email"):
    st.text_area("Example Email", value=example_email, height=120, key="example_email")
    
    with st.spinner("Generating example reply..."):
        result = generate_reply_granite(example_email, "Formal")
        if not result.startswith("Error:"):
            st.success("Example Reply Generated:")
            st.text_area("Example Reply", value=result, height=120, key="example_reply")

