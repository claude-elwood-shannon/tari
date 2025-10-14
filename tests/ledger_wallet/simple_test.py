#!/usr/bin/env python3
"""
Simple test for Tari Ledger Wallet that actually works with Speculos
"""

import os
import sys
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('simple_test_debug.log', mode='w')
    ]
)

logger = logging.getLogger(__name__)

# Add root directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from ragger.backend import SpeculosBackend
    from ragger.navigator import Navigator
    from ledgered.devices import Devices
except ImportError as e:
    logger.error(f"Error importing Ragger: {e}")
    sys.exit(1)

def test_simple_apdu():
    """Simple test that actually works with Speculos"""
    logger.info("=== Starting simple APDU test ===")
    
    # Path to the application
    app_path = Path("applications/minotari_ledger_wallet/wallet/target/flex/release/minotari_ledger_wallet")
    
    if not app_path.exists():
        logger.error(f"Application not found at {app_path}")
        return False
    
    logger.info(f"Application found: {app_path}")
    
    # Get the Flex device
    flex_device = Devices.get_by_name("flex")
    logger.info(f"Using device: {flex_device.name}")
    
    try:
        # Initialize Speculos backend
        logger.info("Initializing Speculos backend...")
        backend = SpeculosBackend(
            application=str(app_path),
            device=flex_device
        )
        
        logger.info("Initializing Navigator...")
        navigator = Navigator(
            backend=backend,
            device=flex_device,
            callbacks={}
        )
        
        logger.info("✅ Speculos backend initialized successfully")
        
        # Wait a bit for Speculos to fully start
        time.sleep(2)
        
        # Test a simple APDU command (GetVersion - INS=0x01)
        logger.info("Testing GetVersion command...")
        
        # Build APDU: CLA=0x80, INS=0x01, P1=0x00, P2=0x00
        apdu_data = bytes([0x80, 0x01, 0x00, 0x00])
        
        logger.info(f"Sending APDU: {apdu_data.hex()}")
        
        # Send the APDU command
        response = backend.exchange(
            cla=0x80,
            ins=0x01,
            p1=0x00,
            p2=0x00,
            data=b""
        )
        
        logger.info(f"✅ Response received: {response.hex()}")
        logger.info(f"Response length: {len(response)} bytes")
        
        # Check if we got a valid response
        if response and len(response) > 0:
            logger.info("✅ APDU test successful!")
            return True
        else:
            logger.error("❌ No response received")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False
    finally:
        # Cleanup
        if 'backend' in locals():
            logger.info("Closing Speculos backend...")
            # SpeculosBackend should handle cleanup automatically

if __name__ == "__main__":
    logger.info("Starting simple Tari Ledger Wallet test")
    
    if test_simple_apdu():
        logger.info("🎉 Simple test completed successfully!")
        print("🎉 Simple test completed successfully!")
    else:
        logger.error("❌ Simple test failed")
        print("❌ Simple test failed")
        sys.exit(1)
