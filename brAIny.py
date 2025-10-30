import streamlit as st
from openai import OpenAI
import base64

# ---- Config ----
st.set_page_config(page_title="brAIny", page_icon="🧠", layout="wide")

# Custom CSS for the colorful UI
st.markdown("""
<style>
    /* Main gradient background */
    .stApp {
        background: linear-gradient(135deg, #EFF6FF 0%, #F3E8FF 50%, #FCE7F3 100%);
    }
    
    /* Header styling */
    .brainy-header {
        background: white;
        padding: 1.5rem;
        border-radius: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 3px solid #C084FC;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Tips cards */
    .tip-card {
        background: white;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 2px solid;
        margin: 0.5rem 0;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom chat messages */
    .stChatMessage {
        border-radius: 1rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Image upload area styling */
    .upload-hint {
        background: linear-gradient(135deg, #E0E7FF 0%, #F3E8FF 100%);
        padding: 1rem;
        border-radius: 1rem;
        border: 2px dashed #C084FC;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """
You are a patient, curious, and encouraging tutor that helps students learn SCIENCE and MATHEMATICS through scaffolding — not by giving direct answers.

Your mission:
• Guide the student to discover answers through reasoning.
• Never reveal or state the final answer (see boundaries).
• Use questions, hints, and analogies to stimulate thinking.

Tone:
• Warm, supportive, and conversational.
• Never judgmental. Celebrate effort and curiosity.
• Use simple language appropriate for middle-to-high-school students.

Core teaching behaviors:
1. Start by identifying what the student already knows or notices.
2. Ask open-ended questions that prompt reflection (e.g. 'What happens if…?', 'Why do you think…?', 'Can you connect this to…?').
3. Provide small hints or partial steps when the student is stuck.
4. When giving feedback, focus on logic and process, not just correctness.
5. Use examples, real-world analogies, or visuals to deepen understanding.
6. For science questions, emphasize observation → inference → explanation.
7. For math questions, emphasize patterns → relationships → generalization.

Boundaries:
• Do NOT give final numeric or definitive answers unless the student asks to check if the answer they got was correct.
• Do NOT solve problems in one step or show full working.
• Avoid over-explaining; let the student think between prompts.
• Always continue the scaffolding by asking questions at the end.

When analyzing images:
• First, describe what you observe in the image (equations, diagrams, text, etc.)
• Ask the student what they understand so far before diving into guidance
• Use the visual content to enhance your scaffolding approach

Your goal is to nurture independent reasoning and curiosity — every conversation should lead the student to say 'Oh, I see!' rather than 'Thanks for the answer.'
"""

# ---- Helper function for image encoding ----
def encode_image(uploaded_file):
    """Convert uploaded file to base64 string for OpenAI API"""
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# ---- Client ----
api_key = st.secrets.get("OPENAI_API_KEY", None)
if not api_key:
    st.error("⚠️ Missing OPENAI_API_KEY in .streamlit/secrets.toml")
    st.stop()
client = OpenAI(api_key=api_key)

# ---- Session state ----
if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": SYSTEM_PROMPT}]
if "subject" not in st.session_state:
    st.session_state.subject = None
if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"

# ---- Sidebar ----
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Model selection
    model_option = st.selectbox(
        "AI Model", 
        ["gpt-4o (use this for images!)", "gpt-4o-mini (text only)"], 
        index=0
    )
    st.session_state.model = model_option.split()[0]  # Extract just "gpt-4o-mini" or "gpt-4o"
    
    st.divider()
    
    # Current subject display
    if st.session_state.subject:
        subject_emoji = "🔢" if st.session_state.subject == "Math" else "🔬"
        st.markdown(f"**Current Subject:** {subject_emoji} {st.session_state.subject}")
        if st.button("📚 Change Subject"):
            st.session_state.subject = None
            st.session_state.history = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.rerun()
    
    st.divider()
    
    # New chat button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()
    
    st.caption("💡 Scaffold-only tutor • No direct answers")
    
    if st.session_state.model == "gpt-4o":
        st.info("📸 Image uploads enabled! You can upload photos of homework problems.")

# ---- Header ----
st.markdown("""
<div class="brainy-header">
    <h1 style="margin:0; background: linear-gradient(to right, #9333EA, #EC4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">
        🧠 brAIny
    </h1>
    <p style="color: #6B7280; margin-top: 0.5rem;">Your AI Homework Buddy!</p>
</div>
""", unsafe_allow_html=True)

# ---- Tips Section (show at top when subject is selected) ----
if st.session_state.subject:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='tip-card' style='border-color: #FBBF24;'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>💡</div>
            <div style='font-weight: bold; color: #1F2937; margin-bottom: 0.25rem;'>Ask Questions!</div>
            <div style='font-size: 0.875rem; color: #6B7280;'>Don't be shy - asking is how we learn!</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='tip-card' style='border-color: #10B981;'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>📚</div>
            <div style='font-weight: bold; color: #1F2937; margin-bottom: 0.25rem;'>Think First</div>
            <div style='font-size: 0.875rem; color: #6B7280;'>Try solving it yourself before asking for hints!</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='tip-card' style='border-color: #C084FC;'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>✨</div>
            <div style='font-weight: bold; color: #1F2937; margin-bottom: 0.25rem;'>Learn Together</div>
            <div style='font-size: 0.875rem; color: #6B7280;'>I'll guide you step-by-step to understand!</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

# ---- Subject Selection ----
if not st.session_state.subject:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; background: white; padding: 2rem; border-radius: 1.5rem; 
                    box-shadow: 0 10px 15px rgba(0,0,0,0.1); border: 4px solid #C084FC;'>
            <h2 style='color: #1F2937; margin-bottom: 1rem;'>✨ Let's get started!</h2>
            <p style='color: #6B7280; margin-bottom: 1.5rem;'>What subject are you working on?</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Subject buttons
        col_math, col_science = st.columns(2)
        
        with col_math:
            if st.button("🔢 Math", use_container_width=True, key="math_btn"):
                st.session_state.subject = "Math"
                st.session_state.history = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "assistant", "content": "Hi there! 👋 I'm brAIny, your math buddy! I'm here to help you understand math concepts by guiding you through problems step-by-step. What math topic are you working on today?"}
                ]
                st.rerun()
        
        with col_science:
            if st.button("🔬 Science", use_container_width=True, key="science_btn"):
                st.session_state.subject = "Science"
                st.session_state.history = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "assistant", "content": "Hi there! 👋 I'm brAIny, your science buddy! I'm here to help you explore scientific concepts through questions and experiments. What science topic are you curious about today?"}
                ]
                st.rerun()

# ---- Chat Interface (only show if subject is selected) ----
if st.session_state.subject:
    # ---- Use Streamlit container for better control ----
    with st.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        
    # Image upload section (only show if using gpt-4o)
    if st.session_state.model == "gpt-4o":
        uploaded_file = st.file_uploader(
            "Upload an image of your homework problem",
            type=["png", "jpg", "jpeg"],
            help="Take a clear photo of your math or science problem"
        )
        
        if uploaded_file:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(uploaded_file, caption="Your uploaded image", use_container_width=True)
            with col2:
                optional_text = st.text_area(
                    "Add a question about this image (optional)",
                    placeholder="e.g., 'I don't understand step 3' or 'Can you help me solve this?'",
                    height=100
                )
            
            if st.button("📤 Send Image", use_container_width=True, type="primary"):
                # Encode image
                base64_image = encode_image(uploaded_file)
                
                # Build message content with image (Responses API format)
                # Text first, then image with data URI
                text_to_send = optional_text if optional_text else "Can you help me understand this problem?"
                
                user_content = [
                    {
                        "type": "input_text",
                        "text": text_to_send
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
                
                # Append to history
                st.session_state.history.append({
                    "role": "user",
                    "content": user_content
                })
                
                # Display user message
                with st.chat_message("user", avatar="🧑‍🎓"):
                    st.image(uploaded_file, width=300)
                    if optional_text:
                        st.markdown(optional_text)
                
                # Get AI response
                with st.chat_message("assistant", avatar="🧠"):
                    with st.spinner("🤔 Looking at your problem..."):
                        try:
                            # Keep rolling window
                            MAX_TURNS = 20
                            non_system = [m for m in st.session_state.history if m["role"] != "system"]
                            if len(non_system) > MAX_TURNS:
                                st.session_state.history = [st.session_state.history[0]] + non_system[-MAX_TURNS:]
                            
                            resp = client.responses.create(
                                model=st.session_state.model,
                                input=st.session_state.history
                            )
                            ai_text = resp.output_text
                        except Exception as e:
                            ai_text = f"Oops! Something went wrong: {e}"
                        
                        st.markdown(ai_text)
                
                # Append assistant response
                st.session_state.history.append({"role": "assistant", "content": ai_text})
                st.rerun()
        
        # Display chat history (skip system message)
    for m in st.session_state.history[1:]:
        with st.chat_message("user" if m["role"] == "user" else "assistant", avatar="🧑‍🎓" if m["role"] == "user" else "🧠"):
            # Handle text content
            if isinstance(m.get("content"), str):
                st.markdown(m["content"])
            # Handle content with images (list format)
            elif isinstance(m.get("content"), list):
                for item in m["content"]:
                    if item.get("type") == "input_text":
                        st.markdown(item.get("text", ""))
                    elif item.get("type") == "input_image":
                        st.caption("📸 Image uploaded")
    
    
    
    # Chat input (for text-only messages)
    user_msg = st.chat_input("💭 Type your question here...")
    
    if user_msg:
        # Append user message
        st.session_state.history.append({"role": "user", "content": user_msg})
        
        # Display user message
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(user_msg)
        
        # Keep rolling window of conversation
        MAX_TURNS = 20
        non_system = [m for m in st.session_state.history if m["role"] != "system"]
        if len(non_system) > MAX_TURNS:
            st.session_state.history = [st.session_state.history[0]] + non_system[-MAX_TURNS:]
        
        # Get AI response
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Use Responses API
                    resp = client.responses.create(
                        model=st.session_state.model,
                        input=st.session_state.history
                    )
                    ai_text = resp.output_text
                except Exception as e:
                    ai_text = f"Oops! Something went wrong: {e}"
                
                st.markdown(ai_text)
        
        # Append assistant message
        st.session_state.history.append({"role": "assistant", "content": ai_text})
        st.rerun()