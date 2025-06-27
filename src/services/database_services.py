"""
Database Services Handlers - RDS, DynamoDB, ElastiCache, etc.

This module contains handlers for AWS database services following the
service-oriented architecture pattern.
"""

from typing import Dict, Any, List
from .service_registry import BaseServiceHandler, service_registry
import logging

logger = logging.getLogger(__name__)

class RDSServiceHandler(BaseServiceHandler):
    """Handler for Amazon RDS service"""
    
    def get_service_name(self) -> str:
        return "Amazon RDS"
    
    def get_search_terms(self) -> List[str]:
        return ["RDS", "Amazon RDS", "Relational Database"]
    
    def get_service_category(self) -> str:
        return "database"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "engine": "MySQL",
            "instance_class": "db.t3.micro",
            "storage_type": "gp2",
            "allocated_storage": "20",
            "storage_unit": "GB",
            "multi_az": "No",
            "region": "US East (N. Virginia)"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        if not config.get("engine"):
            errors.append("RDS: engine is required")
        
        if not config.get("instance_class"):
            errors.append("RDS: instance_class is required")
        
        storage = config.get("allocated_storage", "20")
        try:
            storage_val = int(storage)
            if storage_val < 20:
                errors.append("RDS: allocated_storage must be at least 20 GB")
        except (ValueError, TypeError):
            errors.append("RDS: allocated_storage must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        🗄️ ADD AMAZON RDS SERVICE:

        Step 1: Service Selection
        - Search for "RDS" in the service search box
        - Look for "Amazon RDS" service card (Managed Relational Database)
        - Click "Configure" button on the Amazon RDS service card
        - Verify URL contains "rds" after page loads

        Step 2: Configuration
        Configure RDS with these settings:
        - Region: {full_config['region']}
        - Database Engine: {full_config['engine']}
        - Instance Class: {full_config['instance_class']}
        - Storage Type: {full_config['storage_type']}
        - Allocated Storage: {full_config['allocated_storage']} {full_config['storage_unit']}
        - Multi-AZ: {full_config['multi_az']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm RDS appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 140  # Database services can be complex
    
    def get_complexity_score(self) -> int:
        return 7  # High complexity due to many database options

class DynamoDBServiceHandler(BaseServiceHandler):
    """Handler for Amazon DynamoDB service"""
    
    def get_service_name(self) -> str:
        return "Amazon DynamoDB"
    
    def get_search_terms(self) -> List[str]:
        return ["DynamoDB", "Amazon DynamoDB", "NoSQL"]
    
    def get_service_category(self) -> str:
        return "database"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "read_capacity": "5",
            "write_capacity": "5",
            "storage_size": "1",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        read_cap = config.get("read_capacity", "5")
        try:
            read_val = int(read_cap)
            if read_val < 1:
                errors.append("DynamoDB: read_capacity must be at least 1")
        except (ValueError, TypeError):
            errors.append("DynamoDB: read_capacity must be a valid number")
        
        write_cap = config.get("write_capacity", "5")
        try:
            write_val = int(write_cap)
            if write_val < 1:
                errors.append("DynamoDB: write_capacity must be at least 1")
        except (ValueError, TypeError):
            errors.append("DynamoDB: write_capacity must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        📊 ADD AMAZON DYNAMODB SERVICE:

        Step 1: Service Selection
        - Search for "DynamoDB" in the service search box
        - Look for "Amazon DynamoDB" service card (NoSQL Database)
        - Click "Configure" button on the Amazon DynamoDB service card
        - Verify URL contains "dynamodb" after page loads

        Step 2: Configuration
        Configure DynamoDB with these settings:
        - Region: {full_config['region']}
        - Read Capacity Units: {full_config['read_capacity']}
        - Write Capacity Units: {full_config['write_capacity']}
        - Data Storage: {full_config['storage_size']} {full_config['storage_unit']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm DynamoDB appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 120
    
    def get_complexity_score(self) -> int:
        return 6  # Medium-high complexity

# Register all database services
service_registry.register_service("rds", RDSServiceHandler())
service_registry.register_service("dynamodb", DynamoDBServiceHandler())

logger.info("✅ Database services registered: RDS, DynamoDB")
