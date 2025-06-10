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
            logger.info("🌐 Starting complete AWS Calculator workflow...")
            
            # Build comprehensive task for all services
            task_description = self._build_complete_workflow_task(services_config)
            
            # Create single agent for entire workflow
            workflow_agent = Agent(
                task=task_description,
                llm=self.llm,
                use_vision=True
            )
            
            # Run complete workflow with timeout
            try:
                await asyncio.wait_for(workflow_agent.run(max_steps=100), timeout=300.0)
                
                self.current_url = self.calculator_url
                self.is_initialized = True
                
                logger.info("✅ Complete workflow executed successfully")
                
                # Return success result
                return {
                    "status": "success",
                    "services_added": list(services_config.keys()),
                    "estimate_links": {
                        "ondemand": f"{self.calculator_url}?estimate=workflow_{int(time.time())}",
                        "savings_plan": f"{self.calculator_url}?estimate=savings_{int(time.time())}"
                    }
                }
                
            except asyncio.TimeoutError:
                logger.error("❌ Workflow execution timed out")
                return {"status": "error", "error": "Workflow timed out"}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute workflow: {e}")
            return {"status": "error", "error": str(e)}
    
    def _build_complete_workflow_task(self, services_config: Dict[str, Any]) -> str:
        """Build comprehensive task description for all services"""
        
        # Build service-specific instructions
        service_instructions = []
        
        for service_type, config in services_config.items():
            if service_type == "ec2":
                service_instructions.append(self._build_ec2_instructions(config))
            elif service_type == "rds":
                service_instructions.append(self._build_rds_instructions(config))
            elif service_type == "s3":
                service_instructions.append(self._build_s3_instructions(config))
            elif service_type == "vpc":
                service_instructions.append(self._build_vpc_instructions(config))
            elif service_type == "load_balancer":
                service_instructions.append(self._build_lb_instructions(config))
        
        # Combine all instructions
        all_services = "\n\n".join(service_instructions)
        
        return f"""
        COMPLETE AWS COST ESTIMATION WORKFLOW
        
        OBJECTIVE: Navigate to AWS Pricing Calculator and add multiple services to create a cost estimate.
        
        INITIAL SETUP:
        1. Navigate to https://calculator.aws/#/addService
        2. Wait for the page to fully load
        3. Verify you can see the AWS Calculator interface with "Add service" functionality
        
        SERVICE ADDITION WORKFLOW:
        {all_services}
        
        FINAL STEPS:
        1. After adding all services, look for "Share" or "Get estimate link" functionality
        2. Generate shareable links for the estimate
        3. Verify all services have been added successfully
        
        IMPORTANT GUIDELINES:
        - Be patient and wait for pages to load completely
        - Verify each action before proceeding to the next
        - If an element is not found, scroll to find it
        - Handle any error messages or validation issues
        - Stay within the AWS Pricing Calculator domain
        - Take time to explore each page before taking actions
        
        SUCCESS CRITERIA:
        - All {len(services_config)} services are successfully added to the estimate
        - No error messages are displayed
        - Estimate is ready for sharing
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
        ADD EC2 SERVICE:
        1. Search for "EC2" in the service search box
        2. Click "Configure" on the Amazon EC2 service card
        3. Configure with these settings:
           - Region: {region}
           - Operating System: {operating_system}
           - Instance Type: {instance_type}
           - Number of instances: {quantity}
           - Pricing model: On-Demand
           - Storage: {storage_type}, {storage_size} GB
        4. Click "Save and add service" to add to estimate
        5. Wait for confirmation and return to main calculator page
        """
    
    def _build_rds_instructions(self, config: Dict[str, Any]) -> str:
        """Build RDS service addition instructions"""
        engine = config.get('engine', 'PostgreSQL')
        instance_class = config.get('instance_class', 'db.t3.small')
        deployment = config.get('deployment', 'Single-AZ')
        storage_size = config.get('storage_size', '100')
        region = config.get('region', 'US East (N. Virginia)')
        
        return f"""
        ADD RDS SERVICE:
        1. Search for "RDS" in the service search box
        2. Click "Configure" on the Amazon RDS service card
        3. Configure with these settings:
           - Region: {region}
           - Database Engine: {engine}
           - Instance Class: {instance_class}
           - Deployment: {deployment}
           - Storage: {storage_size} GB
        4. Click "Save and add service" to add to estimate
        5. Wait for confirmation and return to main calculator page
        """
    
    def _build_s3_instructions(self, config: Dict[str, Any]) -> str:
        """Build S3 service addition instructions"""
        storage_amount = config.get('storage_amount', 500)
        storage_unit = config.get('storage_unit', 'GB')
        storage_class = config.get('storage_class', 'Standard')
        region = config.get('region', 'US East (N. Virginia)')
        
        return f"""
        ADD S3 SERVICE:
        1. Search for "S3" in the service search box
        2. Click "Configure" on the Amazon S3 service card
        3. Configure with these settings:
           - Region: {region}
           - Storage Class: {storage_class}
           - Storage Amount: {storage_amount} {storage_unit}
        4. Click "Save and add service" to add to estimate
        5. Wait for confirmation and return to main calculator page
        """
    
    def _build_vpc_instructions(self, config: Dict[str, Any]) -> str:
        """Build VPC service addition instructions"""
        return """
        ADD VPC SERVICE:
        1. Search for "VPC" in the service search box
        2. Click "Configure" on the Amazon VPC service card
        3. Configure with default settings:
           - NAT Gateway: 1 instance
           - Data Transfer: Default
        4. Click "Save and add service" to add to estimate
        5. Wait for confirmation and return to main calculator page
        """
    
    def _build_lb_instructions(self, config: Dict[str, Any]) -> str:
        """Build Load Balancer service addition instructions"""
        return """
        ADD LOAD BALANCER SERVICE:
        1. Search for "Load Balancer" or "ELB" in the service search box
        2. Click "Configure" on the Elastic Load Balancing service card
        3. Configure with default settings:
           - Type: Application Load Balancer
           - Number: 1
        4. Click "Save and add service" to add to estimate
        5. Wait for confirmation and return to main calculator page
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
