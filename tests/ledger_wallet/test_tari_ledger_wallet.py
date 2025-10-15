#!/usr/bin/env python3
"""
Main test for Tari Ledger Wallet

This is the primary test script for the Minotari Ledger Wallet application.
It uses SpeculosClient to test APDU commands and wallet functionality on Ledger devices.
"""

import os
import sys
import time
import logging
from pathlib import Path

# Add speculos to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'speculos'))

try:
    from speculos.client import SpeculosClient
    from ledgered.devices import Devices
except ImportError as e:
    print(f"Error importing Speculos: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('tari_ledger_wallet_test.log', mode='w')
    ]
)

logger = logging.getLogger(__name__)

class PersistentTariTest:
    """Test class using persistent Speculos session"""
    
    # Tari-specific APDU constants
    WALLET_CLA = 0x80
    GET_VERSION = 0x01
    GET_APP_NAME = 0x02
    
    def __init__(self):
        self.client = None
        self.app_path = self._get_app_path()
    
    def _get_app_path(self):
        """Get the path to the compiled application"""
        app_path = Path("applications/minotari_ledger_wallet/wallet/target/flex/release/minotari_ledger_wallet")
        if not app_path.exists():
            raise FileNotFoundError(f"Application not found at {app_path}")
        return str(app_path)
    
    def _build_apdu_command(self, instruction, p1=0x00, p2=0x00, data=b""):
        """Build APDU command for Tari wallet"""
        return bytes([self.WALLET_CLA, instruction, p1, p2, len(data)]) + data
    
    def start_speculos(self):
        """Start Speculos with persistent session"""
        logger.info("Starting persistent Speculos session...")
        
        # Get Flex device configuration
        flex_device = Devices.get_by_name("flex")
        
        # Start Speculos with explicit ports to avoid conflicts
        self.client = SpeculosClient(
            app=self.app_path,
            args=["--model", "flex", "--api-port", "5000", "--apdu-port", "5001", "--display", "headless"]
        )
        
        # Start the session
        self.client.start()
        logger.info("✅ Persistent Speculos session started")
        
        # Wait for application to be ready
        time.sleep(2)
        
        # Get initial screen content to verify it's working
        screen_content = self.client.get_current_screen_content()
        logger.info(f"Initial screen content: {screen_content}")
    
    def stop_speculos(self):
        """Stop Speculos session"""
        if self.client:
            logger.info("Stopping Speculos session...")
            self.client.stop()
            self.client = None
            logger.info("✅ Speculos session stopped")
    
    def test_get_app_name(self):
        """Test GetAppName command with persistent session"""
        if not self.client:
            raise RuntimeError("Speculos session not started")
        
        logger.info("Testing GetAppName command...")
        
        # Build APDU command
        apdu_command = self._build_apdu_command(self.GET_APP_NAME)
        logger.debug(f"APDU command: {apdu_command.hex()}")
        
        # Send command
        response = self.client.apdu_exchange(
            cla=self.WALLET_CLA,
            ins=self.GET_APP_NAME,
            data=b""
        )
        
        # Decode the response (hex to ASCII)
        app_name_decoded = response.decode('ascii', errors='ignore')
        logger.info(f"GetAppName response (hex): {response.hex()}")
        logger.info(f"GetAppName response (decoded): '{app_name_decoded}'")
        logger.info(f"Response length: {len(response)} bytes")
        
        # Verify response
        assert len(response) > 0, "Empty response"
        logger.info("✅ GetAppName test passed")
        
        return response
    
    def test_get_version(self):
        """Test GetVersion command with persistent session"""
        if not self.client:
            raise RuntimeError("Speculos session not started")
        
        logger.info("Testing GetVersion command...")
        
        # Build APDU command
        apdu_command = self._build_apdu_command(self.GET_VERSION)
        logger.debug(f"APDU command: {apdu_command.hex()}")
        
        # Send command
        response = self.client.apdu_exchange(
            cla=self.WALLET_CLA,
            ins=self.GET_VERSION,
            data=b""
        )
        
        # Decode the response (hex to ASCII)
        version_decoded = response.decode('ascii', errors='ignore')
        logger.info(f"GetVersion response (hex): {response.hex()}")
        logger.info(f"GetVersion response (decoded): '{version_decoded}'")
        logger.info(f"Response length: {len(response)} bytes")
        
        # Verify response
        assert len(response) > 0, "Empty response"
        logger.info("✅ GetVersion test passed")
        
        return response
    
    def test_multiple_commands(self):
        """Test multiple APDU commands in the same session"""
        if not self.client:
            raise RuntimeError("Speculos session not started")
        
        logger.info("Testing multiple APDU commands in persistent session...")
        
        # Test sequence of commands
        commands = [
            (self.GET_APP_NAME, "GetAppName"),
            (self.GET_VERSION, "GetVersion"),
        ]
        
        for instruction, name in commands:
            logger.info(f"Testing {name}...")
            
            response = self.client.apdu_exchange(
                cla=self.WALLET_CLA,
                ins=instruction,
                data=b""
            )
            
            # Decode the response based on command type
            if name == "GetAppName":
                decoded = response.decode('ascii', errors='ignore')
                logger.info(f"{name} response (hex): {response.hex()}")
                logger.info(f"{name} response (decoded): '{decoded}'")
            elif name == "GetVersion":
                decoded = response.decode('ascii', errors='ignore')
                logger.info(f"{name} response (hex): {response.hex()}")
                logger.info(f"{name} response (decoded): '{decoded}'")
            else:
                logger.info(f"{name} response: {response.hex()}")
            
            assert len(response) > 0, f"Empty response for {name}"
            logger.info(f"✅ {name} test passed")
            
            # Small delay between commands
            time.sleep(0.5)
        
        logger.info("✅ All multiple command tests passed")


def main():
    """Main function to run persistent tests"""
    logger.info("=== Starting Persistent Speculos Tests ===")
    
    test_instance = PersistentTariTest()
    
    try:
        # Start persistent session
        test_instance.start_speculos()
        
        # Run tests in the same session
        test_instance.test_get_app_name()
        test_instance.test_get_version()
        test_instance.test_multiple_commands()
        
        logger.info("🎉 All persistent tests passed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test error: {e}")
        raise
    finally:
        # Always stop Speculos
        test_instance.stop_speculos()


if __name__ == "__main__":
    main()
