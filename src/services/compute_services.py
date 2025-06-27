"""
Compute Services Handlers - EC2, Lambda, ECS, etc.

This module contains handlers for AWS compute services following the
service-oriented architecture pattern.
"""

from typing import Dict, Any, List
from .service_registry import BaseServiceHandler, service_registry
import logging

logger = logging.getLogger(__name__)

class EC2ServiceHandler(BaseServiceHandler):
    """Handler for Amazon EC2 service"""
    
    def get_service_name(self) -> str:
        return "Amazon EC2"
    
    def get_search_terms(self) -> List[str]:
        return ["EC2", "Amazon EC2", "Elastic Compute Cloud"]
    
    def get_service_category(self) -> str:
        return "compute"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "instance_type": "t4g.nano",  # Updated to match instructions
            "quantity": 1,
            "operating_system": "Linux",
            "region": "US East (Ohio)",  # Updated to match instructions
            "storage_type": "General Purpose SSD (gp3)",  # Full name as in AWS Calculator
            "storage_size": "30",  # Updated to match instructions
            "storage_unit": "GB",
            "tenancy": "Shared",
            "pricing_model": "On-Demand",
            "utilization": "100",  # Added utilization percentage
            "workload_pattern": "Constant usage",  # Added workload pattern
            "iops": "3000",  # Added IOPS configuration
            "description": "EC2 Instance Estimate"  # Added description
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []

        # Required fields validation
        if not config.get("instance_type"):
            errors.append("EC2: instance_type is required")

        if not config.get("operating_system"):
            errors.append("EC2: operating_system is required")

        if not config.get("region"):
            errors.append("EC2: region is required")

        # Quantity validation
        quantity = config.get("quantity", 1)
        try:
            qty_val = int(quantity)
            if qty_val < 1 or qty_val > 1000:
                errors.append("EC2: quantity must be between 1 and 1000")
        except (ValueError, TypeError):
            errors.append("EC2: quantity must be a valid number")

        # Storage size validation
        storage_size = config.get("storage_size", "30")
        try:
            size = int(storage_size)
            if size < 8:
                errors.append("EC2: storage_size must be at least 8 GB")
            if size > 16384:  # 16 TB limit for most EBS volumes
                errors.append("EC2: storage_size cannot exceed 16,384 GB")
        except (ValueError, TypeError):
            errors.append("EC2: storage_size must be a valid number")

        # Utilization validation
        utilization = config.get("utilization", "100")
        try:
            util_val = int(utilization)
            if util_val < 1 or util_val > 100:
                errors.append("EC2: utilization must be between 1 and 100 percent")
        except (ValueError, TypeError):
            errors.append("EC2: utilization must be a valid number")

        # IOPS validation (if provided)
        iops = config.get("iops")
        if iops:
            try:
                iops_val = int(iops)
                if iops_val < 100 or iops_val > 64000:
                    errors.append("EC2: IOPS must be between 100 and 64,000")
            except (ValueError, TypeError):
                errors.append("EC2: IOPS must be a valid number")

        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        # Merge with defaults
        full_config = {**self.get_default_config(), **config}

        return f"""
        🖥️ AMAZON EC2 DETAILED CONFIGURATION WORKFLOW

        PHASE 1: INITIAL SETUP AND NAVIGATION

        Step 1: Access AWS Pricing Calculator
        - Navigate to https://calculator.aws/
        - Wait for page to fully load
        - Verify AWS Calculator interface is visible

        Step 2: Create New Estimate
        - Look for "Create estimate" button
        - Click "Create estimate" button
        - Wait 2 seconds for page transition

        Step 3: Select Amazon EC2 Service
        - Look for "Amazon EC2" service card or tile
        - Click "Configure" button on Amazon EC2 service
        - Wait 3 seconds for EC2 configuration page to load
        - Verify you are on EC2 configuration page

        PHASE 2: BASIC CONFIGURATION

        Step 4: Fill Description (Optional)
        - Find description input field (placeholder may contain 'description')
        - Clear any existing text
        - Enter: "EC2 Instance Estimate"

        Step 5: Select Region
        - Find region dropdown or selection area
        - Click on region dropdown
        - Select: "{full_config['region']}"
        - Verify region is selected correctly

        Step 6: Configure Tenancy
        - Look for tenancy options (Shared Instances, Dedicated, etc.)
        - Select radio button for: "{full_config['tenancy']}"
        - Verify selection is highlighted/checked

        Step 7: Select Operating System
        - Find operating system selection area
        - Select radio button for: "{full_config['operating_system']}"
        - Verify OS selection is highlighted/checked

        PHASE 3: WORKLOAD AND INSTANCE CONFIGURATION

        Step 8: Choose Workload Pattern
        - Look for workload pattern options
        - Select "Constant usage" or "On-Demand" option
        - Verify workload pattern is selected

        Step 9: Set Number of Instances
        - Find instances number input field
        - Clear existing value
        - Enter: "{full_config['quantity']}"
        - Verify number is entered correctly

        Step 10: Select Instance Type
        - Look for instance type selection area or table
        - Find and click on: "{full_config['instance_type']}"
        - Wait 1 second for selection to register
        - Verify "{full_config['instance_type']}" is selected/highlighted

        PHASE 4: PAYMENT OPTIONS CONFIGURATION

        Step 11: Configure Payment Method
        - Find payment method options
        - Select "{full_config['pricing_model']}" option
        - Verify payment method is selected

        Step 12: Set Expected Utilization
        - Find utilization percentage input field
        - Clear existing value
        - Enter: "100" (for 100% utilization)

        PHASE 5: STORAGE CONFIGURATION (EBS)

        Step 13: Expand EBS Section
        - Look for "Amazon Elastic Block Store" or "EBS" section
        - Click to expand EBS configuration section
        - Wait 1 second for section to expand

        Step 14: Select Storage Type
        - Find storage type dropdown
        - Select: "{full_config['storage_type']}" or "General Purpose SSD (gp3)"
        - Verify storage type is selected

        Step 15: Set Storage Amount
        - Find storage amount input field (may have GB placeholder)
        - Clear existing value
        - Enter: "{full_config['storage_size']}"
        - Verify storage amount is entered

        Step 16: Configure IOPS (if available)
        - Look for IOPS input field
        - If IOPS field exists, enter: "3000"
        - If field doesn't exist, skip this step

        PHASE 6: FINALIZATION

        Step 17: Review Configuration
        - Scroll through all sections to verify settings
        - Check that all required fields are filled
        - Look for any validation errors or warnings

        Step 18: Add to Estimate
        - Scroll to bottom of configuration page
        - Look for "Add to my estimate" or "Save and add service" button
        - Click the button to add EC2 to estimate
        - Wait 3 seconds for confirmation
        - Verify success message or return to main calculator page

        CRITICAL SUCCESS CRITERIA:
        - EC2 service must be added to the estimate successfully
        - All configuration values must be applied correctly
        - No validation errors should be present
        - Must return to main calculator page or show success confirmation

        CONFIGURATION SUMMARY:
        - Region: {full_config['region']}
        - OS: {full_config['operating_system']}
        - Instance Type: {full_config['instance_type']}
        - Quantity: {full_config['quantity']}
        - Tenancy: {full_config['tenancy']}
        - Pricing: {full_config['pricing_model']}
        - Storage: {full_config['storage_size']} {full_config['storage_unit']} {full_config['storage_type']}
        """
    
    def get_timeout_seconds(self) -> int:
        return 180  # EC2 has detailed multi-phase configuration

    def get_complexity_score(self) -> int:
        return 8  # High complexity due to detailed phase-based workflow

class LambdaServiceHandler(BaseServiceHandler):
    """Handler for AWS Lambda service"""
    
    def get_service_name(self) -> str:
        return "AWS Lambda"
    
    def get_search_terms(self) -> List[str]:
        return ["Lambda", "AWS Lambda", "Serverless"]
    
    def get_service_category(self) -> str:
        return "compute"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "memory": "512",
            "memory_unit": "MB",
            "requests_per_month": "1000000",
            "duration_per_request": "100",
            "duration_unit": "ms",
            "region": "US East (N. Virginia)"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        memory = config.get("memory", "512")
        try:
            mem_val = int(memory)
            if mem_val < 128 or mem_val > 10240:
                errors.append("Lambda: memory must be between 128 MB and 10,240 MB")
        except (ValueError, TypeError):
            errors.append("Lambda: memory must be a valid number")
        
        requests = config.get("requests_per_month", "1000000")
        try:
            req_val = int(requests)
            if req_val < 0:
                errors.append("Lambda: requests_per_month must be non-negative")
        except (ValueError, TypeError):
            errors.append("Lambda: requests_per_month must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        ⚡ ADD AWS LAMBDA SERVICE:

        Step 1: Service Selection
        - Search for "Lambda" in the service search box
        - Look for "AWS Lambda" service card (Serverless Computing)
        - Click "Configure" button on the AWS Lambda service card
        - Verify URL contains "lambda" after page loads

        Step 2: Configuration
        Configure Lambda with these settings:
        - Region: {full_config['region']}
        - Memory: {full_config['memory']} {full_config['memory_unit']}
        - Requests per month: {full_config['requests_per_month']}
        - Duration per request: {full_config['duration_per_request']} {full_config['duration_unit']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm Lambda appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 90  # Lambda is simpler to configure
    
    def get_complexity_score(self) -> int:
        return 4  # Medium complexity

class SageMakerServiceHandler(BaseServiceHandler):
    """Handler for Amazon SageMaker service"""
    
    def get_service_name(self) -> str:
        return "Amazon SageMaker"
    
    def get_search_terms(self) -> List[str]:
        return ["SageMaker", "Amazon SageMaker", "Machine Learning"]
    
    def get_service_category(self) -> str:
        return "ml"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "instance_type": "ml.t3.medium",
            "instance_hours": "100",
            "storage_size": "20",
            "storage_unit": "GB",
            "region": "US East (N. Virginia)",
            "workload_type": "Training"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        if not config.get("instance_type"):
            errors.append("SageMaker: instance_type is required")
        
        hours = config.get("instance_hours", "100")
        try:
            hours_val = int(hours)
            if hours_val < 1:
                errors.append("SageMaker: instance_hours must be positive")
        except (ValueError, TypeError):
            errors.append("SageMaker: instance_hours must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        🤖 ADD AMAZON SAGEMAKER SERVICE:

        Step 1: Service Selection
        - Search for "SageMaker" in the service search box
        - Look for "Amazon SageMaker" service card (Machine Learning)
        - Click "Configure" button on the Amazon SageMaker service card
        - Verify URL contains "sagemaker" after page loads

        Step 2: Configuration
        Configure SageMaker with these settings:
        - Region: {full_config['region']}
        - Workload Type: {full_config['workload_type']}
        - Instance Type: {full_config['instance_type']}
        - Instance Hours: {full_config['instance_hours']}
        - Storage: {full_config['storage_size']} {full_config['storage_unit']}

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm SageMaker appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 150  # ML services can be complex
    
    def get_complexity_score(self) -> int:
        return 8  # High complexity due to ML-specific options

# Register all compute services
service_registry.register_service("ec2", EC2ServiceHandler())
service_registry.register_service("lambda", LambdaServiceHandler())
service_registry.register_service("sagemaker", SageMakerServiceHandler())

logger.info("✅ Compute services registered: EC2, Lambda, SageMaker")
