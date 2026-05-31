import streamlit as st
import os
from huggingface_hub import InferenceClient #preinstalled native wrapper
# 1. Pull the classic 'Write' token out of your secret settings 
HF_TOKEN = os.getenv("HF_TOKEN") 
# 2. Fire up the native client using the token 
client = InferenceClient(token=HF_TOKEN)
st.title("🎤 AI Debate Partner")
topic = st.text_input("Enter your opinion")
if st.button("Send"): 
    if not topic.strip(): 
        st.warning("Please enter a question.") 
    elif not HF_TOKEN: 
        st.error("Your HF_TOKEN secret key is entirely missing from Settings!")
    else:
        with st.spinner("Processing natively through the cluster..."): 
            try:
                # 3. Route via internal endpoints rather than requests.post 
                response = client.chat.completions.create( model="meta-llama/Llama-3.2-1B-Instruct", messages=[{"role": "user", "content": f"""
                Argue against this statement:
                {topic}
                """}], max_tokens=50 ) 
                # 5. Extract output clean string text safely 
                answer = response.choices[0].message.content 
                st.success(answer) 
            except Exception as e: 
                # This explicitly unpacks server messages instead of dropping HTML text 
                st.error(f"System Response: {e}")
