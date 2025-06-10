"""
EC2 Service Module

Specialized handling for Amazon EC2 service configuration and automation.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class EC2Configuration:
    """EC2 service configuration"""
    instance_type: str = "t3.medium"
    quantity: int = 1
    operating_system: str = "Linux"
    region: str = "US East (N. Virginia)"
    storage_type: str = "gp3"
    storage_size: str = "20"
    storage_unit: str = "GB"
    tenancy: str = "Shared"
    pricing_model: str = "On-Demand"
    
    def validate(self) -> List[str]:
        """Validate EC2 configuration"""
        errors = []
        
        if not self.instance_type:
            errors.append("Instance type is required")
        
        if self.quantity < 1:
            errors.append("Quantity must be at least 1")
        
        if not self.operating_system:
            errors.append("Operating system is required")
        
        try:
            storage_size = int(self.storage_size)
            if storage_size < 8:
                errors.append("Storage size must be at least 8 GB")
        except ValueError:
            errors.append("Storage size must be a valid number")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "instance_type": self.instance_type,
            "quantity": self.quantity,
            "operating_system": self.operating_system,
            "region": self.region,
            "storage_type": self.storage_type,
            "storage_size": self.storage_size,
            "storage_unit": self.storage_unit,
            "tenancy": self.tenancy,
            "pricing_model": self.pricing_model
        }

class EC2ServiceHandler:
    """Handles EC2-specific operations and validations"""
    
    # Common EC2 instance types with their characteristics
    INSTANCE_TYPES = {
        "t3.nano": {"vcpu": 2, "memory": 0.5, "category": "burstable"},
        "t3.micro": {"vcpu": 2, "memory": 1, "category": "burstable"},
        "t3.small": {"vcpu": 2, "memory": 2, "category": "burstable"},
        "t3.medium": {"vcpu": 2, "memory": 4, "category": "burstable"},
        "t3.large": {"vcpu": 2, "memory": 8, "category": "burstable"},
        "t3.xlarge": {"vcpu": 4, "memory": 16, "category": "burstable"},
        "m5.large": {"vcpu": 2, "memory": 8, "category": "general"},
        "m5.xlarge": {"vcpu": 4, "memory": 16, "category": "general"},
        "c5.large": {"vcpu": 2, "memory": 4, "category": "compute"},
        "c5.xlarge": {"vcpu": 4, "memory": 8, "category": "compute"},
        "r5.large": {"vcpu": 2, "memory": 16, "category": "memory"},
        "r5.xlarge": {"vcpu": 4, "memory": 32, "category": "memory"}
    }
    
    OPERATING_SYSTEMS = [
        "Linux",
        "Windows",
        "Red Hat Enterprise Linux",
        "SUSE Linux Enterprise Server",
        "Ubuntu Pro"
    ]
    
    STORAGE_TYPES = [
        "gp3",
        "gp2", 
        "io1",
        "io2",
        "st1",
        "sc1"
    ]
    
    @classmethod
    def create_configuration(cls, config_dict: Dict[str, Any]) -> EC2Configuration:
        """Create EC2Configuration from dictionary"""
        return EC2Configuration(
            instance_type=config_dict.get("instance_type", "t3.medium"),
            quantity=config_dict.get("quantity", 1),
            operating_system=config_dict.get("operating_system", "Linux"),
            region=config_dict.get("region", "US East (N. Virginia)"),
            storage_type=config_dict.get("storage_type", "gp3"),
            storage_size=str(config_dict.get("storage_size", "20")),
            storage_unit=config_dict.get("storage_unit", "GB"),
            tenancy=config_dict.get("tenancy", "Shared"),
            pricing_model=config_dict.get("pricing_model", "On-Demand")
        )
    
    @classmethod
    def validate_instance_type(cls, instance_type: str) -> bool:
        """Validate if instance type is supported"""
        return instance_type in cls.INSTANCE_TYPES
    
    @classmethod
    def get_instance_info(cls, instance_type: str) -> Optional[Dict[str, Any]]:
        """Get information about an instance type"""
        return cls.INSTANCE_TYPES.get(instance_type)
    
    @classmethod
    def suggest_instance_type(cls, requirements: Dict[str, Any]) -> str:
        """Suggest instance type based on requirements"""
        vcpu_needed = requirements.get("vcpu", 2)
        memory_needed = requirements.get("memory", 4)
        category = requirements.get("category", "general")
        
        # Find suitable instance types
        suitable_types = []
        for instance_type, specs in cls.INSTANCE_TYPES.items():
            if (specs["vcpu"] >= vcpu_needed and 
                specs["memory"] >= memory_needed):
                if category == "any" or specs["category"] == category:
                    suitable_types.append(instance_type)
        
        # Return the smallest suitable instance type
        if suitable_types:
            return min(suitable_types, key=lambda x: (
                cls.INSTANCE_TYPES[x]["vcpu"], 
                cls.INSTANCE_TYPES[x]["memory"]
            ))
        
        # Default fallback
        return "t3.medium"
    
    @classmethod
    def get_browser_automation_pattern(cls, config: EC2Configuration) -> str:
        """Get EC2-specific browser automation pattern"""
        return f"""
        EC2 Service Configuration Pattern:
        
        SEARCH PHASE:
        1. Search for "EC2" or "Amazon EC2" in service search
        2. Click "Configure" on Amazon EC2 service card
        3. Wait for EC2 configuration page to load
        
        CONFIGURATION PHASE:
        1. Region Selection:
           - Look for region dropdown
           - Select: {config.region}
        
        2. Operating System:
           - Find OS selection (radio buttons or dropdown)
           - Select: {config.operating_system}
        
        3. Instance Configuration:
           - Instance Type dropdown: {config.instance_type}
           - Quantity field: {config.quantity}
           - Tenancy: {config.tenancy} (usually default)
        
        4. Pricing Model:
           - Look for "Workload" or "Pricing" section
           - Select: {config.pricing_model}
        
        5. Storage Configuration:
           - Scroll down to storage section
           - Storage Type: {config.storage_type}
           - Storage Size: {config.storage_size} {config.storage_unit}
        
        COMPLETION PHASE:
        1. Scroll to bottom of configuration
        2. Click "Save and add service" or "Add to estimate"
        3. Wait for confirmation
        
        IMPORTANT EC2-SPECIFIC NOTES:
        - Instance type dropdown may be large - use search within dropdown
        - Storage configuration is usually in a separate section
        - Pricing model may be under "Workload" section
        - Some configurations may require scrolling to find
        """
    
    @classmethod
    def get_validation_checklist(cls, config: EC2Configuration) -> List[str]:
        """Get validation checklist for EC2 configuration"""
        return [
            f"Instance type '{config.instance_type}' is selected",
            f"Quantity is set to {config.quantity}",
            f"Operating system '{config.operating_system}' is selected",
            f"Region '{config.region}' is selected",
            f"Storage type '{config.storage_type}' is configured",
            f"Storage size '{config.storage_size} {config.storage_unit}' is set",
            f"Pricing model '{config.pricing_model}' is selected",
            "No validation errors are displayed",
            "All required fields are filled"
        ]
    
    @classmethod
    def estimate_monthly_cost(cls, config: EC2Configuration) -> Dict[str, Any]:
        """Rough estimate of monthly cost (for reference only)"""
        # This is a very rough estimate for reference
        # Actual pricing should come from AWS Calculator
        
        base_costs = {
            "t3.nano": 3.80,
            "t3.micro": 7.59,
            "t3.small": 15.18,
            "t3.medium": 30.37,
            "t3.large": 60.74,
            "t3.xlarge": 121.47,
            "m5.large": 70.08,
            "m5.xlarge": 140.16,
            "c5.large": 62.78,
            "c5.xlarge": 125.55,
            "r5.large": 91.25,
            "r5.xlarge": 182.50
        }
        
        base_cost = base_costs.get(config.instance_type, 30.37)  # Default to t3.medium
        
        # Adjust for quantity
        total_compute_cost = base_cost * config.quantity
        
        # Rough storage cost (gp3 ~$0.08/GB/month)
        storage_cost = float(config.storage_size) * 0.08 * config.quantity
        
        # OS adjustment
        os_multiplier = 1.0
        if "Windows" in config.operating_system:
            os_multiplier = 1.5  # Windows licensing
        elif "Red Hat" in config.operating_system:
            os_multiplier = 1.3
        
        total_cost = (total_compute_cost * os_multiplier) + storage_cost
        
        return {
            "estimated_monthly_cost": round(total_cost, 2),
            "compute_cost": round(total_compute_cost * os_multiplier, 2),
            "storage_cost": round(storage_cost, 2),
            "currency": "USD",
            "note": "This is a rough estimate. Use AWS Calculator for accurate pricing."
        }
