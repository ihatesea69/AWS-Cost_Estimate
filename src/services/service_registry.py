"""
AWS Service Registry - Service-Oriented Architecture

This module implements a registry pattern for AWS services, allowing easy
addition of new services without modifying core browser agent code.
"""

from typing import Dict, Any, List, Type, Optional
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseServiceHandler(ABC):
    """Base class for all AWS service handlers"""
    
    def __init__(self):
        self.service_name = self.get_service_name()
        self.search_terms = self.get_search_terms()
        self.category = self.get_service_category()
    
    @abstractmethod
    def get_service_name(self) -> str:
        """Return the official AWS service name"""
        pass
    
    @abstractmethod
    def get_search_terms(self) -> List[str]:
        """Return search terms for finding the service in AWS Calculator"""
        pass
    
    @abstractmethod
    def get_service_category(self) -> str:
        """Return service category (compute, storage, database, etc.)"""
        pass
    
    @abstractmethod
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        """Generate browser automation instructions for this service"""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """Validate service configuration and return list of errors"""
        pass
    
    @abstractmethod
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration for this service"""
        pass
    
    def get_timeout_seconds(self) -> int:
        """Return recommended timeout for this service (can be overridden)"""
        return 120  # Default 2 minutes
    
    def get_complexity_score(self) -> int:
        """Return complexity score 1-10 for workflow planning"""
        return 5  # Default medium complexity

class ServiceRegistry:
    """Registry for managing AWS service handlers"""
    
    def __init__(self):
        self._services: Dict[str, BaseServiceHandler] = {}
        self._categories: Dict[str, List[str]] = {}
        logger.info("🏗️ ServiceRegistry initialized")
    
    def register_service(self, service_type: str, handler: BaseServiceHandler):
        """Register a new service handler"""
        self._services[service_type] = handler
        
        # Update category mapping
        category = handler.get_service_category()
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(service_type)
        
        logger.info(f"✅ Registered service: {service_type} ({handler.get_service_name()})")
    
    def get_handler(self, service_type: str) -> Optional[BaseServiceHandler]:
        """Get handler for a service type"""
        return self._services.get(service_type)
    
    def get_all_services(self) -> List[str]:
        """Get list of all registered service types"""
        return list(self._services.keys())
    
    def get_services_by_category(self, category: str) -> List[str]:
        """Get services in a specific category"""
        return self._categories.get(category, [])
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return list(self._categories.keys())
    
    def validate_service_config(self, service_type: str, config: Dict[str, Any]) -> List[str]:
        """Validate configuration for a service"""
        handler = self.get_handler(service_type)
        if not handler:
            return [f"Unknown service type: {service_type}"]
        
        return handler.validate_config(config)
    
    def get_service_instructions(self, service_type: str, config: Dict[str, Any]) -> str:
        """Get browser instructions for a service"""
        handler = self.get_handler(service_type)
        if not handler:
            raise ValueError(f"Unknown service type: {service_type}")
        
        return handler.get_service_instructions(config)
    
    def get_workflow_plan(self, services: List[str]) -> Dict[str, Any]:
        """Generate optimized workflow plan for multiple services"""
        plan = {
            "services": services,
            "total_estimated_time": 0,
            "complexity_score": 0,
            "service_order": [],
            "category_groups": {}
        }
        
        # Group by category for better workflow organization
        for service_type in services:
            handler = self.get_handler(service_type)
            if handler:
                category = handler.get_service_category()
                if category not in plan["category_groups"]:
                    plan["category_groups"][category] = []
                plan["category_groups"][category].append(service_type)
                
                plan["total_estimated_time"] += handler.get_timeout_seconds()
                plan["complexity_score"] += handler.get_complexity_score()
        
        # Optimize service order (infrastructure first, then applications)
        priority_order = ["networking", "compute", "storage", "database", "analytics", "ml", "security"]
        
        ordered_services = []
        for category in priority_order:
            if category in plan["category_groups"]:
                ordered_services.extend(plan["category_groups"][category])
        
        # Add any remaining services not in priority categories
        for service in services:
            if service not in ordered_services:
                ordered_services.append(service)
        
        plan["service_order"] = ordered_services
        plan["average_complexity"] = plan["complexity_score"] / len(services) if services else 0
        
        return plan

# Global registry instance
service_registry = ServiceRegistry()

def register_service(service_type: str, handler_class: Type[BaseServiceHandler]):
    """Decorator for registering service handlers"""
    def decorator(cls):
        handler = handler_class()
        service_registry.register_service(service_type, handler)
        return cls
    return decorator

def get_service_registry() -> ServiceRegistry:
    """Get the global service registry"""
    return service_registry
