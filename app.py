import streamlit as st
import google.generativeai as genai

# 1. Page Setup
st.set_page_config(page_title="Square Pulse AI", page_icon="⏹️")
st.title("Square Pulse: AI Merchant Strategy Tool")

# 2. Sidebar for API Key
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 3. Logic to initialize the model
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Using 'gemini-1.5-flash' - the most reliable free-tier model
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.success("API Key Connected!")
    except Exception as e:
        st.sidebar.error(f"Setup Error: {e}")

# 4. User Interface
user_input = st.text_area("Paste Seller Reviews here:", height=200, 
                         placeholder="Example: The checkout process is slow...")

if st.button("Generate Strategy"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    elif not user_input:
        st.warning("Please enter some feedback text.")
    else:
        try:
            with st.spinner("AI is thinking..."):
                # Professional PM Prompt
                prompt = f"""
                You are a Square Product Manager. Analyze these reviews:
                {user_input}
                
                Provide:
                1. Sentiment Score (1-10)
                2. Key Seller Pain Points
                3. One AI-driven feature suggestion for Square.
                """
                
                response = model.generate_content(prompt)
                st.markdown("### Analysis Results")
                st.write(response.text)
                
        except Exception as e:
            # This will show the REAL error on your screen instead of crashing
            st.error(f"AI Error: {e}")
            st.info("💡 Tip: Double-check that your API Key is from 'Google AI Studio' and not 'Google Cloud Console'.")
