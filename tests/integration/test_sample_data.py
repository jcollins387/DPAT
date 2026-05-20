"""
Integration tests using real sample data files.

This module contains integration tests that use the actual sample data files
from the sample_data directory to test DPAT functionality with real-world data.
"""

import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sqlite3
import os

# Import the classes we're testing
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dpat import (
    Config, NTDSProcessor, HashProcessor, DataSanitizer, 
    HTMLReportBuilder, DatabaseManager, BloodHoundManager, CrackedPasswordProcessor,
    parse_arguments, main
)
from tests import (
    TestConfig, TestDataGenerator, DatabaseTestHelper, DPATTestCase,
    SAMPLE_NTDS_DATA, SAMPLE_CRACKED_DATA, SAMPLE_GROUP_DATA
)


class TestSampleDataIntegration(DPATTestCase):
    """Integration tests using real sample data files."""
    
    def setUp(self):
        """Set up test environment with sample data paths."""
        super().setUp()
        
        # Get the project root directory (DPAT directory)
        self.project_root = Path(__file__).parent.parent.parent
        self.sample_data_dir = self.project_root / "sample_data"
        
        # Verify sample data files exist
        self.ntds_file = self.sample_data_dir / "customer.ntds"
        self.cracked_file = self.sample_data_dir / "oclHashcat.pot"
        self.domain_admins_file = self.sample_data_dir / "Domain Admins.txt"
        self.enterprise_admins_file = self.sample_data_dir / "Enterprise Admins.txt"
        self.powerview_file = self.sample_data_dir / "Enterprise Admins PowerView Output.txt"
        
        # Verify files exist
        self.assertTrue(self.ntds_file.exists(), f"NTDS file not found: {self.ntds_file}")
        self.assertTrue(self.cracked_file.exists(), f"Cracked file not found: {self.cracked_file}")
        self.assertTrue(self.domain_admins_file.exists(), f"Domain Admins file not found: {self.domain_admins_file}")
        self.assertTrue(self.enterprise_admins_file.exists(), f"Enterprise Admins file not found: {self.enterprise_admins_file}")
        self.assertTrue(self.powerview_file.exists(), f"PowerView file not found: {self.powerview_file}")
    
    def test_sample_data_ntds_processing(self):
        """Test processing the real customer.ntds file."""
        config = Config(
            ntds_file=str(self.ntds_file),
            cracked_file=str(self.cracked_file),
            min_password_length=8,
            report_directory=str(self.temp_dir)
        )
        
        # Process data
        db_manager = DatabaseManager(config)
        ntds_processor = NTDSProcessor(config, db_manager)
        cracked_processor = CrackedPasswordProcessor(config, db_manager)
        
        db_manager.create_schema([])
        ntds_processor.process_ntds_file()
        cracked_processor.process_cracked_file()
        
        # Verify results
        cursor = db_manager.cursor
        
        # Check that accounts were processed
        cursor.execute("SELECT COUNT(*) FROM hash_infos WHERE history_index = -1")
        account_count = cursor.fetchone()[0]
        self.assertGreater(account_count, 0, "Should have processed accounts from customer.ntds")
        
        # Check that some passwords were cracked
        cursor.execute("SELECT COUNT(*) FROM hash_infos WHERE password IS NOT NULL AND history_index = -1")
        cracked_count = cursor.fetchone()[0]
        self.assertGreater(cracked_count, 0, "Should have cracked passwords from oclHashcat.pot")
        
        # Check for specific known cracked passwords
        cursor.execute("SELECT username_full, password FROM hash_infos WHERE password = 'password' AND history_index = -1")
        password_results = cursor.fetchall()
        self.assertGreater(len(password_results), 0, "Should have found 'password' in cracked data")
        
        db_manager.close()
    
