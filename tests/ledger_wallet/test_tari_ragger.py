#!/usr/bin/env python3
"""
Tari Ledger Wallet tests using Ragger framework

This test file uses Ragger's pytest integration to test the Minotari Ledger Wallet
application following the official Ragger testing patterns.
"""

import pytest
import struct
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tari-specific APDU constants
WALLET_CLA = 0x80
GET_VERSION = 0x01
GET_APP_NAME = 0x02
GET_PUBLIC_SPEND_KEY = 0x03
GET_PUBLIC_KEY = 0x04

def test_tari_app_launch(backend):
    """Test that the Tari application launches successfully"""
    logger.info("Testing Tari Ledger Wallet application launch")
    
    # The backend fixture automatically starts Speculos with the application
    # The application path is expected to be in the standard Ledger build location
    assert backend is not None
    logger.info("✅ Tari application launched successfully")


def test_get_app_name(backend):
    """Test GetAppName command using Ragger backend"""
    logger.info("Testing GetAppName command")
    
    # Send command using Ragger's exchange method
    response = backend.exchange(
        cla=WALLET_CLA,
        ins=GET_APP_NAME,
        p1=0x00,
        p2=0x00,
        data=b""
    )
    
    # RAPDU object has data and status attributes
    logger.info(f"GetAppName response (hex): {response.data.hex()}")
    logger.info(f"GetAppName response (decoded): '{response.data.decode('ascii', errors='ignore')}'")
    logger.info(f"Response length: {len(response.data)} bytes")
    logger.info(f"Response status: {hex(response.status)}")
    
    # Verify response
    assert len(response.data) > 0, "Empty response"
    assert response.status == 0x9000, f"Unexpected status: {hex(response.status)}"
    logger.info("✅ GetAppName test passed")


def test_get_version(backend):
    """Test GetVersion command using Ragger backend"""
    logger.info("Testing GetVersion command")
    
    # Send command using Ragger's exchange method
    response = backend.exchange(
        cla=WALLET_CLA,
        ins=GET_VERSION,
        p1=0x00,
        p2=0x00,
        data=b""
    )
    
    # RAPDU object has data and status attributes
    logger.info(f"GetVersion response (hex): {response.data.hex()}")
    logger.info(f"GetVersion response (decoded): '{response.data.decode('ascii', errors='ignore')}'")
    logger.info(f"Response length: {len(response.data)} bytes")
    logger.info(f"Response status: {hex(response.status)}")
    
    # Verify response
    assert len(response.data) > 0, "Empty response"
    assert response.status == 0x9000, f"Unexpected status: {hex(response.status)}"
    logger.info("✅ GetVersion test passed")


def test_get_public_spend_key(backend):
    """Test GET_PUBLIC_SPEND_KEY command with account number"""
    logger.info("Testing GET_PUBLIC_SPEND_KEY command")
    
    # Account number 0 (8 bytes in little-endian)
    account_number = 0
    account_bytes = account_number.to_bytes(8, byteorder='little')
    
    # Send command using Ragger's exchange method
    response = backend.exchange(
        cla=WALLET_CLA,
        ins=GET_PUBLIC_SPEND_KEY,
        p1=0x00,
        p2=0x00,
        data=account_bytes  # 8 bytes para account number
    )
    
    # RAPDU object has data and status attributes
    logger.info(f"GET_PUBLIC_SPEND_KEY response (hex): {response.data.hex()}")
    logger.info(f"Response length: {len(response.data)} bytes")
    logger.info(f"Response status: {hex(response.status)}")
    
    # Verify response structure: version (1 byte) + public key (32 bytes)
    assert len(response.data) == 33, f"Expected 33 bytes, got {len(response.data)}"
    assert response.data[0] == 1, f"Expected version 1, got {response.data[0]}"  # RESPONSE_VERSION
    assert response.status == 0x9000, f"Unexpected status: {hex(response.status)}"
    
    # Log the public key (32 bytes after version)
    public_key_hex = response.data[1:].hex()
    logger.info(f"Public key: {public_key_hex}")
    logger.info("✅ GET_PUBLIC_SPEND_KEY test passed")


def test_get_public_key(backend):
    """Test GET_PUBLIC_KEY command with account, index, and key type"""
    logger.info("Testing GET_PUBLIC_KEY command")
    
    # Prepare data: account (8 bytes), index (8 bytes), key type (8 bytes)
    account_number = 0
    index = 0
    key_type = 0x01  # Spend key type (valid value)
    
    account_bytes = account_number.to_bytes(8, byteorder='little')
    index_bytes = index.to_bytes(8, byteorder='little')
    key_type_bytes = key_type.to_bytes(8, byteorder='little')
    
    # Combine all data (24 bytes total)
    data = account_bytes + index_bytes + key_type_bytes
    
    # Send command using Ragger's exchange method
    response = backend.exchange(
        cla=WALLET_CLA,
        ins=GET_PUBLIC_KEY,
        p1=0x00,
        p2=0x00,
        data=data
    )
    
    # RAPDU object has data and status attributes
    logger.info(f"GET_PUBLIC_KEY response (hex): {response.data.hex()}")
    logger.info(f"Response length: {len(response.data)} bytes")
    logger.info(f"Response status: {hex(response.status)}")
    
    # Verify response structure: version (1 byte) + public key (32 bytes)
    assert len(response.data) == 33, f"Expected 33 bytes, got {len(response.data)}"
    assert response.data[0] == 1, f"Expected version 1, got {response.data[0]}"  # RESPONSE_VERSION
    assert response.status == 0x9000, f"Unexpected status: {hex(response.status)}"
    
    # Log the public key (32 bytes after version)
    public_key_hex = response.data[1:].hex()
    logger.info(f"Public key: {public_key_hex}")
    logger.info("✅ GET_PUBLIC_KEY test passed")


def test_multiple_commands(backend):
    """Test multiple APDU commands in sequence"""
    logger.info("Testing multiple APDU commands")
    
    # Test sequence of commands
    commands = [
        (GET_APP_NAME, "GetAppName", b""),
        (GET_VERSION, "GetVersion", b""),
        (GET_PUBLIC_SPEND_KEY, "GetPublicSpendKey", (0).to_bytes(8, byteorder='little')),
        (GET_PUBLIC_KEY, "GetPublicKey", (0).to_bytes(8, byteorder='little') + (0).to_bytes(8, byteorder='little') + (0x01).to_bytes(8, byteorder='little')),
    ]
    
    for instruction, name, data in commands:
        logger.info(f"Testing {name}...")
        
        response = backend.exchange(
            cla=WALLET_CLA,
            ins=instruction,
            p1=0x00,
            p2=0x00,
            data=data
        )
        
        # RAPDU object has data and status attributes
        logger.info(f"{name} response (hex): {response.data.hex()}")
        logger.info(f"{name} response (decoded): '{response.data.decode('ascii', errors='ignore')}'")
        logger.info(f"{name} response length: {len(response.data)} bytes")
        logger.info(f"{name} response status: {hex(response.status)}")
        
        # Verify response
        assert len(response.data) > 0, f"Empty response for {name}"
        assert response.status == 0x9000, f"Unexpected status for {name}: {hex(response.status)}"
        logger.info(f"✅ {name} test passed")
    
    logger.info("✅ All multiple command tests passed")


@pytest.mark.use_on_backend("speculos")
def test_speculos_only(backend):
    """Test that only runs on Speculos backend"""
    logger.info("Testing Speculos-specific functionality")
    
    # This test will only run when using --backend speculos
    response = backend.exchange(
        cla=WALLET_CLA,
        ins=GET_APP_NAME,
        p1=0x00,
        p2=0x00,
        data=b""
    )
    
    # RAPDU object has data and status attributes
    assert len(response.data) > 0, "Empty response"
    assert response.status == 0x9000, f"Unexpected status: {hex(response.status)}"
    logger.info("✅ Speculos-only test passed")


if __name__ == "__main__":
    # This allows running the tests directly for debugging
    import sys
    import os
    from pathlib import Path
    
    # Add parent directory to path for imports
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    # Run a simple test to verify the setup
    logger.info("Running basic Ragger test verification")
    
    try:
        from ragger.backend import SpeculosBackend
        from ledgered.devices import Devices
        
        # Test basic functionality
        app_path = Path("applications/minotari_ledger_wallet/wallet/target/flex/release/minotari_ledger_wallet")
        if app_path.exists():
            logger.info(f"Application found: {app_path}")
            
            # This is just for verification - actual tests should use pytest
            logger.info("✅ Ragger setup verified")
        else:
            logger.error(f"Application not found at {app_path}")
            
    except ImportError as e:
        logger.error(f"Error importing Ragger: {e}")
        sys.exit(1)
