import streamlit as st
import google.generativeai as genai

# 1. Page Config
st.set_page_config(page_title="Square Pulse AI", page_icon="⏹️")
st.title("Square Pulse: AI Merchant Strategy Tool")

# 2. Sidebar for API Key
st.sidebar.header("System Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # UPDATED TO THE 2026 CUTTING EDGE MODEL FROM YOUR LIST
        model = genai.GenerativeModel('gemini-3-flash-preview')
        st.sidebar.success("Gemini 3 Connected!")
    except Exception as e:
        st.sidebar.error(f"Setup Error: {e}")

# 3. PM UI
st.info("💡 Analyzing seller sentiment and growth opportunities using Gemini 3 Flash.")
user_input = st.text_area("Seller Feedback / Reviews:", height=200, 
                         placeholder="Paste reviews here...")

if st.button("Generate Roadmap Strategy"):
    if not api_key:
        st.error("Please provide an API Key.")
    elif not user_input:
        st.warning("Please provide feedback data.")
    else:
        try:
            with st.spinner("Gemini 3 is processing high-dimensional data..."):
                prompt = f"""
                You are a Square APM. Analyze this seller data: {user_input}
                
                Provide:
                1. Sentiment Health (1-10)
                2. Operational Friction Points
                3. A 'Next-Gen' AI feature Square should build to solve these problems.
                """
                response = model.generate_content(prompt)
                st.markdown("### 🚀 Strategic AI Insights")
                st.write(response.text)
        except Exception as e:
            st.error(f"Execution Error: {e}")
