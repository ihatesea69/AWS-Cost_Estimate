"""
AWS Services Module - Service-Oriented Architecture

This module contains all AWS service handlers and the service registry.
Import this module to automatically register all available services.
"""

from .service_registry import service_registry, BaseServiceHandler
from . import compute_services
from . import ai_ml_services
from . import database_services
from . import storage_services
from . import networking_services

__all__ = [
    'service_registry',
    'BaseServiceHandler',
    'compute_services',
    'ai_ml_services',
    'database_services',
    'storage_services',
    'networking_services'
]
