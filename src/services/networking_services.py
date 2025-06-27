"""
Networking Services Handlers - VPC, CloudFront, API Gateway, etc.

This module contains handlers for AWS networking services following the
service-oriented architecture pattern.
"""

from typing import Dict, Any, List
from .service_registry import BaseServiceHandler, service_registry
import logging

logger = logging.getLogger(__name__)

class VPCServiceHandler(BaseServiceHandler):
    """Handler for Amazon VPC service"""
    
    def get_service_name(self) -> str:
        return "Amazon VPC"
    
    def get_search_terms(self) -> List[str]:
        return ["VPC", "Amazon VPC", "Virtual Private Cloud"]
    
    def get_service_category(self) -> str:
        return "networking"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "nat_gateways": "1",
            "vpn_connections": "0",
            "data_transfer": "10",
            "data_transfer_unit": "GB",
            "region": "US East (N. Virginia)"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        nat_gw = config.get("nat_gateways", "1")
        try:
            nat_val = int(nat_gw)
            if nat_val < 0:
                errors.append("VPC: nat_gateways must be non-negative")
        except (ValueError, TypeError):
            errors.append("VPC: nat_gateways must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        🌐 ADD AMAZON VPC SERVICE:

        Step 1: Service Selection
        - Search for "VPC" in the service search box
        - Look for "Amazon VPC" service card (Virtual Private Cloud)
        - Click "Configure" button on the Amazon VPC service card
        - Verify URL contains "vpc" after page loads

        Step 2: Configuration
        Configure VPC with these settings:
        - Region: {full_config['region']}
        - NAT Gateways: {full_config['nat_gateways']}
        - VPN Connections: {full_config['vpn_connections']}
        - Data Transfer: {full_config['data_transfer']} {full_config['data_transfer_unit']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm VPC appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 100
    
    def get_complexity_score(self) -> int:
        return 4  # Medium complexity

class CloudFrontServiceHandler(BaseServiceHandler):
    """Handler for Amazon CloudFront service"""
    
    def get_service_name(self) -> str:
        return "Amazon CloudFront"
    
    def get_search_terms(self) -> List[str]:
        return ["CloudFront", "Amazon CloudFront", "CDN"]
    
    def get_service_category(self) -> str:
        return "networking"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "data_transfer": "100",
            "data_transfer_unit": "GB",
            "requests": "1000000",
            "origin_requests": "100000",
            "region": "US East (N. Virginia)"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        data_transfer = config.get("data_transfer", "100")
        try:
            transfer_val = int(data_transfer)
            if transfer_val < 0:
                errors.append("CloudFront: data_transfer must be non-negative")
        except (ValueError, TypeError):
            errors.append("CloudFront: data_transfer must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        🌍 ADD AMAZON CLOUDFRONT SERVICE:

        Step 1: Service Selection
        - Search for "CloudFront" in the service search box
        - Look for "Amazon CloudFront" service card (Content Delivery Network)
        - Click "Configure" button on the Amazon CloudFront service card
        - Verify URL contains "cloudfront" after page loads

        Step 2: Configuration
        Configure CloudFront with these settings:
        - Region: {full_config['region']}
        - Data Transfer Out: {full_config['data_transfer']} {full_config['data_transfer_unit']}
        - HTTP/HTTPS Requests: {full_config['requests']}
        - Origin Requests: {full_config['origin_requests']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm CloudFront appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 110
    
    def get_complexity_score(self) -> int:
        return 5  # Medium complexity

class LoadBalancerServiceHandler(BaseServiceHandler):
    """Handler for Elastic Load Balancer service"""
    
    def get_service_name(self) -> str:
        return "Elastic Load Balancing"
    
    def get_search_terms(self) -> List[str]:
        return ["Load Balancer", "ELB", "Application Load Balancer", "Network Load Balancer"]
    
    def get_service_category(self) -> str:
        return "networking"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "load_balancer_type": "Application Load Balancer",
            "number_of_load_balancers": "1",
            "processed_bytes": "1",
            "processed_bytes_unit": "GB",
            "region": "US East (N. Virginia)"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        num_lb = config.get("number_of_load_balancers", "1")
        try:
            lb_val = int(num_lb)
            if lb_val < 1:
                errors.append("Load Balancer: number_of_load_balancers must be at least 1")
        except (ValueError, TypeError):
            errors.append("Load Balancer: number_of_load_balancers must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        ⚖️ ADD ELASTIC LOAD BALANCING SERVICE:

        Step 1: Service Selection
        - Search for "Load Balancer" in the service search box
        - Look for "Elastic Load Balancing" service card
        - Click "Configure" button on the Elastic Load Balancing service card
        - Verify URL contains "elb" or "load" after page loads

        Step 2: Configuration
        Configure Load Balancer with these settings:
        - Region: {full_config['region']}
        - Load Balancer Type: {full_config['load_balancer_type']}
        - Number of Load Balancers: {full_config['number_of_load_balancers']}
        - Processed Bytes: {full_config['processed_bytes']} {full_config['processed_bytes_unit']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm Load Balancer appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 120
    
    def get_complexity_score(self) -> int:
        return 6  # Medium-high complexity

# Register all networking services
service_registry.register_service("vpc", VPCServiceHandler())
service_registry.register_service("cloudfront", CloudFrontServiceHandler())
service_registry.register_service("load_balancer", LoadBalancerServiceHandler())

logger.info("✅ Networking services registered: VPC, CloudFront, Load Balancer")
