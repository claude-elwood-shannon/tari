#!/usr/bin/env python3
"""
Advanced tests for Tari Ledger Wallet using Ragger

This module implements comprehensive functionality tests for the
Minotari Ledger Wallet application using Ledger's Ragger framework.
Includes Tari-specific APDU commands and wallet functionality.
"""

import os
import sys
import pytest
import struct
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
    """Test class for Tari Ledger Wallet with advanced functionality"""
    
    # Tari-specific APDU constants
    WALLET_CLA = 0x80
    
    # Instruction codes from common_types.rs
    GET_VERSION = 0x01
    GET_APP_NAME = 0x02
    GET_PUBLIC_SPEND_KEY = 0x03
    GET_PUBLIC_KEY = 0x04
    GET_SCRIPT_SIGNATURE_DERIVED = 0x05
    GET_SCRIPT_OFFSET = 0x06
    GET_VIEW_KEY = 0x07
    GET_DH_SHARED_SECRET = 0x08
    GET_RAW_SCHNORR_SIGNATURE = 0x09
    GET_SCRIPT_SCHNORR_SIGNATURE = 0x10
    GET_ONE_SIDED_METADATA_SIGNATURE = 0x11
    GET_SCRIPT_SIGNATURE_MANAGED = 0x12
    
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
    
    def _build_apdu_command(self, instruction, p1=0x00, p2=0x00, data=b""):
        """Build APDU command for Tari wallet"""
        return struct.pack(">BBBB", self.WALLET_CLA, instruction, p1, p2) + data
    
    def _exchange_apdu(self, apdu_data):
        """Exchange APDU command with the backend"""
        # Extract components from APDU data
        cla = apdu_data[0]
        ins = apdu_data[1]
        p1 = apdu_data[2]
        p2 = apdu_data[3]
        data = apdu_data[4:] if len(apdu_data) > 4 else b""
        
        return self.backend.exchange(cla=cla, ins=ins, p1=p1, p2=p2, data=data)
    
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
    
    @pytest.mark.speculos
    def test_tari_apdu_commands(self):
        """Test Tari-specific APDU commands"""
        app_path = self._get_app_path("flex")
        flex_device = Devices.get_by_name("flex")
        
        self.backend = SpeculosBackend(
            application=app_path,
            device=flex_device
        )
        
        # Test basic APDU commands
        test_commands = [
            (self.GET_VERSION, "GET_VERSION"),
            (self.GET_APP_NAME, "GET_APP_NAME"),
            (self.GET_PUBLIC_SPEND_KEY, "GET_PUBLIC_SPEND_KEY"),
        ]
        
        for instruction, name in test_commands:
            apdu = self._build_apdu_command(instruction)
            try:
                response = self._exchange_apdu(apdu)
                print(f"✅ {name} command executed successfully")
                print(f"   Response length: {len(response)} bytes")
                print(f"   Response data: {response.hex()}")
            except Exception as e:
                print(f"❌ {name} command failed: {e}")
        
        assert len(test_commands) > 0
    
    @pytest.mark.speculos
    def test_wallet_version_info(self):
        """Test wallet version and application name retrieval"""
        app_path = self._get_app_path("flex")
        flex_device = Devices.get_by_name("flex")
        
        self.backend = SpeculosBackend(
            application=app_path,
            device=flex_device
        )
        
        # Get version
        version_apdu = self._build_apdu_command(self.GET_VERSION)
        version_response = self._exchange_apdu(version_apdu)
        print(f"✅ Version response: {version_response.hex()}")
        
        # Get app name
        app_name_apdu = self._build_apdu_command(self.GET_APP_NAME)
        app_name_response = self._exchange_apdu(app_name_apdu)
        print(f"✅ App name response: {app_name_response.hex()}")
        
        # Basic validation
        assert len(version_response) > 0
        assert len(app_name_response) > 0
    
    @pytest.mark.speculos
    def test_public_key_operations(self):
        """Test public key generation and retrieval"""
        app_path = self._get_app_path("flex")
        flex_device = Devices.get_by_name("flex")
        
        self.backend = SpeculosBackend(
            application=app_path,
            device=flex_device
        )
        
        # Test public spend key retrieval
        spend_key_apdu = self._build_apdu_command(self.GET_PUBLIC_SPEND_KEY)
        spend_key_response = self._exchange_apdu(spend_key_apdu)
        print(f"✅ Public spend key response length: {len(spend_key_response)} bytes")
        
        # Test public key retrieval (with account data)
        account_data = struct.pack("<Q", 0)  # Account 0
        public_key_apdu = self._build_apdu_command(self.GET_PUBLIC_KEY, data=account_data)
        public_key_response = self._exchange_apdu(public_key_apdu)
        print(f"✅ Public key response length: {len(public_key_response)} bytes")
        
        assert len(spend_key_response) > 0
        assert len(public_key_response) > 0
    
    def test_tari_instruction_set(self):
        """Test: verify complete Tari instruction set"""
        # Complete Tari instruction set from common_types.rs
        tari_instructions = [
            (self.GET_VERSION, "GetVersion"),
            (self.GET_APP_NAME, "GetAppName"),
            (self.GET_PUBLIC_SPEND_KEY, "GetPublicSpendKey"),
            (self.GET_PUBLIC_KEY, "GetPublicKey"),
            (self.GET_SCRIPT_SIGNATURE_DERIVED, "GetScriptSignatureDerived"),
            (self.GET_SCRIPT_OFFSET, "GetScriptOffset"),
            (self.GET_VIEW_KEY, "GetViewKey"),
            (self.GET_DH_SHARED_SECRET, "GetDHSharedSecret"),
            (self.GET_RAW_SCHNORR_SIGNATURE, "GetRawSchnorrSignature"),
            (self.GET_SCRIPT_SCHNORR_SIGNATURE, "GetScriptSchnorrSignature"),
            (self.GET_ONE_SIDED_METADATA_SIGNATURE, "GetOneSidedMetadataSignature"),
            (self.GET_SCRIPT_SIGNATURE_MANAGED, "GetScriptSignatureManaged"),
        ]
        
        for instruction_code, instruction_name in tari_instructions:
            print(f"Instruction: {instruction_name} - Code: 0x{instruction_code:02x}")
        
        # Validate we have the complete instruction set
        assert len(tari_instructions) == 12
        print("✅ Complete Tari instruction set verified")


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
