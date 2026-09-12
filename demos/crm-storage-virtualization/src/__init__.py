"""
CRM Storage Virtualization Package.
"""

from .models import (
    StorageBackendType,
    StoredObjectMetadata,
    MigrationProgress
)
from .storage_manager import (
    InMemoryStorageDriver,
    VirtualStorageManager
)

__all__ = [
    "StorageBackendType",
    "StoredObjectMetadata",
    "MigrationProgress",
    "InMemoryStorageDriver",
    "VirtualStorageManager"
]
