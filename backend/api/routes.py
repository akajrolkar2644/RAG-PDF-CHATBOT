from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any, Union, AsyncGenerator
import os
import tempfile
import asyncio
from backend.core.vector_store import VectorStore
from backend.core.query_engine import generate_answer
from backend.core.llm_manager import LLMManager
from backend.utils.pdf_processor import extract_text_from_pdf
from backend.config.settings import VECTOR_STORE_PATH

router: APIRouter = APIRouter()

# Initialize components
vector_store: VectorStore = VectorStore()
llm_manager: LLMManager = LLMManager()

@router.post("/upload")
async def upload_pdf(files: List[UploadFile] = File(...)) -> Dict[str, Any]:
    """Upload and process PDF files"""
    try:
        processed_files: List[str] = []
        failed_files: List[Dict[str, str]] = []
        
        for file in files:
            if not file.filename:
                failed_files.append({"filename": "Unknown", "reason": "No filename provided"})
                continue
                
            if not file.filename.endswith('.pdf'):
                failed_files.append({"filename": file.filename, "reason": "Not a PDF file"})
                continue
                
            try:
                # Save file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    content = await file.read()
                    tmp_file.write(content)
                    tmp_path = tmp_file.name
                
                # Extract text
                text_chunks = extract_text_from_pdf(tmp_path)
                
                # If extract_text_from_pdf returns a list of chunks
                if isinstance(text_chunks, list):
                    text = " ".join(text_chunks)
                else:
                    text = text_chunks
                
                # Split into chunks and add to vector store
                chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
                docs_meta = [
                    {"text": chunk, "source": file.filename, "chunk": i} 
                    for i, chunk in enumerate(chunks)
                ]
                vector_store.add_documents(docs_meta)
                
                # Clean up
                os.unlink(tmp_path)
                
                processed_files.append(file.filename)
            except Exception as e:
                failed_files.append({"filename": file.filename or "Unknown", "reason": str(e)})
        
        return {
            "message": f"Processed {len(processed_files)} files",
            "processed": processed_files,
            "failed": failed_files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_documents(query: str = Query(..., min_length=1)) -> Dict[str, Any]:
    """Query the document collection"""
    try:
        # Search for relevant documents
        docs = vector_store.similarity_search(query, top_k=5)
        
        # Generate answer using LLM
        answer = generate_answer(query, docs, llm_manager)
        
        # Extract sources
        sources = list(set([doc["source"] for doc in docs]))
        
        return {
            "answer": answer,
            "sources": sources,
            "documents": docs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query-stream")
async def query_documents_stream(query: str = Query(..., min_length=1)) -> StreamingResponse:
    """Query the document collection with streaming response"""
    try:
        # Search for relevant documents
        docs = vector_store.similarity_search(query, top_k=5)
        
        # Generate answer using LLM
        answer = generate_answer(query, docs, llm_manager)
        
        # Extract sources
        sources = list(set([doc["source"] for doc in docs]))
        
        # Stream the response word by word
        async def generate_stream() -> AsyncGenerator[str, None]:
            words = answer.split()
            for i, word in enumerate(words):
                yield word + (" " if i < len(words) - 1 else "")
                await asyncio.sleep(0.05)  # Small delay for visual effect
        
        return StreamingResponse(generate_stream(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_status() -> Dict[str, Any]:
    """Get system status"""
    try:
        # Check if vector store exists and has documents
        index_exists = os.path.exists(os.path.join(VECTOR_STORE_PATH, "index.faiss"))
        doc_count = len(vector_store.metadata) if hasattr(vector_store, 'metadata') else 0
        
        return {
            "status": "online",
            "vector_store": {
                "exists": index_exists,
                "document_count": doc_count
            },
            "model_status": "ready" if llm_manager.current_model else "not configured"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@router.post("/reset")
async def reset_index() -> Dict[str, str]:
    """Reset the vector store index"""
    try:
        # Remove existing index files
        index_file = os.path.join(VECTOR_STORE_PATH, "index.faiss")
        meta_file = os.path.join(VECTOR_STORE_PATH, "meta.pkl")
        
        if os.path.exists(index_file):
            os.remove(index_file)
        if os.path.exists(meta_file):
            os.remove(meta_file)
            
        # Reinitialize vector store
        global vector_store
        vector_store = VectorStore()
        
        return {"message": "Index reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))