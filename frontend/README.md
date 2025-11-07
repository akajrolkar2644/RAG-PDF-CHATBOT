# PDF RAG Chatbot - Frontend

A modern **Streamlit web interface** for the PDF RAG Chatbot system.

## 🎨 Features

- **📋 Drag & Drop PDF Upload**: Easy multi-file document upload
- **💬 Interactive Chat Interface**: ChatGPT-style conversation experience
- **🔍 Real-time Document Processing**: Live progress tracking
- **📁 Source Attribution**: View which document chunks were used
- **⚙️ Configurable Retrieval**: Adjust number of relevant chunks
- **📊 System Monitoring**: Real-time backend connection status
- **🚀 Quick Actions**: Sample queries and chat management

## 🌐 Running the Frontend

### Automated Start (Recommended)
```powershell
.\start_frontend.ps1
```

### Manual Start
```bash
# Activate virtual environment
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Start Streamlit
streamlit run frontend/app.py
```

## 📱 User Interface

### Main Chat Area
- **Upload PDFs**: Use the sidebar to upload multiple documents
- **Ask Questions**: Type questions in the chat input
- **View Responses**: AI-generated answers with source attribution
- **Chat History**: Persistent conversation history

### Sidebar Features
- **📄 Document Management**: Upload and process PDFs
- **🔍 Query Settings**: Configure retrieval parameters
- **📊 System Status**: Monitor backend connectivity
- **🚀 Quick Actions**: Clear chat, access API docs
- **💡 Sample Queries**: Pre-built question examples

## 🔧 Technical Details

- **Framework**: Streamlit 1.49+
- **Backend Integration**: RESTful API communication
- **File Handling**: Multi-format PDF support
- **State Management**: Session-based chat persistence
- **Error Handling**: Graceful API failure management

## 🔗 Integration

The frontend communicates with the FastAPI backend at `http://127.0.0.1:8000/api`:
- `POST /upload-pdf` - Document processing
- `POST /ask` - Question answering
- `GET /docs` - API health checks