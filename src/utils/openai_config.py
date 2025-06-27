"""
OpenAI Configuration
Module để cấu hình và tạo kết nối với OpenAI API
"""

import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Optional

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class OpenAIConfig:
    """Configuration class for OpenAI with Singleton pattern"""
    
    _instance = None
    _client = None
    _api_key_validated = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if not hasattr(self, '_initialized'):
            self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            self._initialized = True
        
    def create_openai_client(self) -> ChatOpenAI:
        """
        Tạo ChatOpenAI client với singleton pattern
        """
        # Return existing client if available
        if self._client is not None:
            logger.info(f"♻️ Reusing existing OpenAI client - Model: {self.model_name}")
            return self._client
            
        try:
            # Tạo ChatOpenAI client
            openai_client = ChatOpenAI(
                model=self.model_name,
                api_key=self.api_key,
                base_url=self.base_url,
                temperature=0.1,
                max_tokens=2048,
                max_retries=3,
                request_timeout=30
            )
            
            # Cache the client
            self._client = openai_client
            logger.info(f"✅ OpenAI client created - Model: {self.model_name}")
            return openai_client
            
        except Exception as e:
            logger.error(f"❌ Failed to create OpenAI client: {str(e)}")
            raise

    def validate_api_key(self) -> bool:
        """
        Kiểm tra tính hợp lệ của OpenAI API key (cached)
        """
        # Return cached result if already validated
        if self._api_key_validated:
            return True
            
        if not self.api_key:
            logger.error("❌ OpenAI API key not found in environment variables")
            return False
            
        if not self.api_key.startswith('sk-'):
            logger.error("❌ Invalid OpenAI API key format")
            return False
            
        try:
            # Test API key with a simple request
            test_client = ChatOpenAI(
                model=self.model_name,
                api_key=self.api_key,
                base_url=self.base_url,
                max_tokens=1
            )
            
            # Simple test call
            from langchain.schema import HumanMessage
            test_client.invoke([HumanMessage(content="Hi")])
            
            self._api_key_validated = True
            logger.info(f"✅ OpenAI API key valid for model: {self.model_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ OpenAI API key validation failed: {str(e)}")
            return False

# Global singleton instance
_openai_config = None

def get_openai_llm(temperature: float = 0.1, max_tokens: int = 4096) -> ChatOpenAI:
    """
    Convenience function để tạo ChatOpenAI instance với singleton pattern
    
    Args:
        temperature: Độ sáng tạo của model (0.0-1.0)
        max_tokens: Số token tối đa cho response
        
    Returns:
        ChatOpenAI: Configured ChatOpenAI instance
    """
    global _openai_config
    
    if _openai_config is None:
        _openai_config = OpenAIConfig()
    
    # Validate API key trước khi tạo client (cached)
    if not _openai_config.validate_api_key():
        raise ValueError("❌ Invalid OpenAI API key. Please check your environment variables.")
    
    openai_client = _openai_config.create_openai_client()
    
    # Override temperature và max_tokens nếu được cung cấp
    openai_client.temperature = temperature
    openai_client.max_tokens = max_tokens
    
    return openai_client 