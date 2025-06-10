"""
Browser Helper Utilities for AWS Calculator Automation

This module provides common browser interaction patterns and utilities
for robust AWS Calculator automation.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from browser_use import Agent
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

class BrowserInteractionPatterns:
    """Common browser interaction patterns for AWS Calculator"""
    
    @staticmethod
    def get_service_search_pattern(service_name: str) -> str:
        """Get standardized service search pattern"""
        return f"""
        Search for {service_name} service:
        
        1. Ensure "Search all services" radio button is selected
        2. Click in the search box with placeholder "Search for a service"
        3. Clear any existing text
        4. Type "{service_name}" in the search box
        5. Wait for search results to filter and display
        6. Look for the {service_name} service card in the results
        7. Click the "Configure" button on the service card
        8. Wait for configuration page to load completely
        
        Verify: You should now be on the {service_name} configuration page.
        """
    
    @staticmethod
    def get_service_configuration_pattern(service_type: str, config: Dict[str, Any]) -> str:
        """Get standardized service configuration pattern"""
        config_items = []
        for key, value in config.items():
            if key not in ['service_type', 'template_name']:
                config_items.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        config_text = '\n'.join(config_items)
        
        return f"""
        Configure {service_type} service with the following settings:
        
        CONFIGURATION STRATEGY:
        1. First, scroll down completely to see all configuration sections
        2. Then scroll back up to start configuration from the top
        3. Configure each setting methodically:
        
        REQUIRED SETTINGS:
        {config_text}
        
        IMPORTANT:
        - Take time to find each field (some may require scrolling)
        - Wait for dropdowns to load before selecting options
        - Verify each setting is applied correctly
        - Look for any validation errors or required fields
        """
    
    @staticmethod
    def get_add_to_estimate_pattern() -> str:
        """Get standardized add to estimate pattern"""
        return """
        Add the configured service to the estimate:
        
        1. Scroll to the bottom of the configuration page
        2. Look for "Save and add service" or "Add to estimate" button
        3. Click the button to add the service to the estimate
        4. Wait for confirmation that the service has been added
        5. Look for success message or return to main calculator page
        
        Verify: The service should be added to the estimate successfully.
        """
    
    @staticmethod
    def get_page_verification_pattern(expected_elements: List[str]) -> str:
        """Get page verification pattern"""
        elements_text = '\n'.join([f"- {element}" for element in expected_elements])
        
        return f"""
        Verify current page has the expected elements:
        
        Expected elements:
        {elements_text}
        
        If any elements are missing, navigate to the correct page.
        """

class ErrorRecoveryPatterns:
    """Error recovery patterns for browser automation"""
    
    @staticmethod
    def get_element_not_found_recovery() -> str:
        """Recovery pattern when element is not found"""
        return """
        Element not found recovery:
        
        1. Scroll up and down to find the element
        2. Wait 3 seconds for dynamic content to load
        3. Check if page has changed or needs refresh
        4. Look for alternative element selectors
        5. If still not found, report the issue
        """
    
    @staticmethod
    def get_page_load_recovery() -> str:
        """Recovery pattern when page doesn't load properly"""
        return """
        Page load recovery:
        
        1. Wait 5 seconds for page to fully load
        2. Check if there are any error messages
        3. Refresh the page if needed
        4. Verify expected page elements are present
        5. If page still doesn't load, navigate to the correct URL
        """
    
    @staticmethod
    def get_network_error_recovery() -> str:
        """Recovery pattern for network errors"""
        return """
        Network error recovery:
        
        1. Wait 10 seconds for network to stabilize
        2. Check if page is accessible
        3. Try refreshing the page
        4. If error persists, restart the browser session
        """

class ServiceSpecificPatterns:
    """Service-specific interaction patterns"""
    
    @staticmethod
    def get_ec2_specific_pattern() -> str:
        """EC2-specific interaction pattern"""
        return """
        EC2-specific considerations:
        
        1. Instance type dropdown may be large - scroll to find specific type
        2. Storage configuration is usually in a separate section
        3. Pricing model options may be under "Workload" section
        4. Operating system affects pricing significantly
        5. Tenancy options are usually at the bottom
        """
    
    @staticmethod
    def get_rds_specific_pattern() -> str:
        """RDS-specific interaction pattern"""
        return """
        RDS-specific considerations:
        
        1. Database engine selection affects available options
        2. Multi-AZ deployment significantly increases cost
        3. Storage type and size are separate configurations
        4. Backup retention affects storage costs
        5. Instance class naming follows db.* pattern
        """
    
    @staticmethod
    def get_s3_specific_pattern() -> str:
        """S3-specific interaction pattern"""
        return """
        S3-specific considerations:
        
        1. Storage class affects pricing significantly
        2. Request patterns (GET/PUT) impact costs
        3. Data transfer costs are separate from storage
        4. Different regions have different pricing
        5. Lifecycle policies can reduce costs
        """

class VisualVerificationHelpers:
    """Helpers for visual verification of actions"""
    
    @staticmethod
    def get_screenshot_verification_pattern(action_description: str) -> str:
        """Get pattern for visual verification after action"""
        return f"""
        Visual verification after: {action_description}
        
        Verification checklist:
        1. Confirm the action was completed successfully
        2. Look for any error messages or warnings
        3. Verify expected elements are visible
        4. Note any changes in page state
        5. Confirm we're still on the correct AWS Calculator page
        
        This is for verification purposes only - no further actions needed.
        """
    
    @staticmethod
    def get_success_indicators() -> List[str]:
        """Get list of success indicators to look for"""
        return [
            "Service added to estimate",
            "Configuration saved",
            "Success message displayed",
            "Return to main calculator page",
            "Service appears in estimate list",
            "No error messages visible"
        ]
    
    @staticmethod
    def get_error_indicators() -> List[str]:
        """Get list of error indicators to watch for"""
        return [
            "Error message displayed",
            "Required field validation error",
            "Page not loading",
            "Service not found",
            "Configuration not saved",
            "Network error message"
        ]

class WaitPatterns:
    """Standardized wait patterns for different scenarios"""
    
    @staticmethod
    async def wait_for_page_load(seconds: int = 3):
        """Wait for page to load"""
        await asyncio.sleep(seconds)
    
    @staticmethod
    async def wait_for_service_addition(seconds: int = 2):
        """Wait after service addition"""
        await asyncio.sleep(seconds)
    
    @staticmethod
    async def wait_for_navigation(seconds: int = 1):
        """Wait after navigation"""
        await asyncio.sleep(seconds)
    
    @staticmethod
    def get_dynamic_wait_pattern() -> str:
        """Get pattern for dynamic waiting"""
        return """
        Dynamic wait strategy:
        
        1. Wait for specific elements to appear
        2. Check for loading indicators to disappear
        3. Verify page is interactive
        4. Look for expected content to be visible
        5. Proceed only when page is fully ready
        """
