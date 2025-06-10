# Predefined AWS service templates
from typing import Dict, Any

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
            "instance_type": "t3.large",
            "quantity": 2,
            "operating_system": "Linux",
            "storage_type": "gp3",
            "storage_size": "50",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)"
        },
        "database_server": {
            "instance_type": "r5.xlarge",
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
            "storage_size": "20",
            "storage_unit": "GB",
            "backup_retention": "7",
            "region": "US East (N. Virginia)"
        },
        "postgresql": {
            "engine": "PostgreSQL",
            "instance_class": "db.t3.small",
            "deployment": "Single-AZ",
            "storage_type": "gp3",
            "storage_size": "100",
            "storage_unit": "GB",
            "backup_retention": "7",
            "region": "US East (N. Virginia)"
        },
        "production": {
            "engine": "MySQL",
            "instance_class": "db.r5.large",
            "deployment": "Multi-AZ",
            "storage_type": "gp3",
            "storage_size": "500",
            "storage_unit": "GB",
            "backup_retention": "30",
            "region": "US East (N. Virginia)"
        }
    },
    "s3": {
        "default": {
            "storage_class": "S3 Standard",
            "storage_amount": "100",
            "storage_unit": "GB",
            "requests_get": "10000",
            "requests_put": "1000",
            "data_transfer_out": "10",
            "region": "US East (N. Virginia)"
        },
        "backup": {
            "storage_class": "S3 Intelligent-Tiering",
            "storage_amount": "1",
            "storage_unit": "TB",
            "requests_get": "1000",
            "requests_put": "100",
            "data_transfer_out": "50",
            "region": "US East (N. Virginia)"
        }
    },
    "vpc": {
        "default": {
            "nat_gateway": 1,
            "data_processing": "1",
            "data_processing_unit": "GB",
            "region": "US East (N. Virginia)"
        }
    },
    "load_balancer": {
        "default": {
            "type": "Application Load Balancer",
            "capacity_units": "1",
            "data_processed": "1",
            "data_processed_unit": "GB",
            "region": "US East (N. Virginia)"
        }
    }
}

# Infrastructure templates combining multiple services
INFRASTRUCTURE_TEMPLATES = {
    "basic_web_app": {
        "description": "Basic web application với load balancer và database",
        "services": {
            "ec2": PREDEFINED_TEMPLATES["ec2"]["web_server"],
            "rds": PREDEFINED_TEMPLATES["rds"]["default"],
            "s3": PREDEFINED_TEMPLATES["s3"]["default"],
            "load_balancer": PREDEFINED_TEMPLATES["load_balancer"]["default"],
            "vpc": PREDEFINED_TEMPLATES["vpc"]["default"]
        }
    },
    "enterprise_app": {
        "description": "Enterprise application với high availability",
        "services": {
            "ec2": {
                **PREDEFINED_TEMPLATES["ec2"]["web_server"],
                "quantity": 4
            },
            "rds": PREDEFINED_TEMPLATES["rds"]["production"],
            "s3": PREDEFINED_TEMPLATES["s3"]["backup"],
            "load_balancer": PREDEFINED_TEMPLATES["load_balancer"]["default"],
            "vpc": PREDEFINED_TEMPLATES["vpc"]["default"]
        }
    }
}

def get_service_template(service_type: str, template_name: str = "default") -> Dict[str, Any]:
    """Lấy template cho service cụ thể"""
    if service_type in PREDEFINED_TEMPLATES:
        return PREDEFINED_TEMPLATES[service_type].get(template_name, PREDEFINED_TEMPLATES[service_type]["default"])
    return {}

def get_infrastructure_template(template_name: str) -> Dict[str, Any]:
    """Lấy infrastructure template"""
    return INFRASTRUCTURE_TEMPLATES.get(template_name, {}) 