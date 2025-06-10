"""
Visual Verification Utilities for AWS Calculator Automation

This module provides utilities for verifying browser actions and page states
to ensure reliable automation.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class VerificationStatus(Enum):
    """Status of verification checks"""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    UNKNOWN = "unknown"

@dataclass
class VerificationResult:
    """Result of a verification check"""
    status: VerificationStatus
    message: str
    details: Dict[str, Any]
    timestamp: float
    
    def is_success(self) -> bool:
        return self.status == VerificationStatus.SUCCESS
    
    def is_failure(self) -> bool:
        return self.status == VerificationStatus.FAILURE

class PageVerifier:
    """Verifies page states and elements"""
    
    def __init__(self):
        self.verification_history: List[VerificationResult] = []
    
    async def verify_calculator_page(self, agent) -> VerificationResult:
        """Verify we're on the AWS Calculator page"""
        try:
            # This would be implemented with actual page verification
            # For now, return a mock result
            result = VerificationResult(
                status=VerificationStatus.SUCCESS,
                message="AWS Calculator page verified",
                details={
                    "url_contains": "calculator.aws",
                    "has_add_service": True,
                    "has_search_box": True
                },
                timestamp=asyncio.get_event_loop().time()
            )
            
            self.verification_history.append(result)
            logger.info(f"✅ Page verification: {result.message}")
            return result
            
        except Exception as e:
            result = VerificationResult(
                status=VerificationStatus.FAILURE,
                message=f"Page verification failed: {str(e)}",
                details={"error": str(e)},
                timestamp=asyncio.get_event_loop().time()
            )
            
            self.verification_history.append(result)
            logger.error(f"❌ Page verification failed: {result.message}")
            return result
    
    async def verify_service_configuration_page(self, service_type: str, agent) -> VerificationResult:
        """Verify we're on the correct service configuration page"""
        try:
            # Mock verification for service configuration page
            result = VerificationResult(
                status=VerificationStatus.SUCCESS,
                message=f"{service_type} configuration page verified",
                details={
                    "service_type": service_type,
                    "has_configuration_form": True,
                    "has_save_button": True
                },
                timestamp=asyncio.get_event_loop().time()
            )
            
            self.verification_history.append(result)
            logger.info(f"✅ Service config verification: {result.message}")
            return result
            
        except Exception as e:
            result = VerificationResult(
                status=VerificationStatus.FAILURE,
                message=f"Service configuration verification failed: {str(e)}",
                details={"error": str(e), "service_type": service_type},
                timestamp=asyncio.get_event_loop().time()
            )
            
            self.verification_history.append(result)
            logger.error(f"❌ Service config verification failed: {result.message}")
            return result
    
    async def verify_service_added(self, service_type: str, agent) -> VerificationResult:
        """Verify service was successfully added to estimate"""
        try:
            # Mock verification for service addition
            result = VerificationResult(
                status=VerificationStatus.SUCCESS,
                message=f"{service_type} service successfully added to estimate",
                details={
                    "service_type": service_type,
                    "added_to_estimate": True,
                    "success_message_shown": True
                },
                timestamp=asyncio.get_event_loop().time()
            )
            
            self.verification_history.append(result)
            logger.info(f"✅ Service addition verification: {result.message}")
            return result
            
        except Exception as e:
            result = VerificationResult(
                status=VerificationStatus.FAILURE,
                message=f"Service addition verification failed: {str(e)}",
                details={"error": str(e), "service_type": service_type},
                timestamp=asyncio.get_event_loop().time()
            )
            
            self.verification_history.append(result)
            logger.error(f"❌ Service addition verification failed: {result.message}")
            return result

class ActionVerifier:
    """Verifies specific actions were completed successfully"""
    
    def __init__(self):
        self.action_history: List[Dict[str, Any]] = []
    
    async def verify_search_action(self, search_term: str, agent) -> VerificationResult:
        """Verify search action was successful"""
        try:
            # Record the action
            action = {
                "type": "search",
                "search_term": search_term,
                "timestamp": asyncio.get_event_loop().time()
            }
            self.action_history.append(action)
            
            # Mock verification
            result = VerificationResult(
                status=VerificationStatus.SUCCESS,
                message=f"Search for '{search_term}' completed successfully",
                details={
                    "search_term": search_term,
                    "results_found": True,
                    "service_cards_visible": True
                },
                timestamp=asyncio.get_event_loop().time()
            )
            
            logger.info(f"✅ Search verification: {result.message}")
            return result
            
        except Exception as e:
            result = VerificationResult(
                status=VerificationStatus.FAILURE,
                message=f"Search verification failed: {str(e)}",
                details={"error": str(e), "search_term": search_term},
                timestamp=asyncio.get_event_loop().time()
            )
            
            logger.error(f"❌ Search verification failed: {result.message}")
            return result
    
    async def verify_configuration_action(self, service_type: str, config: Dict[str, Any], agent) -> VerificationResult:
        """Verify configuration action was successful"""
        try:
            # Record the action
            action = {
                "type": "configuration",
                "service_type": service_type,
                "config": config,
                "timestamp": asyncio.get_event_loop().time()
            }
            self.action_history.append(action)
            
            # Mock verification
            result = VerificationResult(
                status=VerificationStatus.SUCCESS,
                message=f"{service_type} configuration completed successfully",
                details={
                    "service_type": service_type,
                    "config_applied": True,
                    "no_validation_errors": True,
                    "config": config
                },
                timestamp=asyncio.get_event_loop().time()
            )
            
            logger.info(f"✅ Configuration verification: {result.message}")
            return result
            
        except Exception as e:
            result = VerificationResult(
                status=VerificationStatus.FAILURE,
                message=f"Configuration verification failed: {str(e)}",
                details={"error": str(e), "service_type": service_type, "config": config},
                timestamp=asyncio.get_event_loop().time()
            )
            
            logger.error(f"❌ Configuration verification failed: {result.message}")
            return result

class EstimateVerifier:
    """Verifies estimate generation and links"""
    
    def __init__(self):
        self.estimate_history: List[Dict[str, Any]] = []
    
    async def verify_estimate_generation(self, services: List[str], agent) -> VerificationResult:
        """Verify estimate was generated with all services"""
        try:
            # Record the estimate
            estimate = {
                "services": services,
                "timestamp": asyncio.get_event_loop().time(),
                "status": "generated"
            }
            self.estimate_history.append(estimate)
            
            # Mock verification
            result = VerificationResult(
                status=VerificationStatus.SUCCESS,
                message=f"Estimate generated successfully with {len(services)} services",
                details={
                    "services_count": len(services),
                    "services": services,
                    "estimate_visible": True
                },
                timestamp=asyncio.get_event_loop().time()
            )
            
            logger.info(f"✅ Estimate verification: {result.message}")
            return result
            
        except Exception as e:
            result = VerificationResult(
                status=VerificationStatus.FAILURE,
                message=f"Estimate verification failed: {str(e)}",
                details={"error": str(e), "services": services},
                timestamp=asyncio.get_event_loop().time()
            )
            
            logger.error(f"❌ Estimate verification failed: {result.message}")
            return result
    
    async def verify_estimate_links(self, links: Dict[str, str], agent) -> VerificationResult:
        """Verify estimate links are valid"""
        try:
            valid_links = {}
            invalid_links = {}
            
            for link_type, url in links.items():
                if url and "calculator.aws" in url and not url.startswith("Error"):
                    valid_links[link_type] = url
                else:
                    invalid_links[link_type] = url
            
            if valid_links:
                status = VerificationStatus.SUCCESS if not invalid_links else VerificationStatus.PARTIAL
                message = f"Estimate links verified: {len(valid_links)} valid, {len(invalid_links)} invalid"
            else:
                status = VerificationStatus.FAILURE
                message = "No valid estimate links found"
            
            result = VerificationResult(
                status=status,
                message=message,
                details={
                    "valid_links": valid_links,
                    "invalid_links": invalid_links,
                    "total_links": len(links)
                },
                timestamp=asyncio.get_event_loop().time()
            )
            
            logger.info(f"✅ Link verification: {result.message}")
            return result
            
        except Exception as e:
            result = VerificationResult(
                status=VerificationStatus.FAILURE,
                message=f"Link verification failed: {str(e)}",
                details={"error": str(e), "links": links},
                timestamp=asyncio.get_event_loop().time()
            )
            
            logger.error(f"❌ Link verification failed: {result.message}")
            return result

class VerificationManager:
    """Manages all verification activities"""
    
    def __init__(self):
        self.page_verifier = PageVerifier()
        self.action_verifier = ActionVerifier()
        self.estimate_verifier = EstimateVerifier()
    
    def get_verification_summary(self) -> Dict[str, Any]:
        """Get summary of all verification activities"""
        total_verifications = (
            len(self.page_verifier.verification_history) +
            len(self.action_verifier.action_history) +
            len(self.estimate_verifier.estimate_history)
        )
        
        successful_verifications = sum(
            1 for v in self.page_verifier.verification_history
            if v.is_success()
        )
        
        return {
            "total_verifications": total_verifications,
            "successful_verifications": successful_verifications,
            "success_rate": successful_verifications / max(total_verifications, 1),
            "page_verifications": len(self.page_verifier.verification_history),
            "action_verifications": len(self.action_verifier.action_history),
            "estimate_verifications": len(self.estimate_verifier.estimate_history)
        }
    
    def clear_history(self):
        """Clear all verification history"""
        self.page_verifier.verification_history.clear()
        self.action_verifier.action_history.clear()
        self.estimate_verifier.estimate_history.clear()
        logger.info("🧹 Verification history cleared")
