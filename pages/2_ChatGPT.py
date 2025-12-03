"""
Week 10: ChatGPT API Integration
"""
import streamlit as st
import os

# Only set page config if running standalone
if "logged_in" not in st.session_state:
    st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
    st.warning("Please login first")
    st.stop()

# Check authentication
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# Header
st.title("🤖 AI Assistant")
st.markdown(f"**User:** {st.session_state.username}")

# Navigation
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()
with col2:
    if st.button("📊 Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

st.divider()

# Get API key
api_key = None
try:
    if hasattr(st, 'secrets') and "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
except:
    pass

if not api_key:
    secrets_path = os.path.join(os.path.dirname(__file__), '..', '.streamlit', 'secrets.toml')
    if os.path.exists(secrets_path):
        try:
            with open(secrets_path) as f:
                for line in f:
                    if 'OPENAI_API_KEY' in line and '=' in line:
                        api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break
        except:
            pass

if not api_key:
    st.error("❌ OpenAI API key not configured")
    st.code('# Add to .streamlit/secrets.toml:\nOPENAI_API_KEY = "sk-..."', language="toml")
    st.stop()

# Initialize OpenAI with environment variable (avoids proxies bug)
os.environ['OPENAI_API_KEY'] = api_key

try:
    from openai import OpenAI
    client = OpenAI()
    st.success("✓ OpenAI connected")
except Exception as e:
    st.error(f"❌ Cannot initialize OpenAI: {str(e)}")
    st.info("Run: `pip install --upgrade openai`")
    st.stop()

# System prompt
SYSTEM_PROMPT = """You are an AI assistant for cybersecurity analysts, data scientists, and IT operations teams. Help with:
- Cybersecurity incident analysis
- Data management  
- IT troubleshooting
- Security best practices

Be clear, professional, and actionable."""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about cybersecurity, data analysis, or IT operations..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Use modern OpenAI API
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ],
                stream=True,
            )
            
            # Stream response
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
        except Exception as e:
            error_str = str(e)
            full_response = f"❌ Error: {error_str}"
            response_placeholder.error(full_response)
            
            # Helpful hints based on error
            if "insufficient_quota" in error_str or "billing" in error_str:
                st.warning("⚠️ **No credits on your OpenAI account**\n\nAdd $5+ at platform.openai.com/settings/organization/billing")
            elif "invalid_api_key" in error_str:
                st.warning("⚠️ **Invalid API key**\n\nCheck your key at platform.openai.com/api-keys")
    
    # Add to history
    if full_response and not full_response.startswith("❌"):
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar
with st.sidebar:
    st.subheader("Chat Controls")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.info(f"**Messages:** {len(st.session_state.messages)}\n**Model:** GPT-3.5-turbo")
    
    st.divider()
    st.markdown("**💡 Tip:** Free tier needs credits at platform.openai.com")