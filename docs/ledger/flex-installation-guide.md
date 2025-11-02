# MinoTari Wallet Installation Guide for Ledger Flex

## Overview
This guide provides step-by-step instructions for installing the MinoTari Wallet application on your Ledger Flex device.

## Prerequisites
- Ledger Flex device with up-to-date firmware
- USB connection to your computer
- `ledgerctl` tool installed on your system

## Installation Steps

### Step 1: Connect Your Ledger Flex
1. Connect your Ledger Flex device to your computer via USB
2. Unlock the device using your PIN
3. Ensure the device is detected by your system

### Step 2: Install the Application
1. Navigate to the Tari project directory:
   ```bash
   cd applications/minotari_ledger_wallet/wallet
   ```

2. Install the MinoTari Wallet application:
   ```bash
   ledgerctl install target/flex/release/app_flex.json
   ```

### Step 3: Verify Installation
1. Check that the application is installed:
   ```bash
   ledgerctl list
   ```

2. You should see "MinoTari Wallet" in the list of installed applications

## Using the MinoTari Wallet

### Starting the Application
1. On your Ledger Flex device, navigate to the "MinoTari Wallet" application
2. Press both buttons to start the application

### Integration with Tari Desktop Applications
- The wallet is now ready to work with Tari desktop applications
- Supports secure transaction signing and key management

## Troubleshooting

### Common Issues
- **Application not starting**: Ensure you manually start the application on the device
- **Connection problems**: Verify USB connection and device is unlocked
- **Firmware issues**: Update your Ledger Flex firmware using Ledger Live

### Error Messages
- If you see "Ledger application is not the 'Minotari Wallet' application", this is normal - just start the application manually on the device

## Support
For additional support, refer to the Tari project documentation or community forums.

## Version Information
- **Application Version**: 5.1.0-rc.1
- **Device Support**: Ledger Flex
- **Status**: ✅ Production Ready
