"""
Enhanced Logging and Monitoring for AWS Cost Estimation Agent

This module provides comprehensive logging, monitoring, and performance tracking
for the browser automation and workflow execution.
"""

import logging
import time
import json
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    operation: str
    start_time: float
    end_time: float
    duration: float
    success: bool
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class WorkflowEvent:
    """Workflow event data structure"""
    event_type: str
    timestamp: float
    service_type: Optional[str] = None
    status: str = "unknown"
    details: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class PerformanceMonitor:
    """Monitors performance metrics for browser automation"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.active_operations: Dict[str, float] = {}
    
    def start_operation(self, operation: str) -> str:
        """Start timing an operation"""
        operation_id = f"{operation}_{int(time.time() * 1000)}"
        self.active_operations[operation_id] = time.time()
        return operation_id
    
    def end_operation(self, operation_id: str, success: bool = True, 
                     error_message: Optional[str] = None, 
                     metadata: Optional[Dict[str, Any]] = None):
        """End timing an operation"""
        if operation_id not in self.active_operations:
            logging.warning(f"Operation {operation_id} not found in active operations")
            return
        
        start_time = self.active_operations.pop(operation_id)
        end_time = time.time()
        duration = end_time - start_time
        
        # Extract operation name from operation_id
        operation = operation_id.rsplit('_', 1)[0]
        
        metric = PerformanceMetric(
            operation=operation,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            success=success,
            error_message=error_message,
            metadata=metadata
        )
        
        self.metrics.append(metric)
        
        # Log the metric
        status = "✅" if success else "❌"
        logging.info(f"{status} {operation} completed in {duration:.2f}s")
        
        if not success and error_message:
            logging.error(f"❌ {operation} failed: {error_message}")
    
    def get_operation_stats(self, operation: str) -> Dict[str, Any]:
        """Get statistics for a specific operation"""
        operation_metrics = [m for m in self.metrics if m.operation == operation]
        
        if not operation_metrics:
            return {"operation": operation, "count": 0}
        
        durations = [m.duration for m in operation_metrics]
        successes = [m for m in operation_metrics if m.success]
        
        return {
            "operation": operation,
            "count": len(operation_metrics),
            "success_count": len(successes),
            "success_rate": len(successes) / len(operation_metrics),
            "avg_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "total_duration": sum(durations)
        }
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall performance statistics"""
        if not self.metrics:
            return {"total_operations": 0}
        
        total_operations = len(self.metrics)
        successful_operations = len([m for m in self.metrics if m.success])
        total_duration = sum(m.duration for m in self.metrics)
        
        # Get unique operations
        unique_operations = list(set(m.operation for m in self.metrics))
        operation_stats = {op: self.get_operation_stats(op) for op in unique_operations}
        
        return {
            "total_operations": total_operations,
            "successful_operations": successful_operations,
            "success_rate": successful_operations / total_operations,
            "total_duration": total_duration,
            "avg_duration": total_duration / total_operations,
            "unique_operations": len(unique_operations),
            "operation_breakdown": operation_stats
        }

class WorkflowMonitor:
    """Monitors workflow execution and events"""
    
    def __init__(self):
        self.events: List[WorkflowEvent] = []
        self.current_workflow: Optional[str] = None
        self.workflow_start_time: Optional[float] = None
    
    def start_workflow(self, workflow_name: str):
        """Start monitoring a workflow"""
        self.current_workflow = workflow_name
        self.workflow_start_time = time.time()
        
        event = WorkflowEvent(
            event_type="workflow_start",
            timestamp=time.time(),
            status="started",
            details={"workflow_name": workflow_name}
        )
        self.events.append(event)
        logging.info(f"🚀 Workflow started: {workflow_name}")
    
    def end_workflow(self, success: bool = True, error_message: Optional[str] = None):
        """End workflow monitoring"""
        if not self.current_workflow:
            logging.warning("No active workflow to end")
            return
        
        duration = time.time() - self.workflow_start_time if self.workflow_start_time else 0
        
        event = WorkflowEvent(
            event_type="workflow_end",
            timestamp=time.time(),
            status="completed" if success else "failed",
            details={
                "workflow_name": self.current_workflow,
                "duration": duration,
                "error_message": error_message
            }
        )
        self.events.append(event)
        
        status = "✅" if success else "❌"
        logging.info(f"{status} Workflow completed: {self.current_workflow} ({duration:.2f}s)")
        
        self.current_workflow = None
        self.workflow_start_time = None
    
    def log_service_event(self, service_type: str, event_type: str, status: str, 
                         details: Optional[Dict[str, Any]] = None):
        """Log a service-related event"""
        event = WorkflowEvent(
            event_type=event_type,
            timestamp=time.time(),
            service_type=service_type,
            status=status,
            details=details
        )
        self.events.append(event)
        
        status_emoji = {"started": "🔄", "completed": "✅", "failed": "❌"}.get(status, "ℹ️")
        logging.info(f"{status_emoji} {service_type} {event_type}: {status}")
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get summary of workflow execution"""
        if not self.events:
            return {"total_events": 0}
        
        workflow_events = [e for e in self.events if e.event_type in ["workflow_start", "workflow_end"]]
        service_events = [e for e in self.events if e.service_type is not None]
        
        # Count service events by type and status
        service_stats = {}
        for event in service_events:
            service = event.service_type
            if service not in service_stats:
                service_stats[service] = {"started": 0, "completed": 0, "failed": 0}
            
            if event.status in service_stats[service]:
                service_stats[service][event.status] += 1
        
        return {
            "total_events": len(self.events),
            "workflow_events": len(workflow_events),
            "service_events": len(service_events),
            "service_breakdown": service_stats,
            "current_workflow": self.current_workflow
        }

class EnhancedLogger:
    """Enhanced logger with structured logging and monitoring integration"""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.performance_monitor = PerformanceMonitor()
        self.workflow_monitor = WorkflowMonitor()
        
        # Configure logger
        if not self.logger.handlers:
            self._setup_logger(log_file)
    
    def _setup_logger(self, log_file: Optional[str] = None):
        """Setup logger with appropriate handlers and formatters"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        self.logger.setLevel(logging.INFO)
    
    def log_with_performance(self, level: int, message: str, operation: Optional[str] = None,
                           duration: Optional[float] = None, success: bool = True,
                           metadata: Optional[Dict[str, Any]] = None):
        """Log message with optional performance data"""
        self.logger.log(level, message)
        
        if operation and duration is not None:
            # Create a synthetic performance metric
            metric = PerformanceMetric(
                operation=operation,
                start_time=time.time() - duration,
                end_time=time.time(),
                duration=duration,
                success=success,
                metadata=metadata
            )
            self.performance_monitor.metrics.append(metric)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.log_with_performance(logging.INFO, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.log_with_performance(logging.ERROR, message, success=False, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.log_with_performance(logging.WARNING, message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.log_with_performance(logging.DEBUG, message, **kwargs)
    
    def export_metrics(self, file_path: str):
        """Export performance metrics to JSON file"""
        try:
            metrics_data = {
                "performance_metrics": [m.to_dict() for m in self.performance_monitor.metrics],
                "workflow_events": [e.to_dict() for e in self.workflow_monitor.events],
                "performance_summary": self.performance_monitor.get_overall_stats(),
                "workflow_summary": self.workflow_monitor.get_workflow_summary(),
                "export_timestamp": time.time()
            }
            
            with open(file_path, 'w') as f:
                json.dump(metrics_data, f, indent=2)
            
            self.info(f"Metrics exported to {file_path}")
            
        except Exception as e:
            self.error(f"Failed to export metrics: {str(e)}")

# Global logger instance
enhanced_logger = EnhancedLogger("aws_cost_estimation_agent")

# Convenience functions
def get_logger() -> EnhancedLogger:
    """Get the global enhanced logger instance"""
    return enhanced_logger

def start_performance_monitoring(operation: str) -> str:
    """Start monitoring performance for an operation"""
    return enhanced_logger.performance_monitor.start_operation(operation)

def end_performance_monitoring(operation_id: str, success: bool = True, 
                             error_message: Optional[str] = None,
                             metadata: Optional[Dict[str, Any]] = None):
    """End performance monitoring for an operation"""
    enhanced_logger.performance_monitor.end_operation(
        operation_id, success, error_message, metadata
    )

def start_workflow_monitoring(workflow_name: str):
    """Start monitoring a workflow"""
    enhanced_logger.workflow_monitor.start_workflow(workflow_name)

def end_workflow_monitoring(success: bool = True, error_message: Optional[str] = None):
    """End workflow monitoring"""
    enhanced_logger.workflow_monitor.end_workflow(success, error_message)

def log_service_event(service_type: str, event_type: str, status: str, 
                     details: Optional[Dict[str, Any]] = None):
    """Log a service-related event"""
    enhanced_logger.workflow_monitor.log_service_event(
        service_type, event_type, status, details
    )
