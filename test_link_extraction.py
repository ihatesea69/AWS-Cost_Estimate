"""
Test script for real link extraction functionality
"""

import sys
import os

# Add src to path
sys.path.append('src')

from agents.browser_agent import UnifiedAWSBrowserAgent

def test_link_extraction():
    """Test the link extraction functionality"""
    
    print("🧪 Testing Real Link Extraction")
    print("=" * 50)
    
    # Initialize agent
    agent = UnifiedAWSBrowserAgent("dummy_key")
    
    # Test cases with different result formats
    test_cases = [
        {
            "name": "Real AWS Calculator Result",
            "result": """
            The AWS Pricing Calculator estimate has been successfully created with the following details:
            - Services Added: Amazon EC2, Amazon RDS, Amazon S3
            - Total Estimated Cost for 12 Months: $5,233.20
            - Public Share Link: https://calculator.aws/#/estimate?id=aa974c722a9a9925f29592d2ead3c5fd5d46c106
            
            The task is complete.
            """,
            "expected": "https://calculator.aws/#/estimate?id=aa974c722a9a9925f29592d2ead3c5fd5d46c106"
        },
        {
            "name": "Alternative Format",
            "result": "calculator.aws/#/estimate?id=bb123456789abcdef123456789abcdef12345678",
            "expected": "https://calculator.aws/#/estimate?id=bb123456789abcdef123456789abcdef12345678"
        },
        {
            "name": "Short Format",
            "result": "estimate?id=cc987654321fedcba987654321fedcba98765432",
            "expected": "https://calculator.aws/#/estimate?id=cc987654321fedcba987654321fedcba98765432"
        },
        {
            "name": "No Link",
            "result": "Task completed but no estimate link found",
            "expected": None
        },
        {
            "name": "Multiple Links",
            "result": """
            First link: https://calculator.aws/#/estimate?id=dd111111111111111111111111111111111111111
            Second link: https://calculator.aws/#/estimate?id=ee222222222222222222222222222222222222222
            Final link: https://calculator.aws/#/estimate?id=ff333333333333333333333333333333333333333
            """,
            "expected": "https://calculator.aws/#/estimate?id=ff333333333333333333333333333333333333333"
        }
    ]
    
    # Test each case
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['name']}")
        print(f"📝 Input: {test_case['result'][:100]}...")
        print(f"🎯 Expected: {test_case['expected']}")
        
        # Extract link
        extracted = agent._extract_estimate_link_from_result(test_case['result'])
        
        print(f"🔗 Extracted: {extracted}")
        
        # Check result
        if extracted == test_case['expected']:
            print("✅ PASS")
        else:
            print("❌ FAIL")
        
        print("-" * 50)
    
    print("\n🎉 Link extraction tests completed!")

def test_workflow_result_format():
    """Test how the workflow result should be formatted"""
    
    print("\n🧪 Testing Workflow Result Format")
    print("=" * 50)
    
    # Mock a successful workflow result
    mock_result = {
        "status": "success",
        "services_added": ["ec2", "rds", "s3"],
        "services_count": 3,
        "workflow_duration": "360s max",
        "estimate_links": {
            "ondemand": "https://calculator.aws/#/estimate?id=test123456789abcdef",
            "savings_plan": "https://calculator.aws/#/estimate?id=test123456789abcdef",
            "reserved": "https://calculator.aws/#/estimate?id=test123456789abcdef",
            "real_link": "https://calculator.aws/#/estimate?id=test123456789abcdef"
        },
        "timestamp": 1749529655,
        "agent_result": "Task completed successfully with estimate link: https://calculator.aws/#/estimate?id=test123456789abcdef"
    }
    
    print("📊 Mock Workflow Result:")
    print(f"✅ Status: {mock_result['status']}")
    print(f"📋 Services: {mock_result['services_added']}")
    print(f"🔗 Real Link: {mock_result['estimate_links']['real_link']}")
    print(f"⏱️ Duration: {mock_result['workflow_duration']}")
    
    # Check if real link is properly formatted
    real_link = mock_result['estimate_links'].get('real_link')
    if real_link and "estimate?id=" in real_link:
        print("✅ Real link format is correct")
    else:
        print("❌ Real link format is incorrect")
    
    print("\n🎉 Workflow result format test completed!")

def main():
    """Main test function"""
    print("🎯 Real Link Extraction Tests")
    print("=" * 60)
    
    test_link_extraction()
    test_workflow_result_format()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
