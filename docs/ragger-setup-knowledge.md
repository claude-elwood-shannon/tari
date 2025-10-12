# Ledger Test Environment Setup Knowledge

## Issue Context
- **Issue**: Ledger test environment setup
- **Target**: NanoSPlus device
- **Goal**: Compile and test Minotari Ledger Wallet application

## Key Discoveries

### 1. SDK Requirements
- **Ledger Secure SDK**: Required for compiling Ledger applications
- **Repository**: https://github.com/LedgerHQ/ledger-secure-sdk
- **Path Configuration**: `LEDGER_SDK_PATH` environment variable must point to SDK directory

### 2. Toolchain Requirements
- **Rust Toolchain**: Nightly required for Ledger development
- **Cargo Ledger**: Tool for building Ledger apps (`cargo install cargo-ledger`)
- **Rust Source**: Required for cross-compilation (`rustup component add rust-src --toolchain nightly`)

### 3. Compilation Dependencies
- **Clang**: Required for C compilation (`sudo apt install clang`)
- **ARM Toolchain**: `gcc-arm-none-eabi` for ARM cross-compilation
- **ELF Headers**: `libelf-dev` for ELF file support
- **CFLAGS**: May need manual configuration for include paths

### 4. Successful Compilation Configuration

```bash
# Environment setup
export LEDGER_SDK_PATH=/tmp/ledger_sdk
export CFLAGS="-I/usr/lib/arm-none-eabi/include"

# Compilation command
cd applications/minotari_ledger_wallet/wallet
cargo ledger build nanosplus
```

### 5. File Structure
```
minotari_ledger_wallet/
├── common/          # Common functionality
├── comms/           # Communication handlers
└── wallet/          # Main application
    ├── Cargo.toml   # Dependencies
    ├── src/         # Source code
    └── target/      # Build output
```

### 6. Compilation Output
- **Binary Size**: 121,248 bytes text + 9,740 bytes bss = 130,988 bytes total
- **Output Files**:
  - `minotari_ledger_wallet` (binary)
  - `minotari_ledger_wallet.apdu` (APDU installation file)

### 7. Troubleshooting Issues

#### Disk Space Management
- **Problem**: Installation failed due to insufficient disk space
- **Solution**: Clean temporary files and manage space efficiently
- **Commands**:
  ```bash
  sudo apt autoremove -y
  sudo apt clean
  ```

#### Missing Dependencies
- **elf.h not found**: Required ARM toolchain headers
- **Solution**: Install `gcc-arm-none-eabi` and configure include paths

### 8. Testing Considerations

#### Ragger Integration
- **Purpose**: Automated testing framework for Ledger applications
- **Setup**: Requires Docker or manual environment configuration
- **Alternative**: Manual testing with physical device or emulator

#### Device Communication
- **APDU Protocol**: Application Protocol Data Unit for device communication
- **Handlers**: Implemented in `comms/` directory for different operations

### 9. Development Workflow

1. **Environment Setup**
   ```bash
   git clone https://github.com/LedgerHQ/ledger-secure-sdk.git /tmp/ledger_sdk
   export LEDGER_SDK_PATH=/tmp/ledger_sdk
   export CFLAGS="-I/usr/lib/arm-none-eabi/include"
   ```

2. **Dependency Installation**
   ```bash
   cargo install cargo-ledger
   rustup component add rust-src --toolchain nightly
   sudo apt install clang libelf-dev gcc-arm-none-eabi
   ```

3. **Compilation**
   ```bash
   cd applications/minotari_ledger_wallet/wallet
   cargo ledger build nanosplus
   ```

4. **Testing**
   - Use Ragger for automated testing
   - Manual testing with Ledger device
   - APDU command validation

### 10. Architecture Insights

#### Application Structure
- **Main Handler**: Central application logic in `wallet/src/main.rs`
- **Command Handlers**: Individual handlers for different operations
- **Common Utilities**: Shared functionality in `common/` directory

#### Security Considerations
- **Secure Element**: All cryptographic operations on secure element
- **APDU Security**: Proper validation of incoming commands
- **Memory Management**: Limited resources on Ledger devices

### 11. Future Improvements

#### Testing Infrastructure
- **Ragger Integration**: Complete automated testing setup
- **CI/CD Pipeline**: Automated builds and tests
- **Device Emulation**: Software emulation for development

#### Development Tools
- **Debugging Support**: Better debugging tools for Ledger development
- **Documentation**: Comprehensive setup and usage guides
- **Error Handling**: Improved error messages and recovery

## Summary

The Ledger test environment setup requires careful configuration of multiple components including the SDK, toolchain, and compilation environment. The successful compilation demonstrates that the core application architecture is sound, but comprehensive testing infrastructure remains to be implemented.

**Key Success Factors**:
- Correct SDK configuration
- Proper toolchain installation
- Appropriate compilation flags
- Sufficient disk space management

**Next Steps**:
1. Implement Ragger testing framework
2. Set up automated testing pipeline
3. Develop comprehensive test cases
4. Document deployment procedures
