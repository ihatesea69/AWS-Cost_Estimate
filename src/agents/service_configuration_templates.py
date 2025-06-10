"""
Service Configuration Templates
Chi tiết về các bước cấu hình cho từng AWS service trong calculator
"""

from typing import Dict, Any, List

class ServiceConfigurationTemplate:
    """Base class cho service configuration templates"""
    
    def __init__(self):
        self.configuration_steps = []
    
    def get_configuration_steps(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trả về list các bước configuration chi tiết"""
        return self.configuration_steps

class EC2ConfigurationTemplate(ServiceConfigurationTemplate):
    """Template configuration cho EC2 service với 12 bước chi tiết"""
    
    def __init__(self):
        super().__init__()
        # 12 bước cấu hình EC2 theo AWS Calculator
        self.configuration_steps = [
            {
                "step": "f1_select_location_type",
                "description": "F.1 Chọn loại vị trí",
                "action": "select_option",
                "target": "location_type_dropdown",
                "options": ["Region", "Local Zone", "Wavelength Zone"],
                "placeholder": "Region",
                "note": "Lựa chọn dựa trên nhu cầu về độ trễ, chi phí, dịch vụ có hỗ trợ"
            },
            {
                "step": "f2_select_region",
                "description": "F.2 Chọn Region",
                "action": "select_option",
                "target": "region_dropdown",
                "placeholder": "US East (N. Virginia)",
                "note": "Xác định khu vực cụ thể triển khai"
            },
            {
                "step": "f3_select_tenancy",
                "description": "F.3 Tenancy (Kiểu triển khai)",
                "action": "select_option",
                "target": "tenancy_dropdown",
                "options": ["Shared Instance", "Dedicated Instance", "Dedicated Host"],
                "placeholder": "Shared Instance",
                "note": "Shared: phổ thông, Dedicated: compliance, Host: kiểm soát vật lý"
            },
            {
                "step": "f4_select_operating_system",
                "description": "F.4 Hệ điều hành",
                "action": "select_option",
                "target": "os_dropdown",
                "options": ["Linux", "Windows", "RHEL", "SUSE"],
                "placeholder": "Linux"
            },
            {
                "step": "f5_select_workload_type",
                "description": "F.5 Loại tải công việc",
                "action": "select_option",
                "target": "workload_dropdown",
                "options": ["Consistent Usage", "Daily spike traffic", "Weekly spike traffic", "Monthly spike traffic"],
                "placeholder": "Consistent Usage",
                "note": "Sử dụng liên tục hoặc cao điểm theo chu kỳ"
            },
            {
                "step": "f6_set_instance_quantity",
                "description": "F.6 Số lượng instance",
                "action": "input_number",
                "target": "quantity_field",
                "placeholder": "1",
                "validation": "positive_integer"
            },
            {
                "step": "f7_select_instance_type",
                "description": "F.7 Loại instance",
                "action": "complex_instance_selection",
                "target": "instance_type_section",
                "placeholder": "t3.medium",
                "note": "Chọn theo family, vCPU, RAM, hiệu năng mạng - PHỨC TẠP",
                "complexity": "high"
            },
            {
                "step": "f8_select_pricing_model",
                "description": "F.8 Lựa chọn thanh toán",
                "action": "select_pricing_option",
                "target": "pricing_section",
                "options": [
                    "On-demand",
                    "Compute Savings Plans",
                    "EC2 Instance Savings Plans", 
                    "Spot Instances",
                    "Standard Reserved Instances",
                    "Convertible Reserved Instances"
                ],
                "placeholder": "On-demand",
                "note": "Cam kết 1-3 năm cho Savings Plans/Reserved, trả trước 0/một phần/toàn bộ"
            },
            {
                "step": "f9_configure_ebs_optional",
                "description": "F.9 EBS (tuỳ chọn)",
                "action": "configure_ebs_storage",
                "target": "ebs_section",
                "optional": True,
                "placeholder": {"type": "gp3", "size": "20", "unit": "GB", "iops": "3000"},
                "note": "Loại ổ lưu trữ, số IOPS mỗi volume"
            },
            {
                "step": "f10_configure_monitoring_optional",
                "description": "F.10 Monitoring (tuỳ chọn)",
                "action": "configure_monitoring",
                "target": "monitoring_section",
                "optional": True,
                "placeholder": {"enabled": False, "detailed": False},
                "note": "Tùy theo số lượng instance và số metrics"
            },
            {
                "step": "f11_configure_data_transfer_optional",
                "description": "F.11 Truyền dữ liệu (tuỳ chọn)",
                "action": "configure_data_transfer",
                "target": "data_transfer_section",
                "optional": True,
                "placeholder": {"outbound": "0", "inbound": "0", "unit": "GB"},
                "note": "Data transfer in/out"
            },
            {
                "step": "f12_additional_costs_optional",
                "description": "F.12 Chi phí bổ sung (tuỳ chọn)",
                "action": "configure_additional_costs",
                "target": "additional_costs_section",
                "optional": True,
                "placeholder": {"elastic_ip": False, "load_balancer": False},
                "note": "Elastic IP, Load Balancer, etc."
            }
        ]

class RDSConfigurationTemplate(ServiceConfigurationTemplate):
    """Template configuration cho RDS service"""
    
    def __init__(self):
        super().__init__()
        # Sẽ được bổ sung chi tiết các bước configuration RDS
        self.configuration_steps = [
            {
                "step": "select_region",
                "description": "Chọn AWS Region",
                "action": "click_dropdown",
                "target": "region_dropdown",
                "placeholder": "US East (N. Virginia)"
            },
            {
                "step": "select_engine",
                "description": "Chọn Database Engine",
                "action": "select_option",
                "target": "engine_dropdown",
                "placeholder": "MySQL"
            },
            {
                "step": "select_instance_class",
                "description": "Chọn DB Instance Class",
                "action": "search_and_select",
                "target": "instance_class_field",
                "placeholder": "db.t3.micro"
            },
            {
                "step": "select_deployment",
                "description": "Chọn Deployment Option",
                "action": "select_option",
                "target": "deployment_dropdown",
                "placeholder": "Single-AZ"
            },
            {
                "step": "configure_storage",
                "description": "Cấu hình Database Storage",
                "action": "configure_storage_section",
                "target": "storage_section",
                "placeholder": {"type": "gp3", "size": "20", "unit": "GB"}
            }
        ]

class S3ConfigurationTemplate(ServiceConfigurationTemplate):
    """Template configuration cho S3 service với các bước chi tiết"""
    
    def __init__(self):
        super().__init__()
        # Chi tiết cấu hình S3 theo AWS Calculator
        self.configuration_steps = [
            {
                "step": "s3_1_select_location_type",
                "description": "S3.1 Chọn loại vị trí",
                "action": "select_option",
                "target": "location_type_dropdown",
                "options": ["Region"],
                "placeholder": "Region",
                "note": "S3 chủ yếu sử dụng Region"
            },
            {
                "step": "s3_2_select_region", 
                "description": "S3.2 Chọn Region",
                "action": "select_option",
                "target": "region_dropdown",
                "placeholder": "US East (Ohio)",
                "note": "Chọn region gần users để giảm latency"
            },
            {
                "step": "s3_3_select_storage_classes",
                "description": "S3.3 Select S3 Storage classes and features",
                "action": "multi_select_storage_classes",
                "target": "storage_classes_section",
                "options": [
                    "S3 Standard",
                    "S3 Intelligent - Tiering", 
                    "S3 Standard - Infrequent Access",
                    "S3 One Zone - Infrequent Access",
                    "S3 Glacier Flexible Retrieval",
                    "S3 Glacier Deep Archive",
                    "S3 Management and Insights",
                    "S3 Object Lambda",
                    "S3 Glacier Instant Retrieval",
                    "Data Transfer",
                    "S3 Express One Zone",
                    "S3 Access Grants"
                ],
                "placeholder": ["S3 Standard"],
                "note": "Chọn các storage classes cần estimate"
            },
            {
                "step": "s3_4_configure_s3_standard",
                "description": "S3.4 Configure S3 Standard feature",
                "action": "configure_s3_standard_section",
                "target": "s3_standard_section",
                "sub_steps": [
                    {
                        "sub_step": "s3_standard_storage_amount",
                        "description": "S3 Standard storage amount",
                        "action": "input_with_unit",
                        "target": "storage_amount_field",
                        "placeholder": {"amount": "100", "unit": "GB per month"}
                    },
                    {
                        "sub_step": "s3_data_movement_method",
                        "description": "How will data be moved into S3 Standard?",
                        "action": "select_option",
                        "target": "data_movement_dropdown",
                        "options": [
                            "Automatically calculates PUT, COPY, POST costs",
                            "The specified amount of data is already stored in S3 Standard"
                        ],
                        "placeholder": "Automatically calculates PUT, COPY, POST costs"
                    },
                    {
                        "sub_step": "s3_put_copy_post_requests",
                        "description": "PUT, COPY, POST, LIST requests to S3 Standard",
                        "action": "input_number",
                        "target": "put_requests_field",
                        "placeholder": "1000",
                        "note": "Ongoing monthly number of PUT, COPY, POST or LIST requests"
                    },
                    {
                        "sub_step": "s3_get_select_requests", 
                        "description": "GET, SELECT, and all other requests from S3 Standard",
                        "action": "input_number",
                        "target": "get_requests_field",
                        "placeholder": "10000",
                        "note": "Ongoing monthly number of GET, SELECT and all other requests"
                    },
                    {
                        "sub_step": "s3_data_returned_by_select",
                        "description": "Data returned by S3 Select",
                        "action": "input_with_unit",
                        "target": "data_returned_field",
                        "placeholder": {"amount": "0", "unit": "GB per month"},
                        "note": "Ongoing monthly volume of data returned by S3 Select requests"
                    },
                    {
                        "sub_step": "s3_data_scanned_by_select",
                        "description": "Data scanned by S3 Select", 
                        "action": "input_with_unit",
                        "target": "data_scanned_field",
                        "placeholder": {"amount": "0", "unit": "GB per month"},
                        "note": "Ongoing monthly volume of data scanned by S3 Select requests"
                    }
                ]
            },
            {
                "step": "s3_5_configure_data_transfer",
                "description": "S3.5 Configure Data Transfer feature",
                "action": "configure_data_transfer_section",
                "target": "data_transfer_section",
                "sub_steps": [
                    {
                        "sub_step": "s3_inbound_data_transfer",
                        "description": "Inbound Data Transfer",
                        "action": "configure_inbound_transfer",
                        "target": "inbound_transfer_section",
                        "note": "Enter data transfer into the region",
                        "fields": [
                            {
                                "field": "data_transfer_from",
                                "placeholder": "Internet"
                            },
                            {
                                "field": "amount",
                                "placeholder": {"amount": "0", "unit": "TB per month"}
                            }
                        ]
                    },
                    {
                        "sub_step": "s3_outbound_data_transfer",
                        "description": "Outbound Data Transfer",
                        "action": "configure_outbound_transfer", 
                        "target": "outbound_transfer_section",
                        "note": "Enter data transfer out of the region",
                        "fields": [
                            {
                                "field": "data_transfer_to",
                                "placeholder": "Internet"
                            },
                            {
                                "field": "amount",
                                "placeholder": {"amount": "10", "unit": "GB per month"}
                            }
                        ]
                    }
                ]
            }
        ]

class VPCConfigurationTemplate(ServiceConfigurationTemplate):
    """Template configuration cho VPC service"""
    
    def __init__(self):
        super().__init__()
        # Sẽ được bổ sung chi tiết các bước configuration VPC
        self.configuration_steps = [
            {
                "step": "select_region",
                "description": "Chọn AWS Region",
                "action": "click_dropdown",
                "target": "region_dropdown", 
                "placeholder": "US East (N. Virginia)"
            },
            {
                "step": "configure_nat_gateway",
                "description": "Cấu hình NAT Gateway",
                "action": "input_number",
                "target": "nat_gateway_field",
                "placeholder": "1"
            },
            {
                "step": "set_data_processing",
                "description": "Nhập Data Processing",
                "action": "input_with_unit",
                "target": "data_processing_field",
                "placeholder": {"amount": "1", "unit": "GB"}
            }
        ]

class LoadBalancerConfigurationTemplate(ServiceConfigurationTemplate):
    """Template configuration cho Load Balancer service"""
    
    def __init__(self):
        super().__init__()
        # Sẽ được bổ sung chi tiết các bước configuration Load Balancer
        self.configuration_steps = [
            {
                "step": "select_region",
                "description": "Chọn AWS Region",
                "action": "click_dropdown",
                "target": "region_dropdown",
                "placeholder": "US East (N. Virginia)"
            },
            {
                "step": "select_type",
                "description": "Chọn Load Balancer Type",
                "action": "select_option",
                "target": "type_dropdown",
                "placeholder": "Application Load Balancer"
            },
            {
                "step": "set_capacity_units",
                "description": "Nhập Capacity Units",
                "action": "input_number",
                "target": "capacity_units_field",
                "placeholder": "1"
            },
            {
                "step": "set_data_processed",
                "description": "Nhập Data Processed",
                "action": "input_with_unit",
                "target": "data_processed_field",
                "placeholder": {"amount": "1", "unit": "GB"}
            }
        ]

# Factory để get template theo service type
SERVICE_CONFIGURATION_TEMPLATES = {
    "ec2": EC2ConfigurationTemplate(),
    "rds": RDSConfigurationTemplate(), 
    "s3": S3ConfigurationTemplate(),
    "vpc": VPCConfigurationTemplate(),
    "load_balancer": LoadBalancerConfigurationTemplate()
}

def get_service_configuration_template(service_type: str) -> ServiceConfigurationTemplate:
    """Get configuration template cho service type"""
    return SERVICE_CONFIGURATION_TEMPLATES.get(service_type.lower())

def get_configuration_steps(service_type: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get chi tiết configuration steps cho service"""
    template = get_service_configuration_template(service_type)
    if template:
        return template.get_configuration_steps(config)
    return [] 