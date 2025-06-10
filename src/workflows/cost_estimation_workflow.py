import asyncio
import logging
from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.agents.browser_agent import UnifiedAWSBrowserAgent
from src.utils.template_parser import TemplateParser
from src.monitoring.logger import (
    start_workflow_monitoring, end_workflow_monitoring,
    log_service_event, start_performance_monitoring,
    end_performance_monitoring
)

logger = logging.getLogger(__name__)

class EstimationState(TypedDict):
    user_input: str
    parsed_services: Dict[str, Any]
    auto_filled_info: List[str]
    services_to_add: List[str]
    current_service_index: int
    added_services: List[str]
    failed_services: List[str]
    estimate_links: Dict[str, str]
    final_result: Dict[str, Any]
    error_message: str

class CostEstimationWorkflow:
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.browser_agent = UnifiedAWSBrowserAgent(openai_api_key)
        self.template_parser = TemplateParser(openai_api_key)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_api_key,
            temperature=0.1
        )
        self.workflow = self._build_workflow()
        logger.info("CostEstimationWorkflow initialized with UnifiedAWSBrowserAgent")
    
    def _build_workflow(self) -> StateGraph:
        """Build unified LangGraph workflow"""
        workflow = StateGraph(EstimationState)

        # Add nodes for unified workflow
        workflow.add_node("parse_input", self.parse_user_input)
        workflow.add_node("validate_config", self.validate_configuration)
        workflow.add_node("prepare_services", self.prepare_services_queue)
        workflow.add_node("execute_complete_workflow", self.execute_complete_workflow)
        workflow.add_node("format_result", self.format_final_result)
        workflow.add_node("handle_error", self.handle_error)

        # Set entry point
        workflow.set_entry_point("parse_input")

        # Add edges for streamlined workflow
        workflow.add_edge("parse_input", "validate_config")

        workflow.add_conditional_edges(
            "validate_config",
            self._validation_router,
            {
                "valid": "prepare_services",
                "invalid": "handle_error"
            }
        )

        workflow.add_edge("prepare_services", "execute_complete_workflow")
        workflow.add_edge("execute_complete_workflow", "format_result")
        workflow.add_edge("format_result", END)
        workflow.add_edge("handle_error", END)

        return workflow.compile()
    
    # Router functions
    def _validation_router(self, state: EstimationState) -> str:
        """Router để kiểm tra validation"""
        if state.get("error_message"):
            return "invalid"
        return "valid"
    
    # Node implementations
    async def parse_user_input(self, state: EstimationState) -> EstimationState:
        """Parse user input và extract service requirements"""
        try:
            user_input = state["user_input"]
            
            # Parse với template parser
            services, auto_filled = await self.template_parser.parse_user_requirement(user_input)
            
            state["parsed_services"] = services
            state["auto_filled_info"] = auto_filled
            state["current_service_index"] = 0
            state["added_services"] = []
            state["failed_services"] = []
            
            print(f"✅ Parsed services: {list(services.keys())}")
            print(f"📝 Auto-filled info: {auto_filled}")
            
        except Exception as e:
            state["error_message"] = f"Error parsing input: {str(e)}"
            print(f"❌ Parse error: {e}")
        
        return state
    
    async def validate_configuration(self, state: EstimationState) -> EstimationState:
        """Validate parsed configuration"""
        try:
            services = state.get("parsed_services", {})
            
            if not services:
                state["error_message"] = "No valid services found in user input"
                return state
            
            # Validate từng service
            is_valid, errors = self.template_parser.validate_configuration(services)
            
            if not is_valid:
                state["error_message"] = f"Configuration errors: {', '.join(errors)}"
                return state
            
            print(f"✅ Configuration validated for {len(services)} services")
            
        except Exception as e:
            state["error_message"] = f"Validation error: {str(e)}"
        
        return state
    
    async def execute_complete_workflow(self, state: EstimationState) -> EstimationState:
        """Execute complete workflow in single browser session"""
        operation_id = start_performance_monitoring("complete_workflow")

        try:
            logger.info("🌐 Starting complete AWS Calculator workflow...")

            # Get all services configuration directly from parsed_services
            parsed_services = state.get("parsed_services", {})
            services_to_add = state.get("services_to_add", [])

            # Use services_to_add order but get config from parsed_services
            all_services_config = {}
            for service_type in services_to_add:
                if service_type in parsed_services:
                    all_services_config[service_type] = parsed_services[service_type]

            if not all_services_config:
                # Fallback: use all parsed services if services_to_add is empty
                all_services_config = parsed_services

            logger.info(f"📋 Executing workflow for {len(all_services_config)} services: {list(all_services_config.keys())}")

            # Execute complete workflow in single browser session
            result = await self.browser_agent.run_complete_workflow(all_services_config)

            if result.get("status") == "success":
                state["added_services"] = result.get("services_added", [])
                state["estimate_links"] = result.get("estimate_links", {})
                state["failed_services"] = []  # Clear failed services on success
                logger.info(f"✅ Complete workflow successful: {len(state['added_services'])} services added")
                end_performance_monitoring(operation_id, success=True,
                                         metadata={"services_count": len(state["added_services"])})
            else:
                state["error_message"] = result.get("error", "Unknown workflow error")
                state["failed_services"] = list(all_services_config.keys())
                state["added_services"] = []
                logger.error(f"❌ Complete workflow failed: {state['error_message']}")
                end_performance_monitoring(operation_id, success=False,
                                         error_message=state["error_message"])

        except Exception as e:
            error_msg = f"Complete workflow error: {str(e)}"
            state["error_message"] = error_msg
            state["failed_services"] = list(state.get("parsed_services", {}).keys())
            state["added_services"] = []
            logger.error(f"❌ Complete workflow error: {e}")
            end_performance_monitoring(operation_id, success=False, error_message=error_msg)

        return state
    
    async def prepare_services_queue(self, state: EstimationState) -> EstimationState:
        """Prepare queue of services to add"""
        try:
            services = state.get("parsed_services", {})
            service_order = ["vpc", "ec2", "rds", "s3", "load_balancer"]  # Thứ tự add services
            
            # Sắp xếp services theo thứ tự ưu tiên
            ordered_services = []
            for service_type in service_order:
                if service_type in services:
                    ordered_services.append(service_type)
            
            # Add any remaining services
            for service_type in services:
                if service_type not in ordered_services:
                    ordered_services.append(service_type)
            
            state["services_to_add"] = ordered_services
            state["current_service_index"] = 0
            
            print(f"📋 Services queue prepared: {ordered_services}")
        
        except Exception as e:
            state["error_message"] = f"Error preparing services: {str(e)}"
        
        return state
    
# Note: Old single service methods removed - now using unified workflow approach
    
    async def format_final_result(self, state: EstimationState) -> EstimationState:
        """Format final result"""
        try:
            result = {
                "status": "success",
                "services_requested": list(state.get("parsed_services", {}).keys()),
                "services_added": state.get("added_services", []),
                "services_failed": state.get("failed_services", []),
                "auto_filled_info": state.get("auto_filled_info", []),
                "estimate_links": state.get("estimate_links", {}),
                "summary": {
                    "total_services": len(state.get("parsed_services", {})),
                    "successful": len(state.get("added_services", [])),
                    "failed": len(state.get("failed_services", []))
                }
            }
            
            state["final_result"] = result
            print("✅ Final result formatted")
        
        except Exception as e:
            state["error_message"] = f"Error formatting result: {str(e)}"
        
        return state
    
    async def handle_error(self, state: EstimationState) -> EstimationState:
        """Handle errors"""
        error_msg = state.get("error_message", "Unknown error")
        
        result = {
            "status": "error",
            "error": error_msg,
            "services_requested": list(state.get("parsed_services", {}).keys()),
            "auto_filled_info": state.get("auto_filled_info", [])
        }
        
        state["final_result"] = result
        print(f"❌ Error handled: {error_msg}")
        
        return state
    
    async def run_estimation(self, user_input: str) -> Dict[str, Any]:
        """Main method to run cost estimation workflow with enhanced monitoring"""
        # Start workflow monitoring
        start_workflow_monitoring("cost_estimation")
        workflow_operation_id = start_performance_monitoring("full_workflow")

        initial_state = EstimationState(
            user_input=user_input,
            parsed_services={},
            auto_filled_info=[],
            services_to_add=[],
            current_service_index=0,
            added_services=[],
            failed_services=[],
            estimate_links={},
            final_result={},
            error_message=""
        )

        logger.info(f"🚀 Starting cost estimation for: {user_input[:100]}...")

        try:
            final_state = await self.workflow.ainvoke(initial_state)
            result = final_state.get("final_result", {})

            # End monitoring
            success = result.get("status") == "success"
            end_workflow_monitoring(success=success)
            end_performance_monitoring(workflow_operation_id, success=success,
                                     metadata={"services_added": len(result.get("services_added", []))})

            return result

        except Exception as e:
            error_msg = f"Workflow execution failed: {str(e)}"
            logger.error(f"❌ Workflow error: {e}")

            # End monitoring with error
            end_workflow_monitoring(success=False, error_message=error_msg)
            end_performance_monitoring(workflow_operation_id, success=False, error_message=error_msg)

            return {
                "status": "error",
                "error": error_msg
            }

        finally:
            # Cleanup browser session
            try:
                await self.browser_agent.cleanup_session()
            except Exception as cleanup_error:
                logger.warning(f"⚠️ Browser cleanup warning: {cleanup_error}")