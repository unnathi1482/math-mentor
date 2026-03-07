"""
Groq Client Wrapper - Makes Groq API work like OpenAI API.
This allows us to use Groq with minimal code changes.
"""

from groq import Groq
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.config import GROQ_API_KEY, GROQ_MODEL


class GroqClient:
    """
    Wrapper for Groq API that mimics OpenAI's interface.
    """
    
    def __init__(self, api_key=None):
        self.client = Groq(api_key=api_key or GROQ_API_KEY)
        self.default_model = GROQ_MODEL
    
    class ChatCompletions:
        """Mimics OpenAI's chat.completions interface."""
        
        def __init__(self, client, default_model):
            self.client = client
            self.default_model = default_model
        
        def create(self, model=None, messages=None, temperature=0.1, response_format=None, max_tokens=None, **kwargs):
            """
            Create a chat completion using Groq.
            
            Args:
                model: Model to use (defaults to config)
                messages: List of message dicts
                temperature: Sampling temperature
                response_format: If {"type": "json_object"}, enforce JSON
                max_tokens: Max tokens in response
            
            Returns:
                Response object mimicking OpenAI's format
            """
            # Use provided model or default
            model = model or self.default_model
            
            # Handle JSON mode
            if response_format and response_format.get("type") == "json_object":
                # Add instruction to return JSON
                if messages:
                    system_msg = next((m for m in messages if m["role"] == "system"), None)
                    if system_msg:
                        system_msg["content"] += "\n\nYou MUST respond with valid JSON only. No other text."
            
            # Call Groq
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens or 2048,
                **kwargs
            )
            
            return response
    
    class Audio:
        """Mimics OpenAI's audio interface."""
        
        def __init__(self, client):
            self.client = client
            self.transcriptions = self.Transcriptions(client)
        
        class Transcriptions:
            """Mimics OpenAI's audio.transcriptions interface."""
            
            def __init__(self, client):
                self.client = client
            
            def create(self, model=None, file=None, language="en", prompt="", **kwargs):
                """
                Transcribe audio using Groq's Whisper.
                
                Args:
                    model: Model name (ignored, Groq uses whisper-large-v3)
                    file: Audio file object
                    language: Language code
                    prompt: Optional prompt to guide transcription
                
                Returns:
                    Transcription object
                """
                response = self.client.audio.transcriptions.create(
                    file=file,
                    model="whisper-large-v3",
                    language=language,
                    prompt=prompt,
                    response_format="json"
                )
                
                return response
    
    class Embeddings:
        """Mimics OpenAI's embeddings interface."""
        
        def __init__(self, client):
            self.client = client
        
        def create(self, model=None, input=None, **kwargs):
            """
            Create embeddings using Groq.
            
            Args:
                model: Embedding model (uses nomic-embed-text)
                input: Text or list of texts to embed
            
            Returns:
                Embeddings response
            """
            # Groq uses nomic-embed-text for embeddings
            response = self.client.embeddings.create(
                model="nomic-embed-text-v1.5",
                input=input if isinstance(input, list) else [input]
            )
            
            return response
    
    @property
    def chat(self):
        """Access chat completions."""
        if not hasattr(self, '_chat'):
            self._chat = type('Chat', (), {
                'completions': self.ChatCompletions(self.client, self.default_model)
            })()
        return self._chat
    
    @property
    def audio(self):
        """Access audio transcriptions."""
        if not hasattr(self, '_audio'):
            self._audio = self.Audio(self.client)
        return self._audio
    
    @property
    def embeddings(self):
        """Access embeddings."""
        if not hasattr(self, '_embeddings'):
            self._embeddings = self.Embeddings(self.client)
        return self._embeddings


# Create a singleton instance
groq_client = GroqClient()