"""
Storage Services Handlers - S3, EBS, EFS, etc.

This module contains handlers for AWS storage services following the
service-oriented architecture pattern.
"""

from typing import Dict, Any, List
from .service_registry import BaseServiceHandler, service_registry
import logging

logger = logging.getLogger(__name__)

class S3ServiceHandler(BaseServiceHandler):
    """Handler for Amazon S3 service"""
    
    def get_service_name(self) -> str:
        return "Amazon S3"
    
    def get_search_terms(self) -> List[str]:
        return ["S3", "Amazon S3", "Simple Storage Service"]
    
    def get_service_category(self) -> str:
        return "storage"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            # Basic configuration
            "region": "US East (Ohio)",
            "location_type": "Region",
            "description": "S3 Storage Cost Estimate",

            # S3 Standard Storage configuration
            "s3_standard_enabled": True,
            "storage_amount": "100",
            "storage_unit": "GB per month",
            "data_movement": "The specified amount of data is already stored in S3 Standard",

            # Request configuration
            "put_copy_post_list_requests": "10000",
            "get_select_requests": "50000",
            "data_returned_s3_select": "10",
            "data_returned_unit": "GB per month",
            "data_scanned_s3_select": "50",
            "data_scanned_unit": "GB per month",

            # Data Transfer configuration
            "data_transfer_enabled": True,
            "inbound_data_amount": "10",
            "inbound_data_unit": "TB per month",
            "outbound_data_amount": "5",
            "outbound_data_unit": "TB per month",

            # Storage Classes (disabled by default)
            "s3_intelligent_tiering": False,
            "s3_standard_infrequent": False,
            "s3_one_zone": False,
            "s3_glacier": False
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []

        # Required fields validation
        if not config.get("region"):
            errors.append("S3: region is required")

        # Storage amount validation
        storage_amount = config.get("storage_amount", "100")
        try:
            amount = float(storage_amount)
            if amount < 0:
                errors.append("S3: storage_amount must be non-negative")
            if amount > 1000000:  # 1 PB limit
                errors.append("S3: storage_amount cannot exceed 1,000,000 GB")
        except (ValueError, TypeError):
            errors.append("S3: storage_amount must be a valid number")

        # Request validation
        put_requests = config.get("put_copy_post_list_requests", "10000")
        try:
            put_val = int(put_requests)
            if put_val < 0:
                errors.append("S3: PUT/COPY/POST/LIST requests must be non-negative")
            if put_val > 100000000:  # 100M requests limit
                errors.append("S3: PUT/COPY/POST/LIST requests cannot exceed 100,000,000")
        except (ValueError, TypeError):
            errors.append("S3: PUT/COPY/POST/LIST requests must be a valid number")

        get_requests = config.get("get_select_requests", "50000")
        try:
            get_val = int(get_requests)
            if get_val < 0:
                errors.append("S3: GET/SELECT requests must be non-negative")
            if get_val > 1000000000:  # 1B requests limit
                errors.append("S3: GET/SELECT requests cannot exceed 1,000,000,000")
        except (ValueError, TypeError):
            errors.append("S3: GET/SELECT requests must be a valid number")

        # Data transfer validation
        inbound_data = config.get("inbound_data_amount", "10")
        try:
            inbound_val = float(inbound_data)
            if inbound_val < 0:
                errors.append("S3: inbound data transfer must be non-negative")
            if inbound_val > 10000:  # 10 PB limit
                errors.append("S3: inbound data transfer cannot exceed 10,000 TB")
        except (ValueError, TypeError):
            errors.append("S3: inbound data transfer must be a valid number")

        outbound_data = config.get("outbound_data_amount", "5")
        try:
            outbound_val = float(outbound_data)
            if outbound_val < 0:
                errors.append("S3: outbound data transfer must be non-negative")
            if outbound_val > 10000:  # 10 PB limit
                errors.append("S3: outbound data transfer cannot exceed 10,000 TB")
        except (ValueError, TypeError):
            errors.append("S3: outbound data transfer must be a valid number")

        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}

        return f"""
        🪣 AMAZON S3 DETAILED CONFIGURATION WORKFLOW

        PHASE 1: KHỞI TẠO VÀ ĐIỀU HƯỚNG S3

        Step 1: Truy Cập Trang Cấu Hình S3
        - Look for "Configure Amazon Simple Storage Service (S3)" button
        - Click the S3 configuration button
        - Wait 3 seconds for S3 configuration page to load
        - Verify you are on S3 configuration page

        Step 2: Điền Mô Tả Estimate
        - Find description input field with placeholder "Enter a description for your estimate"
        - Clear any existing text
        - Enter: "{full_config['description']}"

        PHASE 2: CẤU HÌNH VỊ TRÍ VÀ REGION

        Step 3: Chọn Location Type
        - Find location type dropdown or selection area
        - Select: "{full_config['location_type']}"
        - Wait 1 second for selection to register

        Step 4: Chọn Region
        - Find region dropdown or selection area
        - Select: "{full_config['region']}"
        - Verify region selection is highlighted/confirmed

        PHASE 3: CẤU HÌNH S3 STORAGE CLASSES

        Step 5: Kích Hoạt S3 Standard
        - Find S3 Standard checkbox or toggle switch
        - Enable S3 Standard storage class
        - Verify toggle is in "enabled" state

        Step 6: Kích Hoạt Data Transfer
        - Find Data Transfer checkbox or toggle switch
        - Enable Data Transfer feature
        - Verify toggle is in "enabled" state

        Step 7: Cấu Hình Các Storage Classes Khác (Tùy Chọn)
        - Ensure S3 Intelligent-Tiering is disabled (if present)
        - Ensure S3 Standard-Infrequent Access is disabled (if present)
        - Ensure S3 One Zone-Infrequent Access is disabled (if present)
        - Ensure S3 Glacier options are disabled (if present)

        PHASE 4: CẤU HÌNH S3 STANDARD STORAGE

        Step 8: Mở Rộng S3 Standard Section
        - Look for "S3 Standard" section or button
        - Click to expand S3 Standard configuration section
        - Wait 1 second for section to expand

        Step 9: Nhập Dung Lượng Storage
        - Find storage amount input field for S3 Standard
        - Clear existing value
        - Enter: "{full_config['storage_amount']}"
        - Verify input is accepted

        Step 10: Chọn Đơn Vị Storage
        - Find storage unit dropdown
        - Select: "{full_config['storage_unit']}"
        - Verify unit selection is confirmed

        Step 11: Cấu Hình Data Movement
        - Find data movement dropdown
        - Select: "{full_config['data_movement']}"
        - Wait 0.5 seconds for selection to register

        Step 12: Cấu Hình PUT/COPY/POST/LIST Requests
        - Find PUT/COPY/POST/LIST requests input field
        - Clear existing value
        - Enter: "{full_config['put_copy_post_list_requests']}"

        Step 13: Cấu Hình GET/SELECT Requests
        - Find GET/SELECT requests input field
        - Clear existing value
        - Enter: "{full_config['get_select_requests']}"

        Step 14: Cấu Hình Data Returned by S3 Select
        - Find data returned by S3 Select input field
        - Clear existing value
        - Enter: "{full_config['data_returned_s3_select']}"

        Step 15: Chọn Đơn Vị cho Data Returned
        - Find data returned unit dropdown
        - Select: "{full_config['data_returned_unit']}"

        Step 16: Cấu Hình Data Scanned by S3 Select
        - Find data scanned by S3 Select input field
        - Clear existing value
        - Enter: "{full_config['data_scanned_s3_select']}"

        Step 17: Chọn Đơn Vị cho Data Scanned
        - Find data scanned unit dropdown
        - Select: "{full_config['data_scanned_unit']}"

        PHASE 5: CẤU HÌNH DATA TRANSFER

        Step 18: Mở Rộng Data Transfer Section
        - Look for "Data Transfer" section or button
        - Click to expand Data Transfer configuration section
        - Wait 1 second for section to expand

        Step 19: Cấu Hình Inbound Data Transfer
        - Find inbound data transfer dropdown
        - Select "Data transfer from" option
        - Wait 0.5 seconds for selection

        Step 20: Nhập Lượng Inbound Data
        - Find inbound data amount input field
        - Clear existing value
        - Enter: "{full_config['inbound_data_amount']}"

        Step 21: Chọn Đơn Vị Inbound Data
        - Find inbound data unit dropdown
        - Select: "{full_config['inbound_data_unit']}"

        Step 22: Thêm Inbound Data Transfer
        - Look for "Add inbound data transfer" button
        - Click the button to add inbound data transfer
        - Wait 0.5 seconds for addition to register

        Step 23: Cấu Hình Outbound Data Transfer
        - Find outbound data transfer dropdown
        - Select "Data transfer to" option
        - Wait 0.5 seconds for selection

        Step 24: Nhập Lượng Outbound Data
        - Find outbound data amount input field
        - Clear existing value
        - Enter: "{full_config['outbound_data_amount']}"

        Step 25: Chọn Đơn Vị Outbound Data
        - Find outbound data unit dropdown
        - Select: "{full_config['outbound_data_unit']}"

        Step 26: Thêm Outbound Data Transfer
        - Look for "Add outbound data transfer" button
        - Click the button to add outbound data transfer
        - Wait 0.5 seconds for addition to register

        PHASE 6: KIỂM TRA VÀ HOÀN TẤT

        Step 27: Hiển Thị Calculations (Optional)
        - Look for "Show calculations" button
        - If review is needed, click the button
        - Wait 2 seconds for calculations to display

        Step 28: Thêm Vào Estimate
        - Scroll to bottom of configuration page
        - Look for "Add to my estimate" or "Save and add service" button
        - Click the button to add S3 to estimate
        - Wait 3 seconds for confirmation
        - Verify success message or return to main calculator page

        CRITICAL SUCCESS CRITERIA:
        - S3 service must be added to the estimate successfully
        - All storage and data transfer configurations must be applied
        - No validation errors should be present
        - Must return to main calculator page or show success confirmation

        CONFIGURATION SUMMARY:
        - Region: {full_config['region']}
        - Storage Amount: {full_config['storage_amount']} {full_config['storage_unit']}
        - PUT/COPY/POST/LIST Requests: {full_config['put_copy_post_list_requests']}
        - GET/SELECT Requests: {full_config['get_select_requests']}
        - Inbound Data Transfer: {full_config['inbound_data_amount']} {full_config['inbound_data_unit']}
        - Outbound Data Transfer: {full_config['outbound_data_amount']} {full_config['outbound_data_unit']}
        - S3 Select Data Returned: {full_config['data_returned_s3_select']} {full_config['data_returned_unit']}
        - S3 Select Data Scanned: {full_config['data_scanned_s3_select']} {full_config['data_scanned_unit']}
        """
    
    def get_timeout_seconds(self) -> int:
        return 240  # S3 has very detailed multi-phase configuration with 28 steps

    def get_complexity_score(self) -> int:
        return 9  # Very high complexity due to detailed 6-phase workflow

class EBSServiceHandler(BaseServiceHandler):
    """Handler for Amazon EBS service"""
    
    def get_service_name(self) -> str:
        return "Amazon EBS"
    
    def get_search_terms(self) -> List[str]:
        return ["EBS", "Amazon EBS", "Elastic Block Store"]
    
    def get_service_category(self) -> str:
        return "storage"
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "volume_type": "gp3",
            "storage_amount": "100",
            "storage_unit": "GB",
            "iops": "3000",
            "throughput": "125",
            "region": "US East (N. Virginia)"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        storage = config.get("storage_amount", "100")
        try:
            storage_val = int(storage)
            if storage_val < 1:
                errors.append("EBS: storage_amount must be at least 1 GB")
        except (ValueError, TypeError):
            errors.append("EBS: storage_amount must be a valid number")
        
        return errors
    
    def get_service_instructions(self, config: Dict[str, Any]) -> str:
        full_config = {**self.get_default_config(), **config}
        
        return f"""
        💾 ADD AMAZON EBS SERVICE:

        Step 1: Service Selection
        - Search for "EBS" in the service search box
        - Look for "Amazon EBS" service card (Block Storage)
        - Click "Configure" button on the Amazon EBS service card
        - Verify URL contains "ebs" after page loads

        Step 2: Configuration
        Configure EBS with these settings:
        - Region: {full_config['region']}
        - Volume Type: {full_config['volume_type']}
        - Storage: {full_config['storage_amount']} {full_config['storage_unit']}
        - IOPS: {full_config['iops']}
        - Throughput: {full_config['throughput']} MB/s

        Step 3: Add to Estimate
        - Scroll to bottom and click "Save and add service"
        - Verify return to /addService page
        - Confirm EBS appears in estimate summary
        """
    
    def get_timeout_seconds(self) -> int:
        return 100
    
    def get_complexity_score(self) -> int:
        return 4  # Medium complexity

# Register all storage services
service_registry.register_service("s3", S3ServiceHandler())
service_registry.register_service("ebs", EBSServiceHandler())

logger.info("✅ Storage services registered: S3, EBS")
