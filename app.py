import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Square Pulse AI", page_icon="⏹️")
st.title("Square Pulse: AI Merchant Strategy Tool")

# Sidebar
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # We'll use the most standard model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.success("API Connected")
    except Exception as e:
        st.sidebar.error(f"Config Error: {e}")

# Main UI
user_input = st.text_area("Seller Feedback:", "The Square reader is great, but the app crashes sometimes.")

if st.button("Analyze"):
    if not api_key:
        st.error("Please enter an API Key.")
    else:
        try:
            # The prompt
            response = model.generate_content(user_input)
            st.write(response.text)
        except Exception as e:
            st.error(f"Detailed Error: {e}")
            
            # DEBUGGING SECTION: This helps us see what models YOU have access to
            st.write("---")
            st.write("Checking available models for your API Key...")
            try:
                available_models = [m.name for m in genai.list_models()]
                st.write("Your accessible models:", available_models)
            except:
                st.write("Could not list models. Is the API Key correct?"): Double-check that your API Key is from 'Google AI Studio' and not 'Google Cloud Console'.")
