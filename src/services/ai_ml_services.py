"""
AI/ML Services Handlers - Bedrock, Comprehend, Rekognition, etc.

This module contains handlers for AWS AI/ML services following the
service-oriented architecture pattern.
"""

from typing import Dict, Any, List
from .service_registry import BaseServiceHandler, service_registry
import logging

logger = logging.getLogger(__name__)

class BedrockServiceHandler(BaseServiceHandler):
    """Handler for Amazon Bedrock service"""
    
    def get_service_name(self) -> str:
        return "Amazon Bedrock"
    
    def get_search_terms(self) -> List[str]:
        return ["Bedrock", "Amazon Bedrock", "Foundation Models"]
    
    def get_service_category(self) -> str:
        return "ml"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "model": "Claude 3 Sonnet",
            "input_tokens": "1000000",
            "output_tokens": "100000",
            "region": "US East (N. Virginia)",
            "pricing_model": "On-Demand"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        if not config.get("model"):
            errors.append("Bedrock: model is required")
        
        input_tokens = config.get("input_tokens", "1000000")
        try:
            tokens_val = int(input_tokens)
            if tokens_val < 1:
                errors.append("Bedrock: input_tokens must be positive")
        except (ValueError, TypeError):
            errors.append("Bedrock: input_tokens must be a valid number")
        
        output_tokens = config.get("output_tokens", "100000")
        try:
            tokens_val = int(output_tokens)
            if tokens_val < 1:
                errors.append("Bedrock: output_tokens must be positive")
        except (ValueError, TypeError):
            errors.append("Bedrock: output_tokens must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        ADD AMAZON BEDROCK SERVICE:

        Step 1: Service Selection
        - Search for "Bedrock" in the service search box
        - Look for "Amazon Bedrock" service card (Foundation Models)
        - Click "Configure" button on the Amazon Bedrock service card
        - Verify URL contains "bedrock" after page loads

        Step 2: Configuration
        Configure Bedrock with these settings:
        - Region: {full_config['region']}
        - Model: {full_config['model']}
        - Input Tokens: {full_config['input_tokens']}
        - Output Tokens: {full_config['output_tokens']}
        - Pricing Model: {full_config['pricing_model']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm Bedrock appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 120  # AI services can have complex pricing models
    
    def get_complexity_score(self) -> int:
        return 7  # High complexity due to model selection

class ComprehendServiceHandler(BaseServiceHandler):
    """Handler for Amazon Comprehend service"""
    
    def get_service_name(self) -> str:
        return "Amazon Comprehend"
    
    def get_search_terms(self) -> List[str]:
        return ["Comprehend", "Amazon Comprehend", "Natural Language Processing"]
    
    def get_service_category(self) -> str:
        return "ml"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "characters_per_month": "1000000",
            "api_requests": "10000",
            "region": "US East (N. Virginia)",
            "analysis_type": "Sentiment Analysis"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        characters = config.get("characters_per_month", "1000000")
        try:
            char_val = int(characters)
            if char_val < 1:
                errors.append("Comprehend: characters_per_month must be positive")
        except (ValueError, TypeError):
            errors.append("Comprehend: characters_per_month must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        📝 ADD AMAZON COMPREHEND SERVICE:

        Step 1: Service Selection
        - Search for "Comprehend" in the service search box
        - Look for "Amazon Comprehend" service card (Natural Language Processing)
        - Click "Configure" button on the Amazon Comprehend service card
        - Verify URL contains "comprehend" after page loads

        Step 2: Configuration
        Configure Comprehend with these settings:
        - Region: {full_config['region']}
        - Analysis Type: {full_config['analysis_type']}
        - Characters per month: {full_config['characters_per_month']}
        - API Requests: {full_config['api_requests']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm Comprehend appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 100
    
    def get_complexity_score(self) -> int:
        return 5  # Medium complexity

class RekognitionServiceHandler(BaseServiceHandler):
    """Handler for Amazon Rekognition service"""
    
    def get_service_name(self) -> str:
        return "Amazon Rekognition"
    
    def get_search_terms(self) -> List[str]:
        return ["Rekognition", "Amazon Rekognition", "Image Analysis"]
    
    def get_service_category(self) -> str:
        return "ml"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "images_per_month": "10000",
            "analysis_type": "Object Detection",
            "region": "US East (N. Virginia)"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        images = config.get("images_per_month", "10000")
        try:
            img_val = int(images)
            if img_val < 1:
                errors.append("Rekognition: images_per_month must be positive")
        except (ValueError, TypeError):
            errors.append("Rekognition: images_per_month must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        👁️ ADD AMAZON REKOGNITION SERVICE:

        Step 1: Service Selection
        - Search for "Rekognition" in the service search box
        - Look for "Amazon Rekognition" service card (Image and Video Analysis)
        - Click "Configure" button on the Amazon Rekognition service card
        - Verify URL contains "rekognition" after page loads

        Step 2: Configuration
        Configure Rekognition with these settings:
        - Region: {full_config['region']}
        - Analysis Type: {full_config['analysis_type']}
        - Images per month: {full_config['images_per_month']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm Rekognition appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 100
    
    def get_complexity_score(self) -> int:
        return 5  # Medium complexity

class TextractServiceHandler(BaseServiceHandler):
    """Handler for Amazon Textract service"""
    
    def get_service_name(self) -> str:
        return "Amazon Textract"
    
    def get_search_terms(self) -> List[str]:
        return ["Textract", "Amazon Textract", "Document Analysis"]
    
    def get_service_category(self) -> str:
        return "ml"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "pages_per_month": "1000",
            "analysis_type": "Text Detection",
            "region": "US East (N. Virginia)"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        pages = config.get("pages_per_month", "1000")
        try:
            page_val = int(pages)
            if page_val < 1:
                errors.append("Textract: pages_per_month must be positive")
        except (ValueError, TypeError):
            errors.append("Textract: pages_per_month must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        📄 ADD AMAZON TEXTRACT SERVICE:

        Step 1: Service Selection
        - Search for "Textract" in the service search box
        - Look for "Amazon Textract" service card (Document Analysis)
        - Click "Configure" button on the Amazon Textract service card
        - Verify URL contains "textract" after page loads

        Step 2: Configuration
        Configure Textract with these settings:
        - Region: {full_config['region']}
        - Analysis Type: {full_config['analysis_type']}
        - Pages per month: {full_config['pages_per_month']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm Textract appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 100
    
    def get_complexity_score(self) -> int:
        return 5  # Medium complexity

# Register all AI/ML services
service_registry.register_service("bedrock", BedrockServiceHandler())
service_registry.register_service("comprehend", ComprehendServiceHandler())
service_registry.register_service("rekognition", RekognitionServiceHandler())
service_registry.register_service("textract", TextractServiceHandler())

logger.info("✅ AI/ML services registered: Bedrock, Comprehend, Rekognition, Textract")
