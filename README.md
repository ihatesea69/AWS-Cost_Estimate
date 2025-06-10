# 💰 AWS Cost Estimation Agent

Một AI Agent sử dụng Browser-use, LangChain, LangGraph và OpenAI để tự động tính toán chi phí AWS thông qua AWS Pricing Calculator.

## 🚀 Tính Năng

- **Tự Động Browser Control**: Sử dụng Browser-use để điều khiển AWS Calculator
- **AI-Powered Parsing**: LangChain + OpenAI để phân tích yêu cầu người dùng
- **Workflow Management**: LangGraph để quản lý quy trình estimation
- **Template System**: Predefined templates cho các AWS services phổ biến
- **Streamlit Interface**: Giao diện web đẹp và dễ sử dụng
- **Auto-fill**: Tự động điền các thông tin thiếu từ templates

## 🏗️ Kiến Trúc

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   AI Agent       │───▶│  AWS Calculator │
│  (Streamlit)    │    │  (LangGraph)     │    │   (Browser)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                               │                        │
                               ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Template       │    │  Cost Links     │
                       │   Parser         │    │   (Output)      │
                       └──────────────────┘    └─────────────────┘
```

## 📦 Cài Đặt

### 1. Clone Repository

```bash
git clone <repository-url>
cd aws-cost-estimation-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment

```bash
# Copy environment file
cp env_example.txt .env

# Edit .env và thêm OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Cấu trúc thư mục

```
aws-cost-estimation-agent/
├── src/
│   ├── agents/
│   │   └── browser_agent.py          # Browser automation agent
│   ├── utils/
│   │   └── template_parser.py        # AI template parser
│   └── workflows/
│       └── cost_estimation_workflow.py  # LangGraph workflow
├── config/
│   └── predefined_templates.py       # AWS service templates
├── streamlit_app.py                  # Web interface
├── main.py                          # CLI interface
├── requirements.txt                 # Dependencies
└── # AWS Cost Estimation Agent

An intelligent AWS cost estimation system that automates browser interactions with AWS Pricing Calculator using AI agents and LangGraph workflows.

## 🚀 Features

### Core Functionality
- **Natural Language Processing**: Converts user requirements to AWS service configurations
- **Browser Automation**: Controls browser to interact with AWS Calculator using browser-use
- **Template System**: Uses predefined templates for common AWS services
- **Auto-fill**: Automatically fills missing information from templates
- **Workflow Management**: Orchestrates the multi-step estimation process using LangGraph
- **Web Interface**: Provides user-friendly Streamlit interface

### Enhanced Features (Latest Updates)
- **Unified Browser Agent**: Consolidated and enhanced browser automation with persistent sessions
- **Robust Error Handling**: Advanced error recovery and retry mechanisms
- **Visual Verification**: Screenshot-based verification of successful actions
- **Performance Monitoring**: Comprehensive logging and performance tracking
- **Service-Specific Modules**: Specialized handling for each AWS service type
- **Real-time Progress Updates**: Live feedback during estimation process

## 🏗️ Architecture

### Main Components

1. **User Interface** (`streamlit_app.py`)
   - Streamlit-based web interface for user input and result display
   - Real-time progress tracking
   - Performance metrics dashboard
   - Debug information panel

2. **Workflow Engine** (`src/workflows/cost_estimation_workflow.py`)
   - LangGraph-based workflow orchestration
   - Enhanced monitoring and logging
   - Robust error handling

3. **Unified Browser Agent** (`src/agents/browser_agent.py`)
   - Persistent browser session management
   - Visual verification of actions
   - Service-specific interaction patterns
   - Advanced error recovery

4. **Template Parser** (`src/utils/template_parser.py`)
   - AI-powered parsing of user requirements
   - Integration with predefined templates

5. **Configuration** (`config/predefined_templates.py`)
   - Predefined templates for AWS services
   - Infrastructure templates for common setups

### New Utility Modules

6. **Browser Helpers** (`src/utils/browser_helpers.py`)
   - Common browser interaction patterns
   - Standardized service configuration workflows
   - Error recovery patterns

7. **Verification System** (`src/utils/verification.py`)
   - Visual verification utilities
   - Action verification and validation
   - Estimate verification

8. **Monitoring & Logging** (`src/monitoring/logger.py`)
   - Enhanced logging with performance tracking
   - Workflow event monitoring
   - Metrics export functionality

9. **Service Modules** (`src/services/`)
   - Service-specific configuration handlers
   - Validation and cost estimation utilities
   - Browser automation patterns for each service

## 🔄 Data Flow

1. User inputs requirements via Streamlit interface
2. Template parser extracts structured service configurations
3. Workflow engine orchestrates the estimation process with monitoring
4. Unified browser agent navigates AWS Calculator with persistent sessions
5. Services are added with visual verification and error recovery
6. Results (links to estimates) are returned with performance metrics

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- Chrome/Chromium browser

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd aws-cost-estimation-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp env_example.txt .env
# Edit .env and add your OpenAI API key
```

4. Run the application:
```bash
streamlit run streamlit_app.py
```

## 📋 Usage

### Basic Usage

1. **Start the Application**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Enter Requirements**
   - Describe your AWS infrastructure needs in natural language
   - Example: "I need 2 EC2 t3.medium instances, PostgreSQL RDS, and 500GB S3 storage"

3. **Monitor Progress**
   - Watch real-time progress updates
   - View performance metrics
   - Check debug information if needed

4. **Review Results**
   - Get shareable AWS Calculator links
   - View auto-filled configurations
   - See performance statistics

### Advanced Features

#### Performance Monitoring
- Enable "Show Debug Info" to see detailed performance metrics
- Export metrics for analysis
- Monitor success rates and operation durations

#### Template System
- Use predefined templates for common configurations
- Infrastructure templates for complete setups
- Automatic template selection based on requirements

#### Error Recovery
- Automatic retry mechanisms for failed operations
- Session health monitoring and recovery
- Visual verification of all actions

## 🔧 Configuration

### Service Templates

Edit `config/predefined_templates.py` to customize:
- Default service configurations
- Infrastructure templates
- Regional settings
- Pricing preferences

### Browser Settings

Configure browser behavior in the agent initialization:
- Headless vs visible mode
- Browser type (Chromium/Chrome)
- Timeout settings
- Retry parameters

### Monitoring

Customize monitoring in `src/monitoring/logger.py`:
- Log levels and formats
- Performance metric collection
- Export formats
- Retention policies

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Manual Testing
1. Test individual services with simple configurations
2. Test complex multi-service setups
3. Test error scenarios (network issues, invalid configs)
4. Verify performance metrics collection

## 🔍 Troubleshooting

### Common Issues

1. **Browser Session Failures**
   - Check Chrome/Chromium installation
   - Verify network connectivity
   - Enable debug mode for detailed logs

2. **Service Addition Failures**
   - Verify AWS Calculator page structure hasn't changed
   - Check service configuration validity
   - Review browser automation logs

3. **Performance Issues**
   - Monitor session health
   - Check for memory leaks
   - Optimize retry parameters

### Debug Mode
Enable debug information in the Streamlit interface to:
- View detailed performance metrics
- Monitor workflow events
- Export diagnostic data
- Track browser automation steps

## 📊 Performance Metrics

The system tracks:
- **Operation Duration**: Time taken for each operation
- **Success Rates**: Percentage of successful operations
- **Error Patterns**: Common failure points
- **Resource Usage**: Browser session health
- **Workflow Progress**: Step-by-step execution tracking

## 🔮 Future Enhancements

### Planned Features
- Support for additional AWS services
- Cost optimization recommendations
- Historical cost tracking
- Multi-region pricing comparison
- API integration for direct AWS pricing

### Architecture Improvements
- Microservices architecture
- Distributed browser automation
- Real-time collaboration features
- Advanced caching mechanisms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Update documentation
5. Submit a pull request

### Development Guidelines
- Follow Python PEP 8 style guide
- Add comprehensive logging
- Include performance monitoring
- Write unit and integration tests
- Update documentation

## 📄 License

[Add your license information here]

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review debug logs and performance metrics
- Contact the development team

---

**Note**: This system automates browser interactions with AWS Pricing Calculator. AWS may update their interface, which could require adjustments to the automation patterns.                       # Documentation
```

## 🎯 Sử Dụng

### Chạy Streamlit Web Interface

```bash
streamlit run streamlit_app.py
```

**Lưu ý:** Nếu lệnh `streamlit` không được nhận diện, hãy sử dụng:

```bash
python -m streamlit run streamlit_app.py
```

## 📝 Ví Dụ Sử Dụng

### Basic Web Application
```
Khách hàng tôi cần một web application với 2 EC2 instances t3.medium, RDS PostgreSQL, và S3 storage 500GB
```

### Enterprise Setup
```
Estimate chi phí cho enterprise setup: 4 EC2 r5.large instances, Multi-AZ RDS MySQL, Load Balancer, VPC với NAT Gateway
```

### Microservices Architecture
```
Setup cho microservices: 3 EC2 instances, PostgreSQL database, S3 storage, Application Load Balancer
```

## 🛠️ Predefined Templates

### Infrastructure Templates
- **basic_web_app**: Web application cơ bản với EC2, RDS, S3
- **enterprise_app**: Enterprise setup với high availability

### Service Templates
- **EC2**: default, web_server, database_server
- **RDS**: default, postgresql, production
- **S3**: default, backup
- **VPC**: default with NAT Gateway
- **Load Balancer**: Application Load Balancer

## 🔄 Workflow Process

1. **Parse Input**: AI phân tích yêu cầu người dùng
2. **Validate Config**: Kiểm tra cấu hình hợp lệ
3. **Navigate Calculator**: Điều hướng tới AWS Calculator
4. **Prepare Services**: Sắp xếp thứ tự add services
5. **Add Services**: Thêm từng service một cách tuần tự
   - VPC → EC2 → RDS → S3 → Load Balancer
6. **Generate Links**: Tạo links cho On-Demand và Savings Plans
7. **Format Result**: Format kết quả final

## 🎨 Streamlit Features

- **Modern UI**: Giao diện đẹp với CSS custom
- **Real-time Progress**: Progress bar và status updates
- **Template Browser**: Xem predefined templates
- **Example Prompts**: Quick-start examples
- **History Tracking**: Lưu lịch sử estimation
- **Auto-fill Notifications**: Hiển thị thông tin được auto-fill

## 🔧 Customization

### Thêm Service Templates

Edit `config/predefined_templates.py`:

```python
PREDEFINED_TEMPLATES["new_service"] = {
    "default": {
        "param1": "value1",
        "param2": "value2"
    }
}
```

### Thêm Browser Actions

Edit `src/agents/browser_agent.py` và thêm method mới:

```python
async def add_new_service(self, config: Dict[str, Any]) -> bool:
    # Implementation here
    pass
```

### Thêm Workflow Nodes

Edit `src/workflows/cost_estimation_workflow.py`:

```python
workflow.add_node("new_node", self.new_node_handler)
```

## 🐛 Troubleshooting

### Common Issues

1. **Browser Agent Fails**
   - Kiểm tra internet connection
   - AWS Calculator có thể có cập nhật UI
   - Thử restart application

2. **OpenAI API Errors**
   - Kiểm tra API key validity
   - Kiểm tra rate limits
   - Kiểm tra billing account

3. **Template Parsing Errors**
   - Cải thiện prompt clarity
   - Thêm specific details
   - Sử dụng example prompts

### Debug Mode

Set DEBUG=True trong .env file để enable verbose logging.

## 📊 Output Format

Kết quả estimation bao gồm:

```json
{
    "status": "success",
    "services_requested": ["ec2", "rds", "s3"],
    "services_added": ["ec2", "rds"],
    "services_failed": ["s3"],
    "auto_filled_info": [
        "EC2: storage_type = gp3 (from default template)",
        "RDS: instance_class = db.t3.small (from postgresql template)"
    ],
    "estimate_links": {
        "ondemand": "https://calculator.aws/#/...",
        "savings_plan": "https://calculator.aws/#/..."
    },
    "summary": {
        "total_services": 3,
        "successful": 2,
        "failed": 1
    }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Browser-use**: Browser automation
- **LangChain**: AI integration
- **LangGraph**: Workflow management
- **Streamlit**: Web interface
- **OpenAI**: Language model

---

**Note**: Đây là demo application. Trong production environment, cần thêm error handling, security measures, và performance optimization. 