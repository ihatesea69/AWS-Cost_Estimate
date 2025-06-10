import streamlit as st
import asyncio
import os
import sys
from typing import Dict, Any
import nest_asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fix Windows asyncio event loop policy
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Enable nested async (cần cho Streamlit)
nest_asyncio.apply()

# Import các modules của chúng ta
from src.workflows.cost_estimation_workflow import CostEstimationWorkflow
from config.predefined_templates import PREDEFINED_TEMPLATES, INFRASTRUCTURE_TEMPLATES
from src.monitoring.logger import get_logger, enhanced_logger

# Page config
st.set_page_config(
    page_title="AWS Cost Estimation Agent",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .service-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'estimation_result' not in st.session_state:
        st.session_state.estimation_result = None
    if 'estimation_history' not in st.session_state:
        st.session_state.estimation_history = []
    if 'workflow' not in st.session_state:
        st.session_state.workflow = None
    if 'performance_metrics' not in st.session_state:
        st.session_state.performance_metrics = None
    if 'show_debug_info' not in st.session_state:
        st.session_state.show_debug_info = False

def setup_workflow(api_key: str):
    """Setup workflow với API key"""
    if st.session_state.workflow is None:
        st.session_state.workflow = CostEstimationWorkflow(api_key)
    return st.session_state.workflow

def display_predefined_templates():
    """Display predefined templates trong sidebar"""
    st.sidebar.markdown("### 📋 Predefined Templates")
    
    # Infrastructure templates
    st.sidebar.markdown("**Infrastructure Templates:**")
    for name, template in INFRASTRUCTURE_TEMPLATES.items():
        with st.sidebar.expander(f"🏗️ {name}"):
            st.write(f"**Mô tả:** {template['description']}")
            st.write("**Services:**")
            for service, config in template['services'].items():
                st.write(f"• {service}: {config.get('instance_type', config.get('engine', 'Standard'))}")
    
    # Individual service templates
    st.sidebar.markdown("**Service Templates:**")
    for service_type, templates in PREDEFINED_TEMPLATES.items():
        with st.sidebar.expander(f"⚙️ {service_type.upper()}"):
            for template_name, config in templates.items():
                st.write(f"**{template_name}:**")
                key_configs = {k: v for k, v in config.items() if k in ['instance_type', 'engine', 'storage_class']}
                for k, v in key_configs.items():
                    st.write(f"  {k}: {v}")

def display_estimation_result(result: Dict[str, Any]):
    """Display estimation result với format đẹp"""
    if result.get('status') == 'success':
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.success("✅ Cost estimation hoàn thành thành công!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Summary
        summary = result.get('summary', {})
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Services", summary.get('total_services', 0))
        with col2:
            st.metric("Successfully Added", summary.get('successful', 0))
        with col3:
            st.metric("Failed", summary.get('failed', 0))
        
        # Services added
        if result.get('services_added'):
            st.markdown("### ✅ Services Added Successfully:")
            for service in result['services_added']:
                st.markdown(f"• **{service.upper()}**")
        
        # Auto-filled information
        if result.get('auto_filled_info'):
            st.markdown("### 📝 Auto-filled Information:")
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            for info in result['auto_filled_info']:
                st.markdown(f"• {info}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Estimate links
        links = result.get('estimate_links', {})
        if links:
            st.markdown("### 🔗 AWS Calculator Links:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if links.get('ondemand'):
                    st.markdown("**On-Demand Pricing:**")
                    st.markdown(f"[🔗 View On-Demand Estimate]({links['ondemand']})")
                    st.code(links['ondemand'], language='text')
            
            with col2:
                if links.get('savings_plan'):
                    st.markdown("**1-Year Savings Plan (No Upfront):**")
                    st.markdown(f"[🔗 View Savings Plan Estimate]({links['savings_plan']})")
                    st.code(links['savings_plan'], language='text')
        
        # Failed services
        if result.get('services_failed'):
            st.markdown("### ❌ Failed Services:")
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            for service in result['services_failed']:
                st.markdown(f"• **{service.upper()}** - Có thể do cấu hình không hợp lệ hoặc lỗi browser")
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        st.markdown('</div>', unsafe_allow_html=True)

def display_example_prompts():
    """Display example prompts"""
    st.markdown("### 💡 Example Prompts:")
    
    examples = [
        "Khách hàng tôi cần một web application với 2 EC2 instances t3.medium, RDS PostgreSQL, và S3 storage 500GB",
        "Estimate chi phí cho enterprise setup: 4 EC2 r5.large instances, Multi-AZ RDS MySQL, Load Balancer, VPC với NAT Gateway",
        "Tôi cần basic infrastructure với EC2 t3.small, RDS MySQL nhỏ, và S3 để backup",
        "Setup cho microservices: 3 EC2 instances, PostgreSQL database, S3 storage, Application Load Balancer"
    ]
    
    for i, example in enumerate(examples, 1):
        if st.button(f"📝 Example {i}", key=f"example_{i}"):
            st.session_state.user_input = example

async def run_estimation_async(workflow, user_input):
    """Run estimation asynchronously"""
    return await workflow.run_estimation(user_input)

def main():
    """Main Streamlit app"""
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">💰 AWS Cost Estimation Agent</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    display_predefined_templates()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🚀 Cost Estimation Request")
        
        # API Key input (try to load from .env first)
        default_api_key = os.getenv('OPENAI_API_KEY', '')
        
        api_key = st.text_input(
            "🔑 OpenAI API Key:",
            type="password",
            value=default_api_key if default_api_key != 'your-openai-api-key-here' else '',
            help="API key được auto-load từ .env file. Bạn có thể override nếu cần."
        )
        
        if not api_key:
            st.warning("⚠️ Vui lòng nhập OpenAI API key hoặc cấu hình trong .env file")
            st.info("💡 Tip: Copy env_example.txt thành .env và thêm API key để tự động load")
            st.stop()
        
        # User input
        user_input = st.text_area(
            "📝 Mô tả yêu cầu AWS infrastructure:",
            height=150,
            placeholder="Ví dụ: Khách hàng tôi cần một web application với EC2 t3.medium, RDS PostgreSQL, S3 storage...",
            value=st.session_state.get('user_input', '')
        )
        
        # Example prompts
        display_example_prompts()
        
        # Estimation button
        if st.button("🚀 Start Cost Estimation", type="primary", help="Nhấn để bắt đầu browser agent và workflow"):
            if not user_input.strip():
                st.error("❌ Vui lòng nhập mô tả yêu cầu!")
                st.stop()
            
            # Setup workflow
            try:
                workflow = setup_workflow(api_key)
                st.success("✅ Workflow initialized successfully!")
            except Exception as e:
                st.error(f"❌ Lỗi khởi tạo workflow: {str(e)}")
                st.stop()
            
            # Show detailed progress with real-time updates
            st.markdown("### 🤖 AI Agent Progress")
            
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                detail_text = st.empty()
                
                # Phase 1: Analysis
                progress_bar.progress(10)
                status_text.markdown("**🔍 Phase 1: Analyzing Requirements**")
                detail_text.text("Parsing user input and extracting service requirements...")
                
                # Phase 2: Browser Setup
                progress_bar.progress(25)
                status_text.markdown("**🌐 Phase 2: Browser Agent Setup**")
                detail_text.text("Initializing browser agent and navigating to AWS Calculator...")
                
                # Phase 3: Workflow Execution
                progress_bar.progress(40)
                status_text.markdown("**⚙️ Phase 3: Workflow Execution**")
                detail_text.text("Running LangGraph workflow with browser automation...")
                
                # Run estimation
                try:
                    progress_bar.progress(60)
                    status_text.markdown("**🔄 Phase 4: Adding Services**")
                    detail_text.text("Browser agent is adding services to AWS Calculator...")
                    
                    # Execute the actual workflow
                    result = asyncio.run(run_estimation_async(workflow, user_input))
                    
                    progress_bar.progress(90)
                    status_text.markdown("**🔗 Phase 5: Generating Links**")
                    detail_text.text("Extracting estimate links from AWS Calculator...")
                    
                    # Store results
                    st.session_state.estimation_result = result

                    # Store performance metrics
                    st.session_state.performance_metrics = enhanced_logger.performance_monitor.get_overall_stats()

                    # Add to history
                    st.session_state.estimation_history.append({
                        'timestamp': datetime.now(),
                        'input': user_input,
                        'result': result,
                        'performance': st.session_state.performance_metrics
                    })
                    
                    progress_bar.progress(100)
                    status_text.markdown("**✅ Phase 6: Complete!**")
                    detail_text.text("Cost estimation completed successfully!")
                    
                    # Show success message
                    if result.get('status') == 'success':
                        st.balloons()
                        st.success("🎉 Cost estimation hoàn thành! Scroll xuống để xem kết quả.")
                    else:
                        st.warning("⚠️ Estimation hoàn thành nhưng có một số vấn đề. Xem kết quả bên dưới.")
                    
                except Exception as e:
                    progress_bar.progress(0)
                    status_text.markdown("**❌ Error Occurred**")
                    detail_text.text("")
                    st.error(f"❌ Lỗi trong quá trình estimation: {str(e)}")
                    
                    # Show debug info
                    with st.expander("🔧 Debug Information"):
                        st.code(str(e), language='text')
                    return
    
    with col2:
        st.markdown("### 📊 Status & Info")
        
        # Current status
        if st.session_state.estimation_result:
            status = st.session_state.estimation_result.get('status', 'unknown')
            if status == 'success':
                st.success("✅ Ready")
            else:
                st.error("❌ Error")
        else:
            st.info("⏳ Waiting")
        
        # History count
        st.metric("Estimation History", len(st.session_state.estimation_history))
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Reset"):
            st.session_state.estimation_result = None
            st.session_state.performance_metrics = None
            st.experimental_rerun()

        if st.button("📋 Clear History"):
            st.session_state.estimation_history = []
            enhanced_logger.performance_monitor.metrics.clear()
            enhanced_logger.workflow_monitor.events.clear()
            st.experimental_rerun()

        # Debug toggle
        st.session_state.show_debug_info = st.checkbox("🔧 Show Debug Info", value=st.session_state.show_debug_info)

        # Performance metrics
        if st.session_state.performance_metrics:
            st.markdown("### 📊 Performance")
            metrics = st.session_state.performance_metrics

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Success Rate", f"{metrics.get('success_rate', 0):.1%}")
            with col2:
                st.metric("Avg Duration", f"{metrics.get('avg_duration', 0):.1f}s")
    
    # Display results
    if st.session_state.estimation_result:
        st.markdown("---")
        st.markdown("## 📊 Estimation Results")
        display_estimation_result(st.session_state.estimation_result)

        # Debug information
        if st.session_state.show_debug_info:
            st.markdown("---")
            st.markdown("## 🔧 Debug Information")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Performance Metrics")
                if st.session_state.performance_metrics:
                    st.json(st.session_state.performance_metrics)
                else:
                    st.info("No performance metrics available")

            with col2:
                st.markdown("### Workflow Events")
                workflow_summary = enhanced_logger.workflow_monitor.get_workflow_summary()
                st.json(workflow_summary)

            # Export metrics button
            if st.button("📥 Export Metrics"):
                try:
                    import tempfile

                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        enhanced_logger.export_metrics(f.name)

                    st.success(f"✅ Metrics exported to {f.name}")

                    # Provide download link
                    with open(f.name, 'r') as f:
                        metrics_data = f.read()

                    st.download_button(
                        label="📥 Download Metrics",
                        data=metrics_data,
                        file_name=f"aws_estimation_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )

                except Exception as e:
                    st.error(f"❌ Failed to export metrics: {str(e)}")
    
    # Display history
    if st.session_state.estimation_history:
        st.markdown("---")
        st.markdown("## 📈 Estimation History")
        
        for i, entry in enumerate(reversed(st.session_state.estimation_history[-5:]), 1):
            with st.expander(f"📝 Request {len(st.session_state.estimation_history) - i + 1} - {entry['timestamp'].strftime('%H:%M:%S')}"):
                st.write(f"**Input:** {entry['input'][:100]}...")
                st.write(f"**Status:** {entry['result'].get('status', 'unknown')}")
                if entry['result'].get('services_added'):
                    st.write(f"**Services Added:** {', '.join(entry['result']['services_added'])}")

if __name__ == "__main__":
    main() 