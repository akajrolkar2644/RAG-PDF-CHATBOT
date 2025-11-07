import requests
import requests
import time
from typing import Optional, List, Dict, Any
from backend.config.settings import HF_API_KEY, HF_LLM_MODEL

class LLMManager:
    def __init__(self):
        # List of fallback models in order of preference
        self.models = [
            HF_LLM_MODEL,
            "microsoft/DialoGPT-large",
            "facebook/blenderbot-400M-distill",
            "google/flan-t5-base"
        ]
        self.current_model = HF_LLM_MODEL
        self.api_url = f"https://api-inference.huggingface.co/models/{self.current_model}"
        self.headers = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}
        
    def _try_model(self, model_name: str, prompt: str, max_retries: int = 2) -> Optional[str]:
        """Try to generate text with a specific model"""
        api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        for attempt in range(max_retries):
            try:
                # Model-specific payload preparation
                if "flan-t5" in model_name.lower():
                    payload = {"inputs": f"Answer this question: {prompt}"}
                elif "blenderbot" in model_name.lower():
                    payload = {"inputs": prompt}
                else:
                    payload = {"inputs": prompt}
                
                response = requests.post(
                    api_url, 
                    headers=self.headers, 
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Handle different response formats
                    if isinstance(result, list) and len(result) > 0:
                        if "generated_text" in result[0]:
                            # Extract only the new generated text, not the input prompt
                            generated = result[0]["generated_text"]
                            if generated.startswith(prompt):
                                generated = generated[len(prompt):].strip()
                            return generated if generated else "I understand your question, but I need more context to provide a specific answer."
                        elif "translation_text" in result[0]:
                            return result[0]["translation_text"]
                    
                    return "I understand your question, but I'm having trouble generating a detailed response right now."
                    
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                        
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                    

    
    def _generate_simple_response(self, prompt: str, context: str = "") -> str:
        """Generate a simple rule-based response when API models fail"""
        prompt_lower = prompt.lower()
        
        # Extract key information from context if available
        context_summary = ""
        if context:
            # Take first few sentences of context
            sentences = context.split('.')[0:3]
            context_summary = '. '.join(sentences)
            if len(context_summary) > 200:
                context_summary = context_summary[:200] + "..."
        
        # Simple pattern-based responses
        if any(word in prompt_lower for word in ['what is', 'what are', 'define', 'explain']):
            if context_summary:
                return f"Based on the provided context: {context_summary}. This appears to be relevant information that can help answer your question about the topic you mentioned."
            return "I can see you're asking for an explanation or definition. While I don't have access to advanced language models right now, I can tell you that the document context should contain relevant information to help answer your question."
        
        elif any(word in prompt_lower for word in ['how', 'why', 'when', 'where']):
            if context_summary:
                return f"Based on the document context: {context_summary}. This information from your uploaded documents should help provide insights into your question."
            return "I understand you're looking for detailed information. The context from your uploaded documents contains relevant details that should address your question."
        
        elif any(word in prompt_lower for word in ['list', 'show', 'tell me about']):
            if context_summary:
                return f"From the available information: {context_summary}. The documents you've uploaded contain additional details that are relevant to your request."
            return "I can see you're looking for specific information. Your uploaded documents should contain the details you're seeking."
        
        else:
            if context_summary:
                return f"Based on your uploaded documents: {context_summary}. This context from your files should provide relevant information for your inquiry."
            return "I understand your question. While I'm currently operating with limited capabilities, the context from your uploaded documents should contain information relevant to your query. Please refer to the source documents for more detailed information."
    
    def generate(self, prompt: str, context: str = "") -> str:
        """Generate text with fallback models"""
        if not HF_API_KEY:
            return "Configuration error: Hugging Face API key not found. Please set HF_API_KEY environment variable."
        
        # Clean and prepare prompt
        prompt = prompt.strip()
        if len(prompt) > 1000:  # Limit prompt length
            prompt = prompt[:1000] + "..."
        
        # Try each model in the fallback list
        for model_name in self.models:
            try:
                result = self._try_model(model_name, prompt)
                if result:
                    if model_name != self.current_model:
                        print(f"Switched to fallback model: {model_name}")
                        self.current_model = model_name
                        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
                    return result
            except Exception as e:
                continue
        
        # If all models fail, return a simple rule-based response
        return self._generate_simple_response(prompt, context)