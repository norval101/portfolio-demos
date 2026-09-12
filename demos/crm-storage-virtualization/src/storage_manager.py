"""
Virtual Storage Manager and S3 Migration Engine with dual-read fallback.
"""

import hashlib
from typing import Dict, Optional, Tuple, List
from .models import (
    StorageBackendType,
    StoredObjectMetadata,
    MigrationProgress
)


class InMemoryStorageDriver:
    """Simulates an underlying storage target (Local Disk or AWS S3 Bucket)."""
    def __init__(self, backend_type: StorageBackendType):
        self.backend_type = backend_type
        self._store: Dict[str, bytes] = {}
        self._meta: Dict[str, StoredObjectMetadata] = {}

    def put(self, path: str, content: bytes, content_type: str = "application/octet-stream") -> StoredObjectMetadata:
        hasher = hashlib.sha256()
        hasher.update(content)
        checksum = hasher.hexdigest()

        self._store[path] = content
        metadata = StoredObjectMetadata(
            path=path,
            backend=self.backend_type,
            byte_size=len(content),
            sha256_checksum=checksum,
            content_type=content_type
        )
        self._meta[path] = metadata
        return metadata

    def get(self, path: str) -> Optional[bytes]:
        return self._store.get(path)

    def get_metadata(self, path: str) -> Optional[StoredObjectMetadata]:
        return self._meta.get(path)

    def exists(self, path: str) -> bool:
        return path in self._store

    def delete(self, path: str) -> bool:
        if path in self._store:
            del self._store[path]
            del self._meta[path]
            return True
        return False

    def list_paths(self) -> List[str]:
        return list(self._store.keys())


class VirtualStorageManager:
    def __init__(self):
        self.local_driver = InMemoryStorageDriver(StorageBackendType.LOCAL)
        self.s3_driver = InMemoryStorageDriver(StorageBackendType.S3_CLOUD)
        self._primary_backend = StorageBackendType.S3_CLOUD

    def write_file(self, path: str, content: bytes, content_type: str = "application/octet-stream") -> StoredObjectMetadata:
        """New uploads write directly to Cloud S3 primary storage."""
        return self.s3_driver.put(path, content, content_type)

    def read_file(self, path: str) -> Tuple[Optional[bytes], Optional[StoredObjectMetadata]]:
        """
        Dual-read fallback pattern:
        1. Look in Cloud S3 first.
        2. If not found, check Local Storage (legacy unmigrated asset).
        """
        if self.s3_driver.exists(path):
            return self.s3_driver.get(path), self.s3_driver.get_metadata(path)

        if self.local_driver.exists(path):
            return self.local_driver.get(path), self.local_driver.get_metadata(path)

        return None, None

    def execute_migration_to_s3(self) -> MigrationProgress:
        """
        Batch-migrates all legacy local files to Cloud S3,
        verifying SHA-256 checksum integrity during transfer.
        """
        paths = self.local_driver.list_paths()
        migrated = 0
        failed = 0
        transferred_bytes = 0

        for path in paths:
            content = self.local_driver.get(path)
            meta = self.local_driver.get_metadata(path)

            if content is None or meta is None:
                failed += 1
                continue

            # Upload to S3
            s3_meta = self.s3_driver.put(path, content, meta.content_type)

            # Verify integrity
            if s3_meta.sha256_checksum == meta.sha256_checksum:
                migrated += 1
                transferred_bytes += len(content)
                # Safely delete from local storage after successful verified transfer
                self.local_driver.delete(path)
            else:
                failed += 1

        return MigrationProgress(
            total_files=len(paths),
            migrated_files=migrated,
            failed_files=failed,
            bytes_transferred=transferred_bytes,
            is_complete=(failed == 0)
        )
