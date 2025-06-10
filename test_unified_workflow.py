"""
Test script for unified workflow approach
"""

import asyncio
import sys
import os
from typing import Dict, Any

# Add src to path
sys.path.append('src')

from workflows.cost_estimation_workflow import CostEstimationWorkflow

async def test_unified_workflow():
    """Test the unified workflow with multiple services"""
    
    print("🚀 Testing Unified AWS Cost Estimation Workflow")
    print("=" * 60)
    
    # Test configuration
    test_cases = [
        {
            "name": "Single EC2 Service",
            "input": "I need 1 EC2 instance t3.medium for web server",
            "expected_services": ["ec2"]
        },
        {
            "name": "Multiple Services - Web App",
            "input": "I need a web application with 2 EC2 instances t3.medium, RDS PostgreSQL database, and S3 storage for files",
            "expected_services": ["ec2", "rds", "s3"]
        },
        {
            "name": "Complete Infrastructure",
            "input": "I need complete infrastructure: VPC, 3 EC2 instances t3.large, RDS MySQL, S3 bucket, and Load Balancer",
            "expected_services": ["vpc", "ec2", "rds", "s3", "load_balancer"]
        }
    ]
    
    # Initialize workflow (requires OpenAI API key)
    try:
        # Check for API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️ OPENAI_API_KEY not found in environment variables")
            print("📝 Testing workflow structure only (no actual browser automation)")
            
            # Test workflow structure without API key
            workflow = CostEstimationWorkflow("dummy_key")
            print("✅ Workflow structure initialized successfully")
            
            # Test task building
            print("\n🧪 Testing task building...")
            
            # Mock services config
            test_services = {
                "ec2": {
                    "instance_type": "t3.medium",
                    "quantity": 2,
                    "operating_system": "Linux"
                },
                "rds": {
                    "engine": "PostgreSQL",
                    "instance_class": "db.t3.small"
                },
                "s3": {
                    "storage_amount": 500,
                    "storage_class": "Standard"
                }
            }
            
            # Test task generation
            task = workflow.browser_agent._build_complete_workflow_task(test_services)
            
            print(f"✅ Generated task length: {len(task)} characters")
            print(f"✅ Task contains all services: {all(service in task for service in test_services.keys())}")
            
            # Show task preview
            print("\n📋 Task Preview (first 500 chars):")
            print("-" * 50)
            print(task[:500] + "..." if len(task) > 500 else task)
            print("-" * 50)
            
            return True
            
        else:
            print(f"✅ Found OpenAI API key: {api_key[:10]}...")
            workflow = CostEstimationWorkflow(api_key)
            print("✅ Workflow initialized with real API key")
            
            # Test each case
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n🧪 Test Case {i}: {test_case['name']}")
                print(f"📝 Input: {test_case['input']}")
                print(f"🎯 Expected services: {test_case['expected_services']}")
                
                try:
                    # Run estimation (this will actually execute browser automation)
                    print("⚠️ WARNING: This will open browser and execute real automation!")
                    confirm = input("Continue? (y/N): ").lower().strip()
                    
                    if confirm != 'y':
                        print("⏭️ Skipping browser automation test")
                        continue
                    
                    print("🌐 Starting browser automation...")
                    result = await workflow.run_estimation(test_case['input'])
                    
                    print(f"📊 Result: {result.get('status', 'unknown')}")
                    
                    if result.get('status') == 'success':
                        print(f"✅ Services added: {result.get('services_added', [])}")
                        print(f"🔗 Estimate links: {result.get('estimate_links', {})}")
                    else:
                        print(f"❌ Error: {result.get('error', 'Unknown error')}")
                    
                except Exception as e:
                    print(f"❌ Test case failed: {e}")
                
                print("-" * 60)
            
            return True
            
    except Exception as e:
        print(f"❌ Workflow initialization failed: {e}")
        return False

async def test_task_generation():
    """Test task generation without browser automation"""
    print("\n🧪 Testing Task Generation")
    print("=" * 40)
    
    # Mock browser agent for testing
    from agents.browser_agent import UnifiedAWSBrowserAgent
    
    agent = UnifiedAWSBrowserAgent("dummy_key")
    
    # Test different service combinations
    test_configs = [
        {
            "name": "Single EC2",
            "config": {
                "ec2": {
                    "instance_type": "t3.medium",
                    "quantity": 1
                }
            }
        },
        {
            "name": "EC2 + RDS",
            "config": {
                "ec2": {
                    "instance_type": "t3.large",
                    "quantity": 2
                },
                "rds": {
                    "engine": "MySQL",
                    "instance_class": "db.t3.medium"
                }
            }
        },
        {
            "name": "Full Stack",
            "config": {
                "vpc": {},
                "ec2": {
                    "instance_type": "t3.xlarge",
                    "quantity": 3
                },
                "rds": {
                    "engine": "PostgreSQL",
                    "instance_class": "db.r5.large"
                },
                "s3": {
                    "storage_amount": 1000,
                    "storage_class": "Standard"
                },
                "load_balancer": {}
            }
        }
    ]
    
    for test_config in test_configs:
        print(f"\n📋 Testing: {test_config['name']}")
        print(f"🔧 Services: {list(test_config['config'].keys())}")
        
        task = agent._build_complete_workflow_task(test_config['config'])
        
        # Analyze task
        service_count = len(test_config['config'])
        task_length = len(task)
        
        print(f"✅ Task generated: {task_length} characters")
        print(f"✅ Service count: {service_count}")
        
        # Check if all services are mentioned
        all_mentioned = all(service in task.lower() for service in test_config['config'].keys())
        print(f"✅ All services mentioned: {all_mentioned}")
        
        # Show key sections
        if "PHASE 1" in task:
            print("✅ Contains PHASE 1: Initial Setup")
        if "PHASE 2" in task:
            print("✅ Contains PHASE 2: Service Addition")
        if "PHASE 3" in task:
            print("✅ Contains PHASE 3: Finalization")
        
        print("-" * 40)

def main():
    """Main test function"""
    print("🎯 AWS Cost Estimation - Unified Workflow Tests")
    print("=" * 60)
    
    # Test task generation first (no API key needed)
    asyncio.run(test_task_generation())
    
    # Test full workflow (may need API key)
    asyncio.run(test_unified_workflow())
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
