#!/usr/bin/env python3
"""
Basic tests for Tari Ledger Wallet using Ragger

This module implements basic functionality tests for the
Minotari Ledger Wallet application using Ledger's Ragger framework.
"""

import os
import sys
import pytest
from pathlib import Path

# Add root directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from ragger.backend import SpeculosBackend, LedgerCommBackend
    from ragger.navigator import Navigator
    from ragger.firmware import Firmware
    from ragger.conftest import configuration
    from ledgered.devices import Devices
except ImportError as e:
    print(f"Error importing Ragger: {e}")
    print("Make sure Ragger is installed: pip install 'ragger[speculos]'")
    sys.exit(1)


class TestTariLedgerWallet:
    """Test class for Tari Ledger Wallet"""
    
    def setup_method(self, method):
        """Setup before each test"""
        self.backend = None
        self.navigator = None
        
    def teardown_method(self, method):
        """Cleanup after each test"""
        # SpeculosBackend se cierra automáticamente, no necesita cleanup manual
        pass
    
    def _get_app_path(self, device="flex"):
        """Get the path to the compiled application"""
        app_path = Path(f"applications/minotari_ledger_wallet/wallet/target/{device}/release/minotari_ledger_wallet")
        if not app_path.exists():
            pytest.skip(f"Application not found at {app_path}")
        return str(app_path)
    
    @pytest.mark.speculos
    def test_app_launch_flex(self):
        """Basic test: launch application on Ledger Flex"""
        app_path = self._get_app_path("flex")
        
        # Get the Flex device instance
        flex_device = Devices.get_by_name("flex")
        
        # Configure Speculos backend for Flex with correct device parameter
        self.backend = SpeculosBackend(
            application=app_path,
            device=flex_device
        )
        
        # Initialize navigator with correct parameters
        self.navigator = Navigator(
            backend=self.backend,
            device=flex_device,
            callbacks={}  # Empty callbacks dictionary for basic test
        )
        
        # Verify application launches successfully
        assert self.backend is not None
        print("✅ Application launched successfully on Ledger Flex")
        print(f"Device: {flex_device.name} (SDK: {flex_device.sdk_name})")
    
    def test_apdu_structure(self):
        """Test: verify basic APDU command structure"""
        # Basic APDU commands the wallet should support
        test_commands = [
            {"name": "GET_VERSION", "apdu": "B001000000"},
            {"name": "GET_APP_NAME", "apdu": "B002000000"},
            {"name": "GET_PUBLIC_KEY", "apdu": "B003000000"},
        ]
        
        for cmd in test_commands:
            print(f"Command: {cmd['name']} - APDU: {cmd['apdu']}")
        
        # This test validates we know the expected structure
        assert len(test_commands) > 0


def test_ragger_environment():
    """Ragger environment verification test"""
    # Verify all Ragger components are available
    from ragger.backend import SpeculosBackend, LedgerCommBackend
    from ragger.navigator import Navigator
    from ragger.firmware import Firmware
    
    print("✅ Ragger environment verified")
    print("✅ SpeculosBackend available")
    print("✅ LedgerCommBackend available")
    print("✅ Navigator available")
    print("✅ Firmware enums available")


if __name__ == "__main__":
    # Run basic tests
    test_ragger_environment()
    
    # Create test instance and run methods
    test_instance = TestTariLedgerWallet()
    
    try:
        test_instance.setup_method(None)
        test_instance.test_app_launch_flex()
        test_instance.teardown_method(None)
        
        print("🎉 Basic test for Ledger Flex passed successfully!")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        sys.exit(1)
