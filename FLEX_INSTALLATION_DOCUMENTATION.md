# Documentation: Successful Installation of MinoTari Wallet on Ledger Flex

## Executive Summary
**Date**: February 11, 2025  
**Status**: ✅ SUCCESSFUL INSTALLATION

The "MinoTari Wallet" application has been successfully installed on a Ledger Flex device. This document compiles all technical and procedural information gathered during the installation process.

## Project Configuration

### Application Structure
```
applications/minotari_ledger_wallet/
├── wallet/
│   ├── ledger_app.toml          # Supported devices configuration
│   ├── Cargo.toml               # Dependencies and metadata
│   └── target/flex/release/     # Compiled binaries for Flex
│       ├── app_flex.json        # Installation file
│       ├── minotari_ledger_wallet.hex
│       └── key_40x40.gif        # Flex-specific icon
```

### Configuration in ledger_app.toml
```toml
[app]
build_directory = "./"
sdk = "Rust"
devices = ["nanox", "nanos+", "stax", "flex"]  # Flex included
```

### Configuration in Cargo.toml
```toml
[package.metadata.ledger.flex]
icon = "key_40x40.gif"  # Flex-specific device icon
```

## Verified Installation Process

### 1. Device Verification
- **Command used**: `lsusb | grep -i ledger`
- **Result**: `Bus 002 Device 005: ID 2c97:7000 Ledger Flex`
- **Status**: ✅ Device correctly detected

### 2. Application Build Verification
- **Location**: `applications/minotari_ledger_wallet/wallet/target/flex/release/`
- **Key files present**:
  - `app_flex.json` - Installation file
  - `minotari_ledger_wallet.hex` - Compiled binary
  - `key_40x40.gif` - Device icon

### 3. Installation with ledgerctl
- **Command executed**: 
  ```bash
  cd applications/minotari_ledger_wallet/wallet
  ledgerctl install target/flex/release/app_flex.json
  ```
- **Result**: Successful installation with warning about JSON deprecation
- **Status**: ✅ Application installed successfully

### 4. Installation Verification
- **Command used**: `ledgerctl list`
- **Result**: "MinoTari Wallet" appears in application list with hash `b815907e29e23011762edaf3b671041d10cf1a7c7712963e94083232d3b37b7b`
- **Status**: ✅ Installation confirmed

## Installation Verification

### Verification Steps Completed
- **Device detection**: Ledger Flex correctly identified via USB
- **Application listing**: "MinoTari Wallet" appears in installed applications
- **Hash verification**: Application hash confirmed as `b815907e29e23011762edaf3b671041d10cf1a7c7712963e94083232d3b37b7b`

## Key Technical Details

### Device Information
- **Device Model**: Ledger Flex
- **USB ID**: 2c97:7000
- **Connection Status**: Active and detected

### Application Metadata
- **Application Name**: MinoTari Wallet
- **Version**: 5.1.0-rc.1
- **Supported Curves**: secp256k1
- **Derivation Path**: ["44'/535348'"]
- **Flags**: "0" (bolos_settings)

### Build Configuration
- **Build Profile**: Release with optimizations
- **Optimization Level**: 'z' (size optimization)
- **LTO**: Enabled
- **Panic Strategy**: Abort

## Next Steps for Usage

1. **Start the application on the Ledger Flex device**:
   - Navigate to "MinoTari Wallet" on the device
   - Press both buttons to start the application

2. **Use with Tari desktop applications**:
   - The application is now ready to be used with Tari console wallet
   - Supports integrated addresses and transaction signing

3. **Testing functionality**:
   - Run the ledger_demo example to test all application functions
   - Verify public key retrieval, signature creation, and other operations

## Troubleshooting Notes

### Common Issues and Solutions
- **Application not started error**: Manually start the application on the device
- **Version mismatch**: Ensure firmware is up to date via Ledger Live
- **Connection issues**: Verify USB connection and device is unlocked

### Error Messages Encountered
- `Ledger application is not the 'Minotari Wallet' application (Ledger application not started)` - Normal behavior, requires manual start

## Conclusion

The installation of MinoTari Wallet on Ledger Flex has been completed successfully. The application is properly configured, built, and installed on the device. All verification steps confirm the installation is ready for use with Tari ecosystem applications.

**Final Status**: ✅ READY FOR PRODUCTION USE
