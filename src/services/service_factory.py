"""
Service Factory - Easy Service Creation and Registration

This module provides utilities for easily creating and registering new AWS services
following the service-oriented architecture pattern.
"""

from typing import Dict, Any, List, Type, Optional
from .service_registry import BaseServiceHandler, service_registry
import logging

logger = logging.getLogger(__name__)

class ServiceTemplate:
    """Template for creating new service handlers quickly"""
    
    @staticmethod
    def create_basic_service(
        service_name: str,
        service_type: str,
        search_terms: List[str],
        category: str,
        default_config: Dict[str, Any],
        config_fields: List[Dict[str, Any]],
        complexity_score: int = 5,
        timeout_seconds: int = 120
    ) -> Type[BaseServiceHandler]:
        """
        Create a basic service handler class dynamically
        
        Args:
            service_name: Official AWS service name (e.g., "Amazon DynamoDB")
            service_type: Service type key (e.g., "dynamodb")
            search_terms: List of search terms for finding the service
            category: Service category (compute, storage, database, etc.)
            default_config: Default configuration dictionary
            config_fields: List of required config fields with validation
            complexity_score: Complexity score 1-10
            timeout_seconds: Recommended timeout
        """
        
        class DynamicServiceHandler(BaseServiceHandler):
            def get_service_name(self) -> str:
                return service_name
            
            def get_search_terms(self) -> List[str]:
                return search_terms
            
            def get_service_category(self) -> str:
                return category
            
            def get_default_config(self) -> Dict[str, Any]:
                return default_config.copy()
            
            def validate_config(self, config: Dict[str, Any]) -> List[str]:
                errors = []
                
                for field in config_fields:
                    field_name = field['name']
                    field_type = field.get('type', 'str')
                    required = field.get('required', True)
                    min_value = field.get('min_value')
                    max_value = field.get('max_value')
                    
                    value = config.get(field_name)
                    
                    if required and not value:
                        errors.append(f"{service_name}: {field_name} is required")
                        continue
                    
                    if value is not None:
                        # Type validation
                        if field_type == 'int':
                            try:
                                int_val = int(value)
                                if min_value is not None and int_val < min_value:
                                    errors.append(f"{service_name}: {field_name} must be at least {min_value}")
                                if max_value is not None and int_val > max_value:
                                    errors.append(f"{service_name}: {field_name} must be at most {max_value}")
                            except (ValueError, TypeError):
                                errors.append(f"{service_name}: {field_name} must be a valid number")
                        
                        elif field_type == 'float':
                            try:
                                float_val = float(value)
                                if min_value is not None and float_val < min_value:
                                    errors.append(f"{service_name}: {field_name} must be at least {min_value}")
                                if max_value is not None and float_val > max_value:
                                    errors.append(f"{service_name}: {field_name} must be at most {max_value}")
                            except (ValueError, TypeError):
                                errors.append(f"{service_name}: {field_name} must be a valid number")
                
                return errors
            
            def get_service_instructions(self, config: Dict[str, Any]) -> str:
                # Merge with defaults
                full_config = {**self.get_default_config(), **config}
                
                # Build configuration text
                config_text = []
                for key, value in full_config.items():
                    if key != 'region':  # Region is usually first
                        display_key = key.replace('_', ' ').title()
                        config_text.append(f"        - {display_key}: {value}")
                
                config_section = '\n'.join(config_text)
                
                return f"""
        🔧 ADD {service_name.upper()} SERVICE:

        Step 1: Service Selection
        - Search for "{search_terms[0]}" in the service search box
        - Look for "{service_name}" service card
        - Click "Configure" button on the {service_name} service card
        - Verify URL contains "{service_type}" after page loads

        Step 2: Configuration
        Configure {service_name} with these settings:
        - Region: {full_config.get('region', 'US East (N. Virginia)')}
{config_section}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm {service_name} appears in estimate summary
        """
            
            def get_timeout_seconds(self) -> int:
                return timeout_seconds
            
            def get_complexity_score(self) -> int:
                return complexity_score
        
        # Set class name for better debugging
        DynamicServiceHandler.__name__ = f"{service_type.title()}ServiceHandler"
        DynamicServiceHandler.__qualname__ = f"{service_type.title()}ServiceHandler"
        
        return DynamicServiceHandler

def register_service_from_config(config: Dict[str, Any]) -> bool:
    """
    Register a service from configuration dictionary
    
    Example config:
    {
        "service_name": "Amazon DynamoDB",
        "service_type": "dynamodb",
        "search_terms": ["DynamoDB", "Amazon DynamoDB"],
        "category": "database",
        "default_config": {
            "table_name": "MyTable",
            "read_capacity": "5",
            "write_capacity": "5",
            "region": "US East (N. Virginia)"
        },
        "config_fields": [
            {"name": "read_capacity", "type": "int", "required": True, "min_value": 1},
            {"name": "write_capacity", "type": "int", "required": True, "min_value": 1}
        ],
        "complexity_score": 6,
        "timeout_seconds": 130
    }
    """
    try:
        required_fields = ['service_name', 'service_type', 'search_terms', 'category', 'default_config']
        
        for field in required_fields:
            if field not in config:
                logger.error(f"❌ Missing required field: {field}")
                return False
        
        # Create service handler class
        handler_class = ServiceTemplate.create_basic_service(
            service_name=config['service_name'],
            service_type=config['service_type'],
            search_terms=config['search_terms'],
            category=config['category'],
            default_config=config['default_config'],
            config_fields=config.get('config_fields', []),
            complexity_score=config.get('complexity_score', 5),
            timeout_seconds=config.get('timeout_seconds', 120)
        )
        
        # Register the service
        handler = handler_class()
        service_registry.register_service(config['service_type'], handler)
        
        logger.info(f"✅ Service registered from config: {config['service_type']}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to register service from config: {e}")
        return False

def bulk_register_services(services_config: List[Dict[str, Any]]) -> Dict[str, bool]:
    """Register multiple services from configuration list"""
    results = {}
    
    for config in services_config:
        service_type = config.get('service_type', 'unknown')
        results[service_type] = register_service_from_config(config)
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    logger.info(f"📊 Bulk registration completed: {successful}/{total} services registered")
    
    return results

# Predefined service configurations for easy registration
PREDEFINED_SERVICES = {
    "dynamodb": {
        "service_name": "Amazon DynamoDB",
        "service_type": "dynamodb",
        "search_terms": ["DynamoDB", "Amazon DynamoDB", "NoSQL Database"],
        "category": "database",
        "default_config": {
            "read_capacity": "5",
            "write_capacity": "5",
            "storage_size": "1",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)"
        },
        "config_fields": [
            {"name": "read_capacity", "type": "int", "required": True, "min_value": 1},
            {"name": "write_capacity", "type": "int", "required": True, "min_value": 1},
            {"name": "storage_size", "type": "int", "required": True, "min_value": 1}
        ],
        "complexity_score": 6,
        "timeout_seconds": 130
    },
    
    "cloudfront": {
        "service_name": "Amazon CloudFront",
        "service_type": "cloudfront",
        "search_terms": ["CloudFront", "Amazon CloudFront", "CDN"],
        "category": "networking",
        "default_config": {
            "data_transfer": "100",
            "data_transfer_unit": "GB",
            "requests": "1000000",
            "region": "US East (N. Virginia)"
        },
        "config_fields": [
            {"name": "data_transfer", "type": "int", "required": True, "min_value": 1},
            {"name": "requests", "type": "int", "required": True, "min_value": 1}
        ],
        "complexity_score": 4,
        "timeout_seconds": 100
    },
    
    "apigateway": {
        "service_name": "Amazon API Gateway",
        "service_type": "apigateway",
        "search_terms": ["API Gateway", "Amazon API Gateway"],
        "category": "networking",
        "default_config": {
            "requests_per_month": "1000000",
            "data_transfer": "1",
            "data_transfer_unit": "GB",
            "region": "US East (N. Virginia)"
        },
        "config_fields": [
            {"name": "requests_per_month", "type": "int", "required": True, "min_value": 1},
            {"name": "data_transfer", "type": "int", "required": True, "min_value": 1}
        ],
        "complexity_score": 5,
        "timeout_seconds": 110
    }
}

def register_predefined_services(service_names: Optional[List[str]] = None) -> Dict[str, bool]:
    """Register predefined services"""
    if service_names is None:
        service_names = list(PREDEFINED_SERVICES.keys())
    
    configs = [PREDEFINED_SERVICES[name] for name in service_names if name in PREDEFINED_SERVICES]
    return bulk_register_services(configs)

# Auto-register some common services
if __name__ != "__main__":
    # Register predefined services when module is imported
    register_predefined_services(["dynamodb", "cloudfront", "apigateway"])
    logger.info("🚀 Predefined services auto-registered")
