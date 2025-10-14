#!/usr/bin/env python3
"""
Direct Speculos test that bypasses Ragger to verify the application works
"""

import os
import sys
import time
import subprocess
import requests
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('direct_speculos_test.log', mode='w')
    ]
)

logger = logging.getLogger(__name__)

def test_direct_speculos():
    """Test Speculos directly without Ragger"""
    logger.info("=== Starting direct Speculos test ===")
    
    # Path to the application
    app_path = Path("applications/minotari_ledger_wallet/wallet/target/flex/release/minotari_ledger_wallet")
    
    if not app_path.exists():
        logger.error(f"Application not found at {app_path}")
        return False
    
    logger.info(f"Application found: {app_path}")
    
    # Start Speculos manually
    speculos_process = None
    api_port = 5000
    apdu_port = 5001
    
    try:
        logger.info("Starting Speculos manually...")
        speculos_process = subprocess.Popen([
            "speculos",
            str(app_path),
            "--model", "flex",
            "--api-port", str(api_port),
            "--apdu-port", str(apdu_port),
            "--display", "headless"  # Run in headless mode
            # Don't specify API level to use default
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for Speculos to start
        logger.info("Waiting for Speculos to start...")
        time.sleep(3)
        
        # Check if Speculos is running
        if speculos_process.poll() is not None:
            stdout, stderr = speculos_process.communicate()
            logger.error(f"Speculos failed to start: {stderr.decode()}")
            return False
        
        logger.info("✅ Speculos started successfully")
        
        # Test API connection
        logger.info("Testing API connection...")
        try:
            response = requests.get(f"http://127.0.0.1:{api_port}/")
            if response.status_code == 200:
                logger.info("✅ API connection successful")
            else:
                logger.error(f"❌ API connection failed: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            logger.error("❌ API connection refused")
            return False
        
        # Test APDU command (GetVersion - INS=0x01)
        logger.info("Testing APDU command...")
        
        # Build APDU: CLA=0x80, INS=0x01, P1=0x00, P2=0x00
        apdu_data = {
            "data": "80010000"  # Hex string
        }
        
        try:
            response = requests.post(
                f"http://127.0.0.1:{api_port}/apdu",
                json=apdu_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ APDU response: {result}")
                logger.info("✅ APDU test successful!")
                return True
            else:
                logger.error(f"❌ APDU request failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ APDU request error: {e}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False
    finally:
        # Cleanup
        if speculos_process and speculos_process.poll() is None:
            logger.info("Stopping Speculos...")
            speculos_process.terminate()
            speculos_process.wait()

if __name__ == "__main__":
    logger.info("Starting direct Speculos test")
    
    if test_direct_speculos():
        logger.info("🎉 Direct Speculos test completed successfully!")
        print("🎉 Direct Speculos test completed successfully!")
    else:
        logger.error("❌ Direct Speculos test failed")
        print("❌ Direct Speculos test failed")
        sys.exit(1)
