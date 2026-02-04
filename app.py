import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import json

# 1. SQUARE BRANDING & CONFIG
st.set_page_config(page_title="Square Pulse", page_icon="⏹️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f7f7f7; }
    .stButton>button { background-color: #000000; color: white; border-radius: 8px; font-weight: bold; }
    .insight-card { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR CONFIG
st.sidebar.title("⏹️ Square Pulse")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.info("Don't have a key? Click 'Run Demo Mode' on the right.")

# 3. UI LAYOUT
st.title("Merchant Feedback Intelligence")
st.caption("AI-Native Product Management Prototype for Square")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### 📥 Input Feedback")
    user_input = st.text_area("Paste customer reviews:", height=250, 
                             placeholder="The checkout is slow...\nI love the new layout!",
                             value="The Square reader is incredibly fast, but I wish the mobile app had better inventory tracking for my bakery. Sometimes it crashes when I upload photos.")
    
    # We give buttons unique keys to avoid the 'DuplicateElementId' error
    gen_btn = st.button("Generate from API", key="api_gen")
    demo_btn = st.button("🚀 Run Demo Mode", key="demo_gen")

# 4. DATA PROCESSING LOGIC
data = None

if demo_btn:
    # Simulated AI response for the recruiter
    data = {
        "sentiment_score": 82,
        "sentiment_history": [65, 72, 88, 79, 82],
        "feature_recommendation": "AI-Powered Inventory Photo Sync: A feature to optimize image compression for mobile uploads, preventing app crashes during inventory updates.",
        "summary": "Merchants are happy with hardware speed but facing friction in mobile inventory management."
    }
    st.sidebar.success("Displaying Demo Data")

elif gen_btn:
    if not api_key:
        st.error("Please enter an API Key in the sidebar or use Demo Mode.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3-flash-preview')
            with st.spinner("AI is analyzing..."):
                prompt = f"Analyze these reviews: {user_input}. Return ONLY JSON with: sentiment_score(int), sentiment_history(list of 5 ints), feature_recommendation(str), summary(str)."
                response = model.generate_content(prompt)
                # Clean up the response text to ensure it is only JSON
                clean_json = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(clean_json)
        except Exception as e:
            st.error(f"Error: {e}")

# 5. DASHBOARD VISUALIZATION
if data:
    with col2:
        st.markdown("### 📊 Merchant Health Overview")
        
        # Metrics
        m1, m2 = st.columns(2)
        m1.metric("Sentiment Score", f"{data['sentiment_score']}%", "+3%")
        m2.metric("Data Status", "Analyzed", "AI-Active")

        # Chart
        df = pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu", "Fri"], "Sentiment": data['sentiment_history']})
        fig = px.area(df, x="Day", y="Sentiment", title="Weekly Sentiment Trend")
        fig.update_traces(line_color='#00d44a') # Square Green
        st.plotly_chart(fig, use_container_width=True)

        # Insight Card
        st.markdown(f"""
        <div class="insight-card">
            <h4>🤖 AI Product Recommendation</h4>
            <p>{data['feature_recommendation']}</p>
            <hr>
            <p><strong>Executive Summary:</strong> {data['summary']}</p>
        </div>
        """, unsafe_allow_html=True)
