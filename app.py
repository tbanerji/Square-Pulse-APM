import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import json

# 1. SQUARE BRANDING (CSS)
st.set_page_config(page_title="Square Pulse", page_icon="⏹️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f7f7f7; }
    .stButton>button { background-color: #000000; color: white; border-radius: 8px; width: 100%; }
    .stTextArea>div>div>textarea { border-radius: 10px; border: 1px solid #e0e0e0; }
    h1 { color: #1a1a1a; font-family: 'Inter', sans-serif; font-weight: 700; }
    .insight-card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIC: INITIALIZE AI
st.sidebar.title("⏹️ Square Pulse")
api_key = st.sidebar.text_input("Enter API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')

# 3. UI LAYOUT
st.title("Merchant Feedback Intelligence")
st.caption("AI-Native Product Management for Square Sellers")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### 📥 Input Feedback")
    user_input = st.text_area("Paste customer reviews:", height=300, 
                             placeholder="Example: The POS is fast but the reporting is confusing...")
    analyze_btn = st.button("Generate Dashboard")
    # Create a 'Demo' button next to the 'Generate' button
col_a, col_b = st.columns(2)
with col_a:
    analyze_btn = st.button("Generate Dashboard")
with col_b:
    demo_btn = st.button("🚀 Run Demo (No API Key Needed)")

# If they click the demo button, we use hardcoded data
if demo_btn:
    json_data = {
        "sentiment_score": 85,
        "sentiment_history": [70, 75, 80, 82, 85],
        "top_keywords": {"Fast": 10, "Reliable": 8, "Easy": 15},
        "feature_recommendation": "Implement an 'AI-Morning Summary' for sellers to see top customer issues before they open.",
        "summary": "Overall sentiment is high, specifically regarding the new Afterpay integration."
    }
    # Then trigger the visualization code below...

if analyze_btn and api_key:
    with st.spinner("Analyzing high-dimensional feedback..."):
        # We ask the AI to return JSON so we can build charts!
        prompt = f"""
        Analyze these reviews: {user_input}
        Return ONLY a JSON object with:
        "sentiment_score": (int 1-100),
        "sentiment_history": [list of 5 random ints around the score to simulate a week's trend],
        "top_keywords": {{"Keyword": frequency_int}},
        "feature_recommendation": "string",
        "summary": "string"
        """
        response = model.generate_content(prompt)
        # Clean the response to ensure it's valid JSON
        json_data = json.loads(response.text.replace('```json', '').replace('```', ''))

        with col2:
            st.markdown("### 📊 Merchant Health Overview")
            
            # Metric Row
            m1, m2 = st.columns(2)
            m1.metric("Average Sentiment", f"{json_data['sentiment_score']}%", delta="4%")
            m2.metric("Review Volume", len(user_input.split('\n')), delta="12%")

            # CHART: Sentiment Trend
            df = pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu", "Fri"], "Sentiment": json_data['sentiment_history']})
            fig = px.line(df, x="Day", y="Sentiment", title="Weekly Sentiment Trend", 
                         color_discrete_sequence=['#00d44a']) # Square Green
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

            # AI Insights Card
            st.markdown(f"""
            <div class="insight-card">
                <h4>🤖 AI Product Recommendation</h4>
                <p>{json_data['feature_recommendation']}</p>
                <hr>
                <p><strong>Executive Summary:</strong> {json_data['summary']}</p>
            </div>
            """, unsafe_allow_html=True)
