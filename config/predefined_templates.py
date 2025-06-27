"""
Predefined Templates for AWS Services
Chứa các template mặc định cho AWS services và infrastructure patterns
"""

from typing import Dict, Any


# PREDEFINED TEMPLATES cho từng AWS service
PREDEFINED_TEMPLATES = {
    "ec2": {
        "default": {
            "instance_type": "t3.medium",
            "quantity": 1,
            "operating_system": "Linux",
            "storage_type": "gp3",
            "storage_size": "20",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)"
        },
        "web_server": {
            "instance_type": "t3.medium",
            "quantity": 2,
            "operating_system": "Linux",
            "storage_type": "gp3",
            "storage_size": "30",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)"
        },
        "database_server": {
            "instance_type": "r5.large",
            "quantity": 1,
            "operating_system": "Linux",
            "storage_type": "gp3",
            "storage_size": "100",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)"
        }
    },
    
    "rds": {
        "default": {
            "engine": "MySQL",
            "instance_class": "db.t3.micro",
            "deployment": "Single-AZ",
            "storage_type": "gp3",
            "storage_amount": "20",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)"
        },
        "postgresql": {
            "engine": "PostgreSQL",
            "instance_class": "db.t3.small",
            "deployment": "Single-AZ",
            "storage_type": "gp3",
            "storage_amount": "50",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)"
        },
        "production": {
            "engine": "MySQL",
            "instance_class": "db.r5.large",
            "deployment": "Multi-AZ",
            "storage_type": "gp3",
            "storage_amount": "100",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)"
        }
    },
    
    "s3": {
        "default": {
            "storage_amount": 100,
            "storage_unit": "GB",
            "storage_class": "Standard",
            "region": "US East (N. Virginia)"
        },
        "backup": {
            "storage_amount": 500,
            "storage_unit": "GB",
            "storage_class": "Standard-IA",
            "region": "US East (N. Virginia)"
        }
    },
    
    "vpc": {
        "default": {
            "nat_gateway": True,
            "availability_zones": 2,
            "region": "US East (N. Virginia)"
        }
    },
    
    "load_balancer": {
        "default": {
            "type": "Application Load Balancer",
            "scheme": "Internet-facing",
            "region": "US East (N. Virginia)"
        }
    }
}


# INFRASTRUCTURE TEMPLATES cho các architecture patterns
INFRASTRUCTURE_TEMPLATES = {
    "basic_web_app": {
        "description": "Basic web application với EC2, RDS, và S3 storage",
        "services": {
            "ec2": {
                "instance_type": "t3.medium",
                "quantity": 2,
                "operating_system": "Linux",
                "storage_type": "gp3",
                "storage_size": "20",
                "storage_unit": "GB"
            },
            "rds": {
                "engine": "MySQL",
                "instance_class": "db.t3.small",
                "deployment": "Single-AZ",
                "storage_amount": "50",
                "storage_unit": "GB"
            },
            "s3": {
                "storage_amount": 100,
                "storage_unit": "GB",
                "storage_class": "Standard"
            },
            "load_balancer": {
                "type": "Application Load Balancer",
                "scheme": "Internet-facing"
            }
        }
    },
    
    "enterprise_app": {
        "description": "Enterprise application với high availability và performance",
        "services": {
            "vpc": {
                "nat_gateway": True,
                "availability_zones": 3
            },
            "ec2": {
                "instance_type": "r5.large", 
                "quantity": 4,
                "operating_system": "Linux",
                "storage_type": "gp3",
                "storage_size": "100",
                "storage_unit": "GB"
            },
            "rds": {
                "engine": "PostgreSQL",
                "instance_class": "db.r5.xlarge",
                "deployment": "Multi-AZ",
                "storage_amount": "500",
                "storage_unit": "GB"
            },
            "s3": {
                "storage_amount": 1000,
                "storage_unit": "GB",
                "storage_class": "Standard"
            },
            "load_balancer": {
                "type": "Application Load Balancer",
                "scheme": "Internet-facing"
            }
        }
    }
}


def get_service_template(service_type: str, template_name: str) -> Dict[str, Any]:
    """
    Lấy template configuration cho một service cụ thể
    
    Args:
        service_type: Loại service (ec2, rds, s3, vpc, load_balancer)
        template_name: Tên template (default, web_server, postgresql, etc.)
        
    Returns:
        Dict chứa configuration của template
    """
    if service_type not in PREDEFINED_TEMPLATES:
        return {}
    
    service_templates = PREDEFINED_TEMPLATES[service_type]
    
    if template_name not in service_templates:
        # Fallback to default template
        template_name = "default"
    
    if template_name not in service_templates:
        return {}
    
    # Return a copy to avoid modifying original template
    return service_templates[template_name].copy()


def get_infrastructure_template(template_name: str) -> Dict[str, Any]:
    """
    Lấy infrastructure template cho một architecture pattern
    
    Args:
        template_name: Tên infrastructure template (basic_web_app, enterprise_app)
        
    Returns:
        Dict chứa description và services configuration
    """
    if template_name not in INFRASTRUCTURE_TEMPLATES:
        return {}
    
    # Return a copy to avoid modifying original template
    template = INFRASTRUCTURE_TEMPLATES[template_name].copy()
    
    # Deep copy the services dict
    if 'services' in template:
        template['services'] = {
            service: config.copy() 
            for service, config in template['services'].items()
        }
    
    return template


def get_available_service_templates(service_type: str) -> list:
    """
    Lấy danh sách các template có sẵn cho một service type
    
    Args:
        service_type: Loại service
        
    Returns:
        List các template names
    """
    if service_type not in PREDEFINED_TEMPLATES:
        return []
    
    return list(PREDEFINED_TEMPLATES[service_type].keys())


def get_available_infrastructure_templates() -> list:
    """
    Lấy danh sách các infrastructure templates có sẵn
    
    Returns:
        List các infrastructure template names
    """
    return list(INFRASTRUCTURE_TEMPLATES.keys())


def merge_with_template(service_type: str, user_config: Dict[str, Any], template_name: str = "default") -> Dict[str, Any]:
    """
    Merge user configuration với predefined template
    
    Args:
        service_type: Loại service
        user_config: Configuration từ user
        template_name: Template name để merge (default: "default")
        
    Returns:
        Dict chứa merged configuration
    """
    template = get_service_template(service_type, template_name)
    
    if not template:
        return user_config.copy()
    
    # Template làm base, user config override
    merged = template.copy()
    merged.update(user_config)
    
    return merged 