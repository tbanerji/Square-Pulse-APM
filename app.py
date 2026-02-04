import streamlit as st
import google.generativeai as genai

# 1. Page Config
st.set_page_config(page_title="Square Pulse AI", page_icon="⏹️", layout="wide")

st.title("⏹️ Square Pulse: AI Merchant Strategy Tool")
st.markdown("### Turning customer feedback into economic empowerment.")

# 2. API Setup
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
# 3. User Input
col1, col2 = st.columns([1, 1])

with col1:
    st.info("💡 **PM Tip:** Paste raw customer reviews or feedback below. This tool simulates how a Square APM uses AI to prioritize product features.")
    user_input = st.text_area("Paste Seller Reviews:", height=300, 
                             placeholder="Example: The POS system crashed during lunch rush. / I love how easy the invoices are!")

# 4. Processing Logic
if st.button("Generate Portfolio-Ready Insights"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar to run the analysis.")
    elif not user_input:
        st.warning("Please provide some feedback data first.")
    else:
        with st.spinner("Analyzing data through a Product Manager lens..."):
            # The prompt is key for an APM role—it shows you understand business value.
            prompt = f"""
            You are a Product Manager at Square. Analyze these merchant reviews:
            "{user_input}"
            
            Provide the following structured report:
            1. **Sentiment Health**: (A quick status: Critical, Stable, or Excellent)
            2. **Feature Requests**: What specific tools are sellers asking for?
            3. **Operational Friction**: Where is the merchant losing money or time?
            4. **Proposed Roadmap Item**: Suggest one high-impact AI feature Square could build to solve these issues.
            
            Format with professional bold headers and bullet points.
            """
            
            response = model.generate_content(prompt)
            
            with col2:
                st.success("Analysis Complete")
                st.markdown(response.text)

# 5. Footer for the Hiring Manager
st.markdown("---")
st.caption("Built for the Square APM 2026 Application | Focus: AI-Native Product Development")
