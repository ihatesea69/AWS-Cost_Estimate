"""
AWS Bedrock Configuration
Module để cấu hình và tạo kết nối với AWS Bedrock
"""

import os
import boto3
from langchain_aws import ChatBedrock
from typing import Optional
import logging
from dotenv import load_dotenv
from .rate_limiter import bedrock_rate_limiter, with_retry_and_backoff

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class BedrockConfig:
    """Configuration class for AWS Bedrock with Singleton pattern"""
    
    _instance = None
    _client = None
    _credentials_validated = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BedrockConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if not hasattr(self, '_initialized'):
            # Use Claude 3.5 Sonnet v2 inference profile for cross-region support (can override via env)
            self.model_id = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")
            self.region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
            self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            self._initialized = True
        
    def create_bedrock_client(self) -> ChatBedrock:
        """
        Tạo ChatBedrock client với singleton pattern và rate limiting
        """
        # Return existing client if available
        if self._client is not None:
            logger.info(f"♻️ Reusing existing Bedrock client - Model: {self.model_id}")
            return self._client
            
        try:
            # Tạo ChatBedrock client với rate limiting
            bedrock_client = ChatBedrock(
                model_id=self.model_id,
                region_name=self.region_name,
                credentials_profile_name=None,  # Sử dụng env vars
                temperature=0.1,
                max_tokens=2048,  # Giảm token để tránh throttling
                # Claude 3.5 Sonnet specific configurations với rate limiting
                model_kwargs={
                    "max_tokens": 1024,  # Giảm xuống 1024 để tránh token limits
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "stop_sequences": ["\n\nHuman:"]
                }
            )
            
            # Wrap _generate method với rate limiter (LangChain sử dụng _generate)
            if hasattr(bedrock_client, '_generate'):
                original_generate = bedrock_client._generate
                
                @with_retry_and_backoff(max_retries=3, base_delay=2.0)
                def rate_limited_generate(*args, **kwargs):
                    bedrock_rate_limiter.wait_if_needed()
                    return original_generate(*args, **kwargs)
                
                bedrock_client._generate = rate_limited_generate
            
            # Cache the client
            self._client = bedrock_client
            logger.info(f"✅ AWS Bedrock client created with rate limiting - Model: {self.model_id}")
            return bedrock_client
            
        except Exception as e:
            logger.error(f"❌ Failed to create Bedrock client: {str(e)}")
            raise

    def validate_credentials(self) -> bool:
        """
        Kiểm tra tính hợp lệ của AWS credentials (cached)
        """
        # Return cached result if already validated
        if self._credentials_validated:
            return True
            
        try:
            session = boto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
            
            # Test credentials bằng cách gọi STS
            sts = session.client('sts')
            identity = sts.get_caller_identity()
            
            self._credentials_validated = True
            logger.info(f"✅ AWS Credentials valid. Account: {identity.get('Account')}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Invalid AWS credentials: {str(e)}")
            return False

# Global singleton instance
_bedrock_config = None

def get_bedrock_llm(temperature: float = 0.1, max_tokens: int = 4096) -> ChatBedrock:
    """
    Convenience function để tạo ChatBedrock instance với singleton pattern
    
    Args:
        temperature: Độ sáng tạo của model (0.0-1.0)
        max_tokens: Số token tối đa cho response
        
    Returns:
        ChatBedrock: Configured ChatBedrock instance
    """
    global _bedrock_config
    
    if _bedrock_config is None:
        _bedrock_config = BedrockConfig()
    
    # Validate credentials trước khi tạo client (cached)
    if not _bedrock_config.validate_credentials():
        raise ValueError("❌ Invalid AWS credentials. Please check your environment variables.")
    
    bedrock_client = _bedrock_config.create_bedrock_client()
    
    # Override temperature và max_tokens nếu được cung cấp
    bedrock_client.temperature = temperature
    bedrock_client.model_kwargs["temperature"] = temperature
    bedrock_client.model_kwargs["max_tokens"] = max_tokens
    
    return bedrock_client 