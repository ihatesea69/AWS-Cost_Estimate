"""
Service Orchestrator - LangGraph-based Multi-Agent Architecture

This module implements a service-oriented orchestrator that delegates
service-specific tasks to specialized agents using LangGraph patterns.
"""

import asyncio
import logging
from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END, START
from browser_use import Agent

from ..services.service_registry import service_registry
from ..monitoring.logger import start_performance_monitoring, end_performance_monitoring
from src.utils.aws_config import get_bedrock_llm

logger = logging.getLogger(__name__)

class ServiceOrchestrationState(TypedDict):
    """State for service orchestration workflow"""
    services_config: Dict[str, Any]
    workflow_plan: Dict[str, Any]
    current_service_index: int
    completed_services: List[str]
    failed_services: List[str]
    browser_session: Any
    estimate_links: Dict[str, str]
    error_message: str

class ServiceOrchestrator:
    """
    Service-oriented orchestrator using LangGraph patterns
    
    This orchestrator delegates service-specific tasks to specialized handlers
    and manages the overall workflow using LangGraph state management.
    """
    
    def __init__(self):
        self.llm = get_bedrock_llm(temperature=0.1)
        self.workflow = self._build_workflow()
        logger.info("🎭 ServiceOrchestrator initialized with modular architecture")
    
    def _build_workflow(self) -> StateGraph:
        """Build LangGraph workflow for service orchestration"""
        workflow = StateGraph(ServiceOrchestrationState)
        
        # Add workflow nodes
        workflow.add_node("plan_workflow", self.plan_workflow)
        workflow.add_node("initialize_browser", self.initialize_browser)
        workflow.add_node("process_service", self.process_single_service)
        workflow.add_node("finalize_estimate", self.finalize_estimate)
        workflow.add_node("handle_error", self.handle_error)
        
        # Set entry point
        workflow.set_entry_point("plan_workflow")
        
        # Add edges
        workflow.add_edge("plan_workflow", "initialize_browser")
        workflow.add_edge("initialize_browser", "process_service")
        
        # Conditional edges for service processing
        workflow.add_conditional_edges(
            "process_service",
            self._service_router,
            {
                "continue": "process_service",
                "finalize": "finalize_estimate",
                "error": "handle_error"
            }
        )
        
        workflow.add_edge("finalize_estimate", END)
        workflow.add_edge("handle_error", END)
        
        return workflow.compile()
    
    def _service_router(self, state: ServiceOrchestrationState) -> str:
        """Router to determine next action in service processing"""
        if state.get("error_message"):
            return "error"
        
        current_index = state.get("current_service_index", 0)
        total_services = len(state.get("workflow_plan", {}).get("service_order", []))
        
        if current_index >= total_services:
            return "finalize"
        
        return "continue"
    
    async def plan_workflow(self, state: ServiceOrchestrationState) -> ServiceOrchestrationState:
        """Plan the workflow based on services configuration"""
        try:
            services_config = state["services_config"]
            service_types = list(services_config.keys())
            
            # Generate workflow plan using service registry
            workflow_plan = service_registry.get_workflow_plan(service_types)
            
            # Validate all services
            validation_errors = []
            for service_type, config in services_config.items():
                errors = service_registry.validate_service_config(service_type, config)
                validation_errors.extend(errors)
            
            if validation_errors:
                state["error_message"] = f"Configuration validation failed: {'; '.join(validation_errors)}"
                return state
            
            state["workflow_plan"] = workflow_plan
            state["current_service_index"] = 0
            state["completed_services"] = []
            state["failed_services"] = []
            
            logger.info(f"📋 Workflow planned for {len(service_types)} services")
            logger.info(f"⏱️ Estimated time: {workflow_plan['total_estimated_time']} seconds")
            logger.info(f"🎯 Service order: {workflow_plan['service_order']}")
            
        except Exception as e:
            state["error_message"] = f"Workflow planning failed: {str(e)}"
            logger.error(f"❌ Workflow planning error: {e}")
        
        return state
    
    async def initialize_browser(self, state: ServiceOrchestrationState) -> ServiceOrchestrationState:
        """Initialize browser session for the workflow"""
        try:
            # Create browser agent with comprehensive task
            task_description = self._build_comprehensive_task(state)
            
            browser_agent = Agent(
                task=task_description,
                llm=self.llm,
                use_vision=True
            )
            
            state["browser_session"] = browser_agent
            logger.info("🌐 Browser session initialized")
            
        except Exception as e:
            state["error_message"] = f"Browser initialization failed: {str(e)}"
            logger.error(f"❌ Browser initialization error: {e}")
        
        return state
    
    async def process_single_service(self, state: ServiceOrchestrationState) -> ServiceOrchestrationState:
        """Process a single service using its specialized handler"""
        try:
            workflow_plan = state["workflow_plan"]
            current_index = state["current_service_index"]
            service_order = workflow_plan["service_order"]
            
            if current_index >= len(service_order):
                return state  # All services processed
            
            service_type = service_order[current_index]
            service_config = state["services_config"][service_type]
            
            operation_id = start_performance_monitoring(f"service_{service_type}")
            
            # Get service handler
            handler = service_registry.get_handler(service_type)
            if not handler:
                raise ValueError(f"No handler found for service: {service_type}")
            
            logger.info(f"🔄 Processing service {current_index + 1}/{len(service_order)}: {service_type}")
            
            # Execute service-specific workflow
            success = await self._execute_service_workflow(
                state["browser_session"],
                handler,
                service_config,
                service_type
            )
            
            if success:
                state["completed_services"].append(service_type)
                logger.info(f"✅ Service {service_type} completed successfully")
                end_performance_monitoring(operation_id, success=True)
            else:
                state["failed_services"].append(service_type)
                logger.warning(f"⚠️ Service {service_type} failed")
                end_performance_monitoring(operation_id, success=False)
            
            # Move to next service
            state["current_service_index"] = current_index + 1
            
        except Exception as e:
            error_msg = f"Service processing error: {str(e)}"
            state["error_message"] = error_msg
            logger.error(f"❌ {error_msg}")
        
        return state
    
    async def _execute_service_workflow(self, browser_agent: Agent, handler, config: Dict[str, Any], service_type: str) -> bool:
        """Execute workflow for a specific service"""
        try:
            # Get service-specific instructions
            instructions = handler.get_service_instructions(config)
            timeout = handler.get_timeout_seconds()
            
            # Create service-specific task
            service_task = f"""
            🎯 ADD {handler.get_service_name().upper()} TO AWS CALCULATOR
            
            Current Status: Adding service {service_type} to existing estimate
            
            NAVIGATION REQUIREMENTS:
            1. Ensure you are on https://calculator.aws/#/addService page
            2. If not, navigate to that page first
            3. Look for "Find Service" search box
            
            SERVICE-SPECIFIC INSTRUCTIONS:
            {instructions}
            
            CRITICAL SUCCESS CRITERIA:
            - Service must be added to the SAME estimate as previous services
            - Must return to /addService page after adding service
            - Verify service appears in estimate summary
            - No error messages should be displayed
            """
            
            # Execute with timeout
            result = await asyncio.wait_for(
                browser_agent.run(max_steps=50),
                timeout=timeout
            )
            
            return True  # If no exception, consider success
            
        except asyncio.TimeoutError:
            logger.error(f"❌ Service {service_type} timed out after {timeout} seconds")
            return False
        except Exception as e:
            logger.error(f"❌ Service {service_type} execution failed: {e}")
            return False
    
    def _build_comprehensive_task(self, state: ServiceOrchestrationState) -> str:
        """Build comprehensive task description for the entire workflow"""
        workflow_plan = state["workflow_plan"]
        services = workflow_plan["service_order"]
        
        return f"""
        🎯 AWS COST ESTIMATION - MULTI-SERVICE WORKFLOW
        
        MISSION: Add {len(services)} AWS services to a single estimate
        Services: {', '.join(services)}
        Estimated time: {workflow_plan['total_estimated_time']} seconds
        
        WORKFLOW OVERVIEW:
        1. Navigate to AWS Pricing Calculator
        2. Add each service sequentially to the same estimate
        3. Generate final estimate link
        
        CRITICAL GUIDELINES:
        - ALL services must be added to the SAME estimate
        - After each service, return to /addService page
        - Verify each service appears in estimate summary
        - Use exact service names when searching
        - Wait for pages to load completely
        
        You will receive specific instructions for each service as we progress.
        """
    
    async def finalize_estimate(self, state: ServiceOrchestrationState) -> ServiceOrchestrationState:
        """Finalize the estimate and extract links"""
        try:
            browser_agent = state["browser_session"]
            
            # Extract estimate links
            finalization_task = """
            🔗 FINALIZE AWS COST ESTIMATE
            
            MISSION: Generate shareable estimate link
            
            STEPS:
            1. Navigate to estimate summary/review page
            2. Look for "Share" or "Get estimate link" button
            3. Generate public shareable link
            4. Copy the complete estimate URL
            5. Provide the final estimate URL in format:
               "Final Estimate URL: https://calculator.aws/#/estimate?id=ACTUAL_ID"
            
            CRITICAL: Must provide the actual working estimate URL
            """
            
            result = await asyncio.wait_for(
                browser_agent.run(max_steps=20),
                timeout=60
            )
            
            # Extract estimate link from result
            estimate_link = self._extract_estimate_link(result)
            
            if estimate_link:
                state["estimate_links"] = {
                    "ondemand": estimate_link,
                    "savings_plan": estimate_link,
                    "real_link": estimate_link
                }
            
            logger.info(f"✅ Workflow completed: {len(state['completed_services'])} services added")
            
        except Exception as e:
            state["error_message"] = f"Finalization failed: {str(e)}"
            logger.error(f"❌ Finalization error: {e}")
        
        return state
    
    def _extract_estimate_link(self, result) -> str:
        """Extract estimate link from browser result"""
        try:
            result_str = str(result)
            
            # Look for estimate URL patterns
            import re
            patterns = [
                r'Final Estimate URL:\s*(https://calculator\.aws/#/estimate\?id=([a-f0-9]+))',
                r'https://calculator\.aws/#/estimate\?id=([a-f0-9]+)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, result_str, re.IGNORECASE)
                if matches:
                    if isinstance(matches[0], tuple):
                        return matches[0][0]
                    return f"https://calculator.aws/#/estimate?id={matches[0]}"
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Link extraction error: {e}")
            return None
    
    async def handle_error(self, state: ServiceOrchestrationState) -> ServiceOrchestrationState:
        """Handle workflow errors"""
        error_msg = state.get("error_message", "Unknown error")
        logger.error(f"❌ Workflow error: {error_msg}")
        
        return state
    
    async def run_estimation(self, services_config: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to run service-oriented estimation workflow"""
        initial_state = ServiceOrchestrationState(
            services_config=services_config,
            workflow_plan={},
            current_service_index=0,
            completed_services=[],
            failed_services=[],
            browser_session=None,
            estimate_links={},
            error_message=""
        )
        
        try:
            final_state = await self.workflow.ainvoke(initial_state)
            
            # Format result
            if final_state.get("error_message"):
                return {
                    "status": "error",
                    "error": final_state["error_message"],
                    "services_attempted": list(services_config.keys())
                }
            
            return {
                "status": "success",
                "services_added": final_state["completed_services"],
                "services_failed": final_state["failed_services"],
                "estimate_links": final_state["estimate_links"],
                "workflow_plan": final_state["workflow_plan"],
                "summary": {
                    "total_services": len(services_config),
                    "successful": len(final_state["completed_services"]),
                    "failed": len(final_state["failed_services"])
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Orchestration error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "services_attempted": list(services_config.keys())
            }
