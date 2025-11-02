# MinoTari Wallet Installation Guide for Ledger Flex

## Overview
This guide provides complete instructions for building and installing the MinoTari Wallet application on your Ledger Flex device.

## Prerequisites
- Ledger Flex device with up-to-date firmware
- USB connection to your computer
- `ledgerctl` tool installed on your system
- Rust toolchain and Ledger development environment

## Step 1: Build the Application

### Prerequisites for Building
Ensure you have the necessary development tools:
```bash
# Install Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Install Ledger development tools
cargo install ledgerctl
```

### Build Process
1. Navigate to the Tari project directory:
   ```bash
   cd applications/minotari_ledger_wallet/wallet
   ```

2. Build the application for Ledger Flex:
   ```bash
   cargo ledger build --target flex --release
   ```

3. Verify the build output:
   ```bash
   ls target/flex/release/
   ```
   You should see:
   - `app_flex.json` - Installation file
   - `minotari_ledger_wallet.hex` - Compiled binary
   - `key_40x40.gif` - Device icon

## Step 2: Install on Ledger Flex

### Connect Your Device
1. Connect your Ledger Flex device to your computer via USB
2. Unlock the device using your PIN
3. Ensure the device is detected by your system

### Install the Application
```bash
ledgerctl install target/flex/release/app_flex.json
```

### Verify Installation
```bash
ledgerctl list
```
You should see "MinoTari Wallet" in the list of installed applications.

## Step 3: Using the MinoTari Wallet

### Starting the Application
1. On your Ledger Flex device, navigate to the "MinoTari Wallet" application
2. Press both buttons to start the application

### Integration with Tari Desktop Applications
- The wallet is now ready to work with Tari desktop applications
- Supports secure transaction signing and key management

## Troubleshooting

### Build Issues
- **Missing dependencies**: Ensure all Ledger development tools are installed
- **Build errors**: Check Rust toolchain version and Ledger SDK compatibility

### Installation Issues
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
