"""
Unit tests for CRM Virtual Storage Manager and S3 Migration Engine.
"""

import unittest
from src.models import StorageBackendType
from src.storage_manager import VirtualStorageManager


class TestVirtualStorageManager(unittest.TestCase):
    def setUp(self):
        self.manager = VirtualStorageManager()

    def test_direct_cloud_write_and_read(self):
        content = b"%PDF-1.4 sample invoice data"
        meta = self.manager.write_file("invoices/INV-2026-001.pdf", content, "application/pdf")
        self.assertEqual(meta.backend, StorageBackendType.S3_CLOUD)
        self.assertEqual(meta.byte_size, len(content))

        read_bytes, read_meta = self.manager.read_file("invoices/INV-2026-001.pdf")
        self.assertEqual(read_bytes, content)
        self.assertEqual(read_meta.sha256_checksum, meta.sha256_checksum)

    def test_fallback_reads_legacy_local_file(self):
        # Simulate legacy file existing only on local disk
        legacy_content = b"old client contract v1"
        self.manager.local_driver.put("contracts/C-99.txt", legacy_content, "text/plain")

        # Virtual manager transparently resolves it from local without 404
        read_bytes, read_meta = self.manager.read_file("contracts/C-99.txt")
        self.assertIsNotNone(read_bytes)
        self.assertEqual(read_bytes, legacy_content)
        self.assertEqual(read_meta.backend, StorageBackendType.LOCAL)

    def test_batch_migration_to_s3_with_integrity_verification(self):
        # Seed 3 legacy files on local disk
        f1 = b"photo-1"
        f2 = b"photo-2"
        f3 = b"photo-3"
        self.manager.local_driver.put("uploads/p1.jpg", f1, "image/jpeg")
        self.manager.local_driver.put("uploads/p2.jpg", f2, "image/jpeg")
        self.manager.local_driver.put("uploads/p3.jpg", f3, "image/jpeg")

        # Execute migration
        progress = self.manager.execute_migration_to_s3()
        self.assertTrue(progress.is_complete)
        self.assertEqual(progress.total_files, 3)
        self.assertEqual(progress.migrated_files, 3)
        self.assertEqual(progress.failed_files, 0)
        self.assertEqual(progress.bytes_transferred, len(f1) + len(f2) + len(f3))

        # Local storage is now emptied
        self.assertEqual(len(self.manager.local_driver.list_paths()), 0)

        # S3 has all 3 files
        self.assertTrue(self.manager.s3_driver.exists("uploads/p1.jpg"))
        self.assertTrue(self.manager.s3_driver.exists("uploads/p2.jpg"))
        self.assertTrue(self.manager.s3_driver.exists("uploads/p3.jpg"))


if __name__ == "__main__":
    unittest.main()
