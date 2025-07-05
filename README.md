# 📬 AI-Powered Email Reply Generator using IBM Granite 13B Instruct

This project is a Streamlit-based web application that generates professional, friendly, or concise replies to emails using IBM's `granite-13b-instruct-v2` foundation model. It demonstrates the practical use of generative AI in communication automation with secure API integration.

---

## 🚀 Features

- ✅ Generate email replies in 3 tones: **Formal**, **Friendly**, and **Concise**
- ✅ Uses **IBM watsonx.ai Granite 13B Instruct v2** for high-quality generation
- ✅ IAM Token-based secure authentication with IBM Cloud
- ✅ Streamlit interface for easy interaction
- ✅ Sidebar test for API connectivity
- ✅ Example email demonstration

---

## 🧠 Model Used

- **Name**: `ibm/granite-13b-instruct-v2`
- **Type**: Instruction-following LLM
- **Host**: IBM Watsonx.ai
- **Region**: EU-DE (Frankfurt)

---

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/) – UI framework  
- [IBM Watsonx.ai](https://www.ibm.com/products/watsonx) – Foundation model hosting  
- Python 3.10  
- `requests` – For API integration

---

## 🔐 Prerequisites

- An [IBM Cloud account](https://cloud.ibm.com/registration)
- Enable [watsonx.ai service](https://dataplatform.cloud.ibm.com/)
- IAM API Key
- Project ID (from your Watsonx project)

---

## 📦 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/email-reply-generator.git
   cd email-reply-generator
