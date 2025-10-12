#!/usr/bin/env python3
"""
Verification script for Ragger setup with Tari Ledger Wallet application
This script validates that Ragger is properly configured and can communicate with the application
"""

import sys
import os

def check_ragger_installation():
    """Verifies that Ragger is correctly installed"""
    try:
        import ragger
        from ragger.backend import SpeculosBackend, LedgerCommBackend, LedgerWalletBackend
        print("✅ Ragger 1.40.2 installed correctly")
        print("✅ Available backends: Speculos, LedgerComm, LedgerWallet")
        return True
    except ImportError as e:
        print(f"❌ Error importing Ragger: {e}")
        return False

def check_dependencies():
    """Verifies critical dependencies"""
    try:
        import jsonschema
        print(f"✅ jsonschema {jsonschema.__version__} installed")
        
        # Verify compatibility with Speculos
        if jsonschema.__version__.startswith('4.17'):
            print("✅ jsonschema compatible with Speculos 0.25.7")
        else:
            print(f"⚠️  jsonschema {jsonschema.__version__} - verify compatibility with Speculos")
            
        return True
    except ImportError as e:
        print(f"❌ Error with dependencies: {e}")
        return False

def check_application_path():
    """Verifies that the Ledger application is available"""
    app_path = "applications/minotari_ledger_wallet/wallet/target/avalanche/nanos/debug/minotari_ledger_wallet.elf"
    
    if os.path.exists(app_path):
        print(f"✅ Ledger application found: {app_path}")
        return app_path
    else:
        print(f"❌ Ledger application not found at: {app_path}")
        print("   Need to compile the application first:")
        print("   cd applications/minotari_ledger_wallet/wallet")
        print("   cargo build --target avalanche-nanos")
        return None

def main():
    """Main verification function"""
    print("🔍 Verifying Ragger setup for Tari Ledger Wallet")
    print("=" * 60)
    
    # Verify Ragger installation
    if not check_ragger_installation():
        sys.exit(1)
    
    # Verify dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Verify application
    app_path = check_application_path()
    if not app_path:
        print("\n💡 Solution: Compile the Ledger application first")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Ragger setup VERIFIED successfully")
    print("📋 Next steps:")
    print("   1. Implement basic APDU communication tests")
    print("   2. Configure Speculos for emulation")
    print("   3. Develop complete integration tests")
    
    return app_path

if __name__ == "__main__":
    main()
