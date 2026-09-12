"""
Domain models for Storage Virtualization and Migration.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime, timezone


class StorageBackendType(str, Enum):
    LOCAL = "LOCAL"
    S3_CLOUD = "S3_CLOUD"


@dataclass(frozen=True)
class StoredObjectMetadata:
    path: str
    backend: StorageBackendType
    byte_size: int
    sha256_checksum: str
    content_type: str
    uploaded_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass(frozen=True)
class MigrationProgress:
    total_files: int
    migrated_files: int
    failed_files: int
    bytes_transferred: int
    is_complete: bool
