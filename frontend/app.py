import streamlit as st
import requests
import json
from typing import Optional
import time
import base64
from datetime import datetime

# Configure page with modern settings
st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with glass morphism and gradients
def load_modern_css():
    st.markdown("""
    <style>
    /* Modern CSS Reset and Base */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main container with glass effect */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 20px;
        padding: 0;
    }
    
    /* Modern Header */
    .modern-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 24px 24px 0 0;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .modern-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" preserveAspectRatio="none"><path d="M0,0 L1000,100 L0,100 Z" fill="rgba(255,255,255,0.1)"/></svg>');
        background-size: cover;
    }
    
    .modern-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        position: relative;
        background: linear-gradient(45deg, #fff, #f0f4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .modern-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
    }
    
    .subtitle {
        font-size: 1.1rem;
        opacity: 0.8;
        margin-top: -1rem;
        margin-bottom: 2rem;
    }
    
    /* Card Components */
    .modern-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Chat Messages - DARKER COLORS FOR BETTER VISIBILITY */
    .user-message {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
        animation: slideInRight 0.3s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .assistant-message {
        background: rgba(30, 41, 59, 0.95);
        color: white;
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 18px 18px 18px 4px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* Status Indicators */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-online {
        background: rgba(34, 197, 94, 0.1);
        color: #16a34a;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    .status-offline {
        background: rgba(239, 68, 68, 0.1);
        color: #dc2626;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 12px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* File Uploader */
    .upload-section {
        background: rgba(255, 255, 255, 0.6);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .upload-section:hover {
        border-color: rgba(102, 126, 234, 0.6);
        background: rgba(255, 255, 255, 0.8);
    }
    
    /* Animations */
    @keyframes slideInRight {
        from {
            transform: translateX(30px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-30px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.5);
    }
    
    /* Sidebar styling */
    .sidebar-content {
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 0 0 0 24px;
        min-height: 100vh;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(30, 41, 59, 0.9);
        color: white;
        padding: 0.5rem 1rem;
        text-align: center;
        font-size: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .modern-header h1 {
            font-size: 2rem;
        }
        
        .user-message, .assistant-message {
            max-width: 90%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration (unchanged)
API_BASE_URL = "http://127.0.0.1:8000/api"

def upload_pdf_to_api(uploaded_file) -> Optional[dict]:
    """Upload PDF file to the backend API"""
    try:
        files = {"files": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend API. Make sure the server is running.")
        return None
    except Exception as e:
        st.error(f"Upload error: {str(e)}")
        return None

def ask_question_to_api(question: str, top_k: int = 5) -> Optional[dict]:
    """Send question to the backend API"""
    try:
        params = {"query": question}
        response = requests.post(f"{API_BASE_URL}/query", params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Query failed: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend API. Make sure the server is running.")
        return None
    except Exception as e:
        st.error(f"Query error: {str(e)}")
        return None

def stream_ask_question(question: str, top_k: int = 5):
    """Stream question to the backend API"""
    try:
        params = {"query": question}
        with requests.post(f"{API_BASE_URL}/query-stream", params=params, stream=True) as r:
            if r.status_code == 200:
                for chunk in r.iter_content(None, decode_unicode=True):
                    yield chunk
            else:
                st.error(f"Query failed: {r.status_code} - {r.text}")
                yield "Sorry, I couldn't process your question. Please try again."
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend API. Make sure the server is running.")
        yield "Cannot connect to backend API. Please make sure the server is running."
    except Exception as e:
        st.error(f"Query error: {str(e)}")
        yield "Sorry, I couldn't process your question. Please try again."

def check_api_health() -> bool:
    """Check if the backend API is running"""
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api', '')}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_system_status():
    """Get detailed system status from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def display_modern_message(role, content, sources=None):
    """Display a modern chat message"""
    if role == "user":
        st.markdown(f'<div class="user-message"><strong>You:</strong> {content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message"><strong>🤖 Assistant:</strong> {content}', unsafe_allow_html=True)
        if sources:
            with st.expander("📚 View Sources", expanded=False):
                st.write(f"Answer based on {len(sources)} document chunks:")
                for i, source in enumerate(sources, 1):
                    if isinstance(source, dict) and "text" in source:
                        with st.container():
                            st.markdown(f"**Source {i}**")
                            st.markdown(f'<div class="modern-card" style="background: rgba(255,255,255,0.9); color: #333;">{source.get("text", "No text available.")}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"{i}. {source}")
        st.markdown("</div>", unsafe_allow_html=True)

def create_document_card(filename, details):
    """Create a modern document card"""
    with st.container():
        st.markdown(f"""
        <div class="modern-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <h4 style="margin: 0; color: #333;">📄 {filename}</h4>
                <span style="background: rgba(34, 197, 94, 0.1); color: #16a34a; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.875rem; font-weight: 600;">
                    {details['chunks']} chunks
                </span>
            </div>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Status: {details['status']}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Load modern CSS
    load_modern_css()
    
    # Initialize session state
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = {}
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'messages' not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "Hello! I'm your AI document assistant. Upload PDF documents and ask me anything about them! 🚀"
        }]
    
    # Create sidebar on LEFT side
    with st.sidebar:
        #st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Simplified sidebar header without the white banner
        st.subheader("⚙️ Control Panel")
        
        # System status
        api_connected = check_api_health()
        system_status = get_system_status() if api_connected else None
        
        # System status card
        st.markdown("""
        <div class="modern-card">
            <h4 style="margin-bottom: 1rem; color: #333;">System Status</h4>
        """, unsafe_allow_html=True)
        
        status_col1, status_col2 = st.columns(2)
        with status_col1:
            st.metric("API Status", "Connected" if api_connected else "Disconnected")
        with status_col2:
            doc_count = system_status.get("vector_store", {}).get("document_count", 0) if system_status else 0
            st.metric("Documents", doc_count)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Knowledge base section
        st.subheader("🗂️ Knowledge Base")
        
        if not st.session_state.processed_files:
            st.info("👆 Upload documents to build your knowledge base")
        else:
            for filename, details in st.session_state.processed_files.items():
                create_document_card(filename, details)
            
            total_chunks = sum(details['chunks'] for details in st.session_state.processed_files.values())
            st.markdown(f"""
            <div class="modern-card">
                <div style="text-align: center;">
                    <h4 style="color: #333; margin-bottom: 0.5rem;">📊 Total Content</h4>
                    <p style="font-size: 1.5rem; font-weight: bold; color: #667eea; margin: 0;">{total_chunks} chunks</p>
                    <p style="color: #666; margin: 0;">across {len(st.session_state.processed_files)} documents</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Settings section
        st.subheader("⚙️ Settings")
        
        with st.container():
            top_k = st.slider(
                "Retrieval chunks per query",
                min_value=1,
                max_value=10,
                value=5,
                help="Number of document chunks to use for context"
            )
            st.session_state['top_k'] = top_k
            
            # Model settings (placeholder for future features)
            st.selectbox(
                "Response Style",
                ["Balanced", "Detailed", "Concise"],
                help="Adjust how detailed the responses should be"
            )
        
        # Add footer at the bottom of sidebar
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem 0; color: #666;">
                <p style="margin: 0.25rem 0; font-size: 0.9rem;"><strong>Anant Kajrolkar</strong></p>
                <p style="margin: 0.25rem 0; font-size: 0.8rem;">akajrolkar9727@gmail.com</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Modern header with subtitle
    st.markdown("""
    <div class="modern-header">
        <h1>🧠 PDF RAG Assistant</h1>
        <p>Transform your PDF documents into an interactive knowledge base with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content layout
    st.markdown('<div style="padding: 2rem;">', unsafe_allow_html=True)
    
    # Document Upload Section in Main Area
    st.subheader("📄 Upload Documents")
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drag & drop PDF files here",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload PDF documents to build your knowledge base",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_files:
        if st.button("🚀 Process Documents", type="primary", use_container_width=True):
            with st.status("Processing documents...", expanded=True) as status:
                total_chunks = 0
                processed_files = []
                for i, uploaded_file in enumerate(uploaded_files):
                    st.write(f"📄 Processing {uploaded_file.name}...")
                    result = upload_pdf_to_api(uploaded_file)
                    if result:
                        chunks = result.get('chunks', 0)
                        total_chunks += chunks
                        st.session_state.processed_files[uploaded_file.name] = {
                            "chunks": chunks,
                            "status": "✅ Processed",
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        }
                        processed_files.append(uploaded_file.name)
                        st.success(f"✅ Added {chunks} chunks")
                    time.sleep(0.5)
                
                status.update(label=f"Processing complete! Added {total_chunks} total chunks from {len(processed_files)} files.", state="complete")
                st.balloons()
    
    # Chat Section
    st.markdown("---")
    
    # Chat header with stats
    header_col1, header_col2, header_col3 = st.columns([2, 1, 1])
    with header_col1:
        st.subheader("💬 Document Chat")
    with header_col2:
        if api_connected:
            st.markdown('<div class="status-badge status-online">🟢 Online</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge status-offline">🔴 Offline</div>', unsafe_allow_html=True)
    with header_col3:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [{
                "role": "assistant", 
                "content": "Chat cleared! How can I help you with your documents?"
            }]
            st.rerun()
    
    # Chat container with modern styling
    chat_container = st.container(height=500, border=False)
    
    with chat_container:
        for message in st.session_state.messages:
            display_modern_message(message["role"], message["content"], message.get("sources"))
    
    # Chat input at the bottom of main area
    user_input = st.chat_input("💭 Ask a question about your documents...")
    
    # Sample questions in a modern grid
    st.markdown("### 💡 Quick Questions")
    sample_queries = [
        "Summarize the main topics",
        "What are the key findings?",
        "Explain the methodology",
        "List important dates/events",
        "Who are the main contributors?"
    ]
    
    cols = st.columns(3)
    for i, query in enumerate(sample_queries):
        with cols[i % 3]:
            if st.button(f"💬 {query}", key=f"sample_{i}", use_container_width=True):
                user_input = query
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle chat input
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response with streaming
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            for chunk in stream_ask_question(user_input, st.session_state.get('top_k', 5)):
                full_response += chunk
                response_placeholder.markdown(f'<div class="assistant-message"><strong>🤖 Assistant:</strong> {full_response}</div>', unsafe_allow_html=True)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
        
        st.rerun()

if __name__ == "__main__":
    main()