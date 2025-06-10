import re
import json
from typing import Dict, List, Any, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from config.predefined_templates import get_service_template, get_infrastructure_template, PREDEFINED_TEMPLATES

class TemplateParser:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_api_key,
            temperature=0.1
        )
    
    async def parse_user_requirement(self, user_input: str) -> Tuple[Dict[str, Any], List[str]]:
        """
        Parse user input và trả về configuration + list các thông tin được auto-fill
        """
        system_prompt = """
        You are an AWS cost estimation expert. Analyze user requirements and return ONLY a valid JSON response.

        IMPORTANT: Return ONLY JSON format, no other text or explanation.

        JSON structure:
        {
            "services": {
                "ec2": {
                    "instance_type": "t3.medium",
                    "quantity": 2,
                    "operating_system": "Linux",
                    "storage_type": "gp3",
                    "storage_size": "20",
                    "storage_unit": "GB"
                },
                "rds": {
                    "engine": "PostgreSQL",
                    "instance_class": "db.t3.small",
                    "deployment": "Single-AZ"
                },
                "s3": {
                    "storage_amount": 500,
                    "storage_unit": "GB",
                    "storage_class": "Standard"
                }
            },
            "auto_filled": [
                "EC2: storage_type = gp3 (from default template)",
                "RDS: instance_class = db.t3.small (from postgresql template)"
            ]
        }

        Service types: ec2, rds, s3, vpc, load_balancer
        """
        
        user_prompt = f"""
        User requirement: {user_input}
        
        Available templates:
        - EC2: {list(PREDEFINED_TEMPLATES['ec2'].keys())}
        - RDS: {list(PREDEFINED_TEMPLATES['rds'].keys())}
        - S3: {list(PREDEFINED_TEMPLATES['s3'].keys())}
        - VPC: available
        - Load Balancer: available
        
        Hãy phân tích và trả về JSON configuration.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        try:
            print(f"🔍 Raw LLM response: {response.content}")
            
            # Clean up response content để tìm JSON
            content = response.content.strip()
            
            # Tìm JSON block trong response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = content[json_start:json_end]
                print(f"🔍 Extracted JSON: {json_content}")
                
                # Parse JSON response
                result = json.loads(json_content)
                services = result.get('services', {})
                auto_filled = result.get('auto_filled', [])
                
                # Merge với predefined templates
                merged_services = self._merge_with_templates(services)
                
                return merged_services, auto_filled
            else:
                # Fallback: Manual parsing nếu không có JSON
                print("⚠️ No JSON found, using manual parsing...")
                return self._manual_parse_fallback(user_input)
            
        except Exception as e:
            print(f"❌ Error parsing LLM response: {e}")
            print(f"❌ Response content was: {response.content}")
            # Fallback: Manual parsing
            return self._manual_parse_fallback(user_input)
    
    def _merge_with_templates(self, services: Dict[str, Any]) -> Dict[str, Any]:
        """Merge user requirements với predefined templates"""
        merged = {}
        
        for service_type, config in services.items():
            if service_type in PREDEFINED_TEMPLATES:
                # Lấy template phù hợp nhất
                template = self._get_best_template(service_type, config)
                
                # Merge config với template
                merged_config = {**template, **config}
                merged[service_type] = merged_config
            else:
                merged[service_type] = config
        
        return merged
    
    def _get_best_template(self, service_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Chọn template phù hợp nhất dựa trên config"""
        templates = PREDEFINED_TEMPLATES[service_type]
        
        # Logic để chọn template tốt nhất
        if service_type == "ec2":
            if config.get("quantity", 1) > 1:
                return templates.get("web_server", templates["default"])
            return templates["default"]
        
        elif service_type == "rds":
            engine = config.get("engine", "").lower()
            if "postgres" in engine:
                return templates["postgresql"]
            return templates["default"]
        
        return templates.get("default", {})
    
    def extract_services_from_text(self, text: str) -> List[str]:
        """Extract AWS services mentioned trong text"""
        services = []
        text_lower = text.lower()
        
        service_keywords = {
            "ec2": ["ec2", "instance", "server", "compute"],
            "rds": ["rds", "database", "db", "mysql", "postgres", "postgresql"],
            "s3": ["s3", "storage", "bucket"],
            "vpc": ["vpc", "network", "nat"],
            "load_balancer": ["load balancer", "alb", "elb", "balancer"]
        }
        
        for service, keywords in service_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                services.append(service)
        
        return list(set(services))  # Remove duplicates
    
    def validate_configuration(self, services: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate configuration trước khi gửi tới calculator"""
        errors = []
        
        for service_type, config in services.items():
            if service_type == "ec2":
                if not config.get("instance_type"):
                    errors.append("EC2: Missing instance_type")
                if not config.get("quantity") or config["quantity"] < 1:
                    errors.append("EC2: Invalid quantity")
            
            elif service_type == "rds":
                if not config.get("engine"):
                    errors.append("RDS: Missing engine")
                if not config.get("instance_class"):
                    errors.append("RDS: Missing instance_class")
        
        return len(errors) == 0, errors 
    
    def _manual_parse_fallback(self, user_input: str) -> Tuple[Dict[str, Any], List[str]]:
        """Manual parsing fallback khi LLM response không valid"""
        services = {}
        auto_filled = []
        
        text_lower = user_input.lower()
        
        # Parse EC2
        if any(keyword in text_lower for keyword in ["ec2", "instance", "server"]):
            ec2_config = get_service_template("ec2", "default")
            
            # Extract instance type
            instance_match = re.search(r'(t3\.|t2\.|m5\.|c5\.|r5\.)\w+', text_lower)
            if instance_match:
                ec2_config["instance_type"] = instance_match.group(0)
            
            # Extract quantity  
            quantity_match = re.search(r'(\d+)\s*(ec2|instance)', text_lower)
            if quantity_match:
                ec2_config["quantity"] = int(quantity_match.group(1))
            
            services["ec2"] = ec2_config
            auto_filled.append("EC2: Using default template with detected parameters")
        
        # Parse RDS
        if any(keyword in text_lower for keyword in ["rds", "database", "postgres", "mysql"]):
            if "postgres" in text_lower:
                rds_config = get_service_template("rds", "postgresql")
                auto_filled.append("RDS: Using PostgreSQL template")
            else:
                rds_config = get_service_template("rds", "default")
                auto_filled.append("RDS: Using default template")
            
            services["rds"] = rds_config
        
        # Parse S3
        if any(keyword in text_lower for keyword in ["s3", "storage", "bucket"]):
            s3_config = get_service_template("s3", "default")
            
            # Extract storage amount
            storage_match = re.search(r'(\d+)\s*(gb|tb)', text_lower)
            if storage_match:
                amount = int(storage_match.group(1))
                unit = storage_match.group(2).upper()
                s3_config["storage_amount"] = amount
                s3_config["storage_unit"] = unit
            
            services["s3"] = s3_config
            auto_filled.append("S3: Using default template with detected storage amount")
        
        # Parse Load Balancer
        if any(keyword in text_lower for keyword in ["load balancer", "alb", "balancer"]):
            lb_config = get_service_template("load_balancer", "default")
            services["load_balancer"] = lb_config
            auto_filled.append("Load Balancer: Using default ALB template")
        
        # Parse VPC
        if any(keyword in text_lower for keyword in ["vpc", "network", "nat"]):
            vpc_config = get_service_template("vpc", "default")
            services["vpc"] = vpc_config
            auto_filled.append("VPC: Using default template with NAT Gateway")
        
        return services, auto_filled