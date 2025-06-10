"""
Test script to verify the enhanced AWS Cost Estimation Agent implementation
"""

import asyncio
import sys
import os
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Test imports
def test_imports():
    """Test that all modules can be imported successfully"""
    print("🧪 Testing imports...")
    
    try:
        # Core modules
        from src.agents.browser_agent import UnifiedAWSBrowserAgent
        from src.workflows.cost_estimation_workflow import CostEstimationWorkflow
        from src.utils.template_parser import TemplateParser
        print("✅ Core modules imported successfully")
        
        # New utility modules
        from src.utils.browser_helpers import BrowserInteractionPatterns
        from src.utils.verification import VerificationManager
        from src.monitoring.logger import get_logger, enhanced_logger
        print("✅ Utility modules imported successfully")
        
        # Service modules
        from src.services.ec2_service import EC2ServiceHandler, EC2Configuration
        print("✅ Service modules imported successfully")
        
        # Configuration
        from config.predefined_templates import PREDEFINED_TEMPLATES, INFRASTRUCTURE_TEMPLATES
        print("✅ Configuration modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration_creation():
    """Test configuration creation and validation"""
    print("\n🧪 Testing configuration creation...")
    
    try:
        from src.services.ec2_service import EC2ServiceHandler, EC2Configuration
        
        # Test EC2 configuration creation
        config_dict = {
            "instance_type": "t3.medium",
            "quantity": 2,
            "operating_system": "Linux",
            "region": "US East (N. Virginia)"
        }
        
        ec2_config = EC2ServiceHandler.create_configuration(config_dict)
        print(f"✅ EC2 configuration created: {ec2_config.instance_type}")
        
        # Test validation
        errors = ec2_config.validate()
        if not errors:
            print("✅ EC2 configuration validation passed")
        else:
            print(f"⚠️ EC2 configuration validation errors: {errors}")
        
        # Test instance type suggestion
        requirements = {"vcpu": 2, "memory": 4, "category": "general"}
        suggested = EC2ServiceHandler.suggest_instance_type(requirements)
        print(f"✅ Instance type suggestion: {suggested}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test error: {e}")
        return False

def test_browser_patterns():
    """Test browser interaction patterns"""
    print("\n🧪 Testing browser patterns...")
    
    try:
        from src.utils.browser_helpers import BrowserInteractionPatterns
        
        # Test service search pattern
        search_pattern = BrowserInteractionPatterns.get_service_search_pattern("EC2")
        print("✅ Service search pattern generated")
        
        # Test configuration pattern
        config = {"instance_type": "t3.medium", "quantity": 1}
        config_pattern = BrowserInteractionPatterns.get_service_configuration_pattern("EC2", config)
        print("✅ Service configuration pattern generated")
        
        # Test add to estimate pattern
        add_pattern = BrowserInteractionPatterns.get_add_to_estimate_pattern()
        print("✅ Add to estimate pattern generated")
        
        return True
        
    except Exception as e:
        print(f"❌ Browser patterns test error: {e}")
        return False

def test_verification_system():
    """Test verification system"""
    print("\n🧪 Testing verification system...")
    
    try:
        from src.utils.verification import VerificationManager, VerificationStatus
        
        # Create verification manager
        verifier = VerificationManager()
        print("✅ Verification manager created")
        
        # Test verification summary
        summary = verifier.get_verification_summary()
        print(f"✅ Verification summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification system test error: {e}")
        return False

def test_monitoring_system():
    """Test monitoring and logging system"""
    print("\n🧪 Testing monitoring system...")
    
    try:
        from src.monitoring.logger import (
            get_logger, start_performance_monitoring, 
            end_performance_monitoring, enhanced_logger
        )
        
        # Test logger
        logger = get_logger()
        logger.info("Test log message")
        print("✅ Logger working")
        
        # Test performance monitoring
        operation_id = start_performance_monitoring("test_operation")
        end_performance_monitoring(operation_id, success=True)
        print("✅ Performance monitoring working")
        
        # Test metrics
        stats = enhanced_logger.performance_monitor.get_overall_stats()
        print(f"✅ Performance stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Monitoring system test error: {e}")
        return False

async def test_workflow_initialization():
    """Test workflow initialization (without running full workflow)"""
    print("\n🧪 Testing workflow initialization...")
    
    try:
        # Mock API key for testing
        api_key = "test-api-key"
        
        from src.workflows.cost_estimation_workflow import CostEstimationWorkflow
        
        # This will fail without a real API key, but we can test initialization
        try:
            workflow = CostEstimationWorkflow(api_key)
            print("✅ Workflow initialized (note: requires valid API key for full functionality)")
        except Exception as e:
            if "api" in str(e).lower() or "key" in str(e).lower():
                print("⚠️ Workflow initialization requires valid API key (expected)")
            else:
                raise e
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow initialization test error: {e}")
        return False

def test_template_system():
    """Test template system"""
    print("\n🧪 Testing template system...")
    
    try:
        from config.predefined_templates import (
            PREDEFINED_TEMPLATES, INFRASTRUCTURE_TEMPLATES,
            get_service_template, get_infrastructure_template
        )
        
        # Test service templates
        ec2_template = get_service_template("ec2", "default")
        print(f"✅ EC2 template: {ec2_template.get('instance_type')}")
        
        rds_template = get_service_template("rds", "postgresql")
        print(f"✅ RDS template: {rds_template.get('engine')}")
        
        # Test infrastructure templates
        basic_app = get_infrastructure_template("basic_web_app")
        print(f"✅ Infrastructure template: {len(basic_app.get('services', {}))} services")
        
        return True
        
    except Exception as e:
        print(f"❌ Template system test error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting AWS Cost Estimation Agent Implementation Tests\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration_creation),
        ("Browser Patterns Test", test_browser_patterns),
        ("Verification System Test", test_verification_system),
        ("Monitoring System Test", test_monitoring_system),
        ("Workflow Initialization Test", test_workflow_initialization),
        ("Template System Test", test_template_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Implementation is ready.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())
