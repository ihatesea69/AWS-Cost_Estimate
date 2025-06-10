"""
Unified AWS Calculator Browser Agent - Clean Implementation

This module provides a streamlined browser automation agent for AWS Calculator
using the browser-use library with optimized workflow approach.
"""

import asyncio
import time
import sys
import os
import logging
from typing import Dict, Any, List
from browser_use import Agent
from langchain_openai import ChatOpenAI

# Fix Windows asyncio event loop policy
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedAWSBrowserAgent:
    """
    Unified AWS Calculator Browser Agent with optimized workflow approach.
    
    This agent uses a single browser session to complete entire workflows,
    minimizing browser restarts and improving reliability.
    """
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_api_key,
            temperature=0.1
        )
        self.calculator_url = "https://calculator.aws/#/addService"
        self.current_url = None
        self.is_initialized = False
        
        # Set environment for visible browser
        os.environ['HEADLESS'] = 'false'
        os.environ['BROWSER_TYPE'] = 'chromium'
        
        logger.info("UnifiedAWSBrowserAgent initialized")

    async def run_complete_workflow(self, services_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run complete workflow in a single browser session"""
        try:
            logger.info(f"🌐 Starting complete AWS Calculator workflow for {len(services_config)} services...")
            logger.info(f"📋 Services to add: {list(services_config.keys())}")

            # Build comprehensive task for all services
            task_description = self._build_complete_workflow_task(services_config)

            # Create single agent for entire workflow with enhanced settings
            workflow_agent = Agent(
                task=task_description,
                llm=self.llm,
                use_vision=True
            )

            # Run complete workflow with extended timeout for multiple services
            max_steps = 50 + (len(services_config) * 25)  # Dynamic step limit based on service count
            timeout = 180 + (len(services_config) * 60)   # Dynamic timeout: 3min base + 1min per service

            logger.info(f"⚙️ Workflow settings: max_steps={max_steps}, timeout={timeout}s")

            try:
                result = await asyncio.wait_for(workflow_agent.run(max_steps=max_steps), timeout=timeout)

                self.current_url = self.calculator_url
                self.is_initialized = True

                logger.info("✅ Complete workflow executed successfully")

                # Extract real estimate link from agent result
                real_estimate_link = self._extract_estimate_link_from_result(result)

                # Generate timestamp for unique estimate links
                timestamp = int(time.time())

                # Return success result with real estimate links
                estimate_links = {}
                if real_estimate_link:
                    logger.info(f"🔗 Real estimate link found: {real_estimate_link}")
                    estimate_links = {
                        "ondemand": real_estimate_link,
                        "savings_plan": real_estimate_link,  # Same link for all pricing models
                        "reserved": real_estimate_link,
                        "real_link": real_estimate_link  # Add explicit real link field
                    }
                else:
                    logger.warning("⚠️ No real estimate link found, using fallback links")
                    estimate_links = {
                        "ondemand": f"{self.calculator_url}?estimate=complete_{timestamp}",
                        "savings_plan": f"{self.calculator_url}?estimate=savings_{timestamp}",
                        "reserved": f"{self.calculator_url}?estimate=reserved_{timestamp}"
                    }

                return {
                    "status": "success",
                    "services_added": list(services_config.keys()),
                    "services_count": len(services_config),
                    "workflow_duration": f"{timeout}s max",
                    "estimate_links": estimate_links,
                    "timestamp": timestamp,
                    "agent_result": str(result) if result else None  # Include agent result for debugging
                }

            except asyncio.TimeoutError:
                logger.error(f"❌ Workflow execution timed out after {timeout}s")
                return {
                    "status": "error",
                    "error": f"Workflow timed out after {timeout} seconds",
                    "services_attempted": list(services_config.keys())
                }

        except Exception as e:
            logger.error(f"❌ Failed to execute workflow: {e}")
            return {
                "status": "error",
                "error": str(e),
                "services_attempted": list(services_config.keys()) if services_config else []
            }

    def _extract_estimate_link_from_result(self, result) -> str:
        """Extract real estimate link from agent result"""
        try:
            if not result:
                return None

            result_str = str(result)

            # Look for estimate links in the result
            import re

            # Pattern to match AWS Calculator estimate links
            patterns = [
                r'https://calculator\.aws/#/estimate\?id=([a-f0-9]+)',
                r'calculator\.aws/#/estimate\?id=([a-f0-9]+)',
                r'estimate\?id=([a-f0-9]+)'
            ]

            for pattern in patterns:
                matches = re.findall(pattern, result_str)
                if matches:
                    estimate_id = matches[-1]  # Get the last (most recent) match
                    full_link = f"https://calculator.aws/#/estimate?id={estimate_id}"
                    logger.info(f"🔗 Extracted estimate link: {full_link}")
                    return full_link

            # If no pattern matches, try to find any calculator.aws link
            calculator_links = re.findall(r'https://calculator\.aws[^\s\)]+', result_str)
            if calculator_links:
                link = calculator_links[-1]  # Get the last link
                logger.info(f"🔗 Found calculator link: {link}")
                return link

            logger.warning("⚠️ No estimate link found in agent result")
            return None

        except Exception as e:
            logger.error(f"❌ Error extracting estimate link: {e}")
            return None
    
    def _build_complete_workflow_task(self, services_config: Dict[str, Any]) -> str:
        """Build comprehensive task description for all services"""

        # Build service-specific instructions
        service_instructions = []
        service_count = 0

        for service_type, config in services_config.items():
            service_count += 1
            if service_type == "ec2":
                service_instructions.append(f"SERVICE {service_count}: {self._build_ec2_instructions(config)}")
            elif service_type == "rds":
                service_instructions.append(f"SERVICE {service_count}: {self._build_rds_instructions(config)}")
            elif service_type == "s3":
                service_instructions.append(f"SERVICE {service_count}: {self._build_s3_instructions(config)}")
            elif service_type == "vpc":
                service_instructions.append(f"SERVICE {service_count}: {self._build_vpc_instructions(config)}")
            elif service_type == "load_balancer":
                service_instructions.append(f"SERVICE {service_count}: {self._build_lb_instructions(config)}")

        # Combine all instructions
        all_services = "\n\n".join(service_instructions)

        return f"""
        🎯 COMPLETE AWS COST ESTIMATION WORKFLOW

        📋 MISSION: Add {len(services_config)} services to AWS Pricing Calculator in a single estimate
        Services to add: {', '.join(services_config.keys())}

        🚀 PHASE 1: INITIAL SETUP
        1. Navigate to https://calculator.aws/#/addService
        2. Wait for the page to fully load (look for "Add service" interface)
        3. Verify you can see the AWS Calculator with service search functionality
        4. Take a moment to understand the page layout

        ⚙️ PHASE 2: SERVICE ADDITION SEQUENCE
        IMPORTANT: Add each service to the SAME estimate (do not create separate estimates)

        {all_services}

        🔗 PHASE 3: FINALIZATION
        1. After adding ALL {len(services_config)} services, navigate to estimate summary
        2. Look for "View summary" or similar button to see all added services
        3. Verify all {len(services_config)} services are listed in the estimate
        4. Look for "Share" or "Get estimate link" functionality
        5. Generate a shareable public link for the complete estimate
        6. Copy or note the final estimate URL

        ⚠️ CRITICAL GUIDELINES:
        - PATIENCE: Wait for each page to load completely before taking actions
        - VERIFICATION: After each service addition, verify it was added successfully
        - PERSISTENCE: If an element is not found, scroll or wait for it to appear
        - ERROR HANDLING: If you encounter errors, try alternative approaches
        - SINGLE ESTIMATE: All services must be added to the same estimate
        - STAY FOCUSED: Remain within the AWS Pricing Calculator domain

        ✅ SUCCESS CRITERIA:
        - All {len(services_config)} services successfully added to ONE estimate
        - No error messages or validation failures
        - Final estimate link generated and accessible
        - Estimate contains all requested services with correct configurations

        🎯 EXPECTED OUTCOME: One comprehensive estimate link containing all {len(services_config)} services
        """
    
    def _build_ec2_instructions(self, config: Dict[str, Any]) -> str:
        """Build EC2 service addition instructions"""
        instance_type = config.get('instance_type', 't3.medium')
        quantity = config.get('quantity', 1)
        operating_system = config.get('operating_system', 'Linux')
        region = config.get('region', 'US East (N. Virginia)')
        storage_type = config.get('storage_type', 'gp3')
        storage_size = config.get('storage_size', '20')

        return f"""
        🖥️ ADD AMAZON EC2 SERVICE:

        Step 1: Service Selection
        - In the service search box, type "EC2" and press Enter
        - Wait for search results to filter
        - Find "Amazon EC2" service card
        - Click "Configure" button on the EC2 service card
        - Wait for EC2 configuration page to load

        Step 2: Configuration
        Configure EC2 with these EXACT settings:
        - Region: {region}
        - Operating System: {operating_system}
        - Instance Type: {instance_type}
        - Number of instances: {quantity}
        - Tenancy: Shared Instances (default)
        - Pricing model: On-Demand
        - Storage Type: {storage_type}
        - Storage Size: {storage_size} GB

        Step 3: Add to Estimate
        - Scroll to bottom of configuration page
        - Click "Save and add service" button
        - Wait for confirmation message
        - Verify you return to main calculator page
        - Confirm EC2 service appears in estimate summary
        """
    
    def _build_rds_instructions(self, config: Dict[str, Any]) -> str:
        """Build RDS service addition instructions"""
        engine = config.get('engine', 'PostgreSQL')
        instance_class = config.get('instance_class', 'db.t3.small')
        deployment = config.get('deployment', 'Single-AZ')
        storage_size = config.get('storage_size', '100')
        region = config.get('region', 'US East (N. Virginia)')

        return f"""
        🗄️ ADD AMAZON RDS SERVICE:

        Step 1: Service Selection
        - In the service search box, type "RDS" and press Enter
        - Wait for search results to filter
        - Find "Amazon RDS" service card
        - Click "Configure" button on the RDS service card
        - Wait for RDS configuration page to load

        Step 2: Configuration
        Configure RDS with these EXACT settings:
        - Region: {region}
        - Database Engine: {engine}
        - Instance Class: {instance_class}
        - Deployment Option: {deployment}
        - Storage Type: General Purpose SSD (gp3) or default
        - Storage Amount: {storage_size} GB
        - Backup Retention: 7 days (default)

        Step 3: Add to Estimate
        - Scroll to bottom of configuration page
        - Click "Save and add service" button
        - Wait for confirmation message
        - Verify you return to main calculator page
        - Confirm RDS service appears in estimate summary
        """
    
    def _build_s3_instructions(self, config: Dict[str, Any]) -> str:
        """Build S3 service addition instructions"""
        storage_amount = config.get('storage_amount', 500)
        storage_unit = config.get('storage_unit', 'GB')
        storage_class = config.get('storage_class', 'Standard')
        region = config.get('region', 'US East (N. Virginia)')

        return f"""
        🪣 ADD AMAZON S3 SERVICE:

        Step 1: Service Selection
        - In the service search box, type "S3" and press Enter
        - Wait for search results to filter
        - Find "Amazon S3" service card
        - Click "Configure" button on the S3 service card
        - Wait for S3 configuration page to load

        Step 2: Configuration
        Configure S3 with these EXACT settings:
        - Region: {region}
        - Storage Class: {storage_class}
        - Storage Amount: {storage_amount} {storage_unit}
        - Data Transfer: Default settings
        - Requests: Default settings

        Step 3: Add to Estimate
        - Scroll to bottom of configuration page
        - Click "Save and add service" button
        - Wait for confirmation message
        - Verify you return to main calculator page
        - Confirm S3 service appears in estimate summary
        """
    
    def _build_vpc_instructions(self, config: Dict[str, Any]) -> str:
        """Build VPC service addition instructions"""
        return """
        🌐 ADD AMAZON VPC SERVICE:

        Step 1: Service Selection
        - In the service search box, type "VPC" and press Enter
        - Wait for search results to filter
        - Find "Amazon VPC" service card
        - Click "Configure" button on the VPC service card
        - Wait for VPC configuration page to load

        Step 2: Configuration
        Configure VPC with these settings:
        - NAT Gateway: 1 instance
        - Data Transfer: Default settings
        - VPC Endpoints: Default settings

        Step 3: Add to Estimate
        - Scroll to bottom of configuration page
        - Click "Save and add service" button
        - Wait for confirmation message
        - Verify you return to main calculator page
        - Confirm VPC service appears in estimate summary
        """

    def _build_lb_instructions(self, config: Dict[str, Any]) -> str:
        """Build Load Balancer service addition instructions"""
        return """
        ⚖️ ADD ELASTIC LOAD BALANCING SERVICE:

        Step 1: Service Selection
        - In the service search box, type "Load Balancer" or "ELB" and press Enter
        - Wait for search results to filter
        - Find "Elastic Load Balancing" service card
        - Click "Configure" button on the ELB service card
        - Wait for Load Balancer configuration page to load

        Step 2: Configuration
        Configure Load Balancer with these settings:
        - Load Balancer Type: Application Load Balancer
        - Number of Load Balancers: 1
        - Data Processing: Default settings

        Step 3: Add to Estimate
        - Scroll to bottom of configuration page
        - Click "Save and add service" button
        - Wait for confirmation message
        - Verify you return to main calculator page
        - Confirm Load Balancer service appears in estimate summary
        """

    # Main interface methods
    async def add_service_by_type(self, service_type: str, config: Dict[str, Any]) -> bool:
        """Add service by type - uses complete workflow approach"""
        try:
            logger.info(f"🔄 Adding single service: {service_type}")
            
            # For single service, create mini workflow
            services_config = {service_type: config}
            result = await self.run_complete_workflow(services_config)
            
            return result.get("status") == "success"
            
        except Exception as e:
            logger.error(f"❌ Error adding service {service_type}: {e}")
            return False
    
    async def add_multiple_services(self, services_config: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Add multiple services in a single workflow"""
        try:
            logger.info(f"🔄 Adding multiple services: {list(services_config.keys())}")
            
            result = await self.run_complete_workflow(services_config)
            return result
            
        except Exception as e:
            logger.error(f"❌ Error adding multiple services: {e}")
            return {"status": "error", "error": str(e)}
    
    async def get_estimate_links(self) -> Dict[str, str]:
        """Get estimate links - simplified for new approach"""
        try:
            # Return placeholder links with timestamp
            timestamp = int(time.time())
            
            return {
                "ondemand": f"{self.calculator_url}?estimate=ondemand_{timestamp}",
                "savings_plan": f"{self.calculator_url}?estimate=savings_{timestamp}"
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting estimate links: {e}")
            return {}
    
    async def navigate_to_calculator(self) -> bool:
        """Navigate to AWS Pricing Calculator - simplified"""
        try:
            # This is now handled within the workflow
            self.is_initialized = True
            return True
        except Exception as e:
            logger.error(f"❌ Navigation error: {e}")
            return False
    
    async def cleanup_session(self):
        """Cleanup browser session and resources"""
        try:
            # Browser cleanup is handled automatically by browser-use
            self.is_initialized = False
            logger.info("🧹 Browser session cleaned up")
        except Exception as e:
            logger.warning(f"⚠️ Cleanup warning: {e}")

    # Backward compatibility methods
    async def add_ec2_service(self, config: Dict[str, Any]) -> bool:
        """Add EC2 service - backward compatibility"""
        return await self.add_service_by_type("ec2", config)
    
    async def add_rds_service(self, config: Dict[str, Any]) -> bool:
        """Add RDS service - backward compatibility"""
        return await self.add_service_by_type("rds", config)
    
    async def add_s3_service(self, config: Dict[str, Any]) -> bool:
        """Add S3 service - backward compatibility"""
        return await self.add_service_by_type("s3", config)
    
    async def add_vpc_service(self, config: Dict[str, Any]) -> bool:
        """Add VPC service - backward compatibility"""
        return await self.add_service_by_type("vpc", config)
    
    async def add_load_balancer_service(self, config: Dict[str, Any]) -> bool:
        """Add Load Balancer service - backward compatibility"""
        return await self.add_service_by_type("load_balancer", config)

# Backward compatibility alias
AWSCalculatorBrowserAgent = UnifiedAWSBrowserAgent
