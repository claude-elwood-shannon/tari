# CI Integration with Ledger App Builder

This document describes how to integrate the Tari Ledger Wallet testing framework with the CI system using Ledger's official Docker image.

## Overview

The project already has a CI workflow configured in `.github/workflows/build_ledger_wallet.yml` that uses Ledger's official Docker image to compile the application for multiple devices.

## Existing CI Workflow

### Current Configuration

The current workflow:
- **Docker Image**: `ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:4.15.0`
- **Supported Devices**: 
  - ✅ `nanosplus` (working correctly)
  - ✅ `flex` (working correctly)
  - ⚠️ `nanox` (best_effort: true)
  - ⚠️ `stax` (best_effort: true)

### Compilation Command

```yaml
docker run --rm \
  -v ".:/app" \
  -w "/app/applications/minotari_ledger_wallet/wallet" \
  ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:4.15.0 \
  cargo ledger build ${{ matrix.ledger_target }} -- --locked
```

## Available Docker Images

### Image Types

1. **`ledger-app-builder`** (full image)
   - Base: Debian slim + Rust tools
   - Use: Standard compilation
   - Command: `docker pull ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:latest`

2. **`ledger-app-builder-lite`** (lightweight image)
   - Base: Debian slim
   - Use: C compilation only
   - Command: `docker pull ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder-lite:latest`

3. **`ledger-app-dev-tools`** (development image)
   - Base: Full image + Ragger + Speculos
   - Use: Testing and development
   - Command: `docker pull ghcr.io/ledgerhq/ledger-app-builder/ledger-app-dev-tools:latest`

## Testing Integration in CI

### Proposed Testing Workflow

To integrate Ragger tests in CI, we can create an additional workflow:

```yaml
name: Test Ledger Wallet with Ragger

on:
  push:
    branches: [ development, mainnet, nextnet ]
    paths:
      - 'applications/minotari_ledger_wallet/**'
      - 'tests/ledger_wallet/**'
  pull_request:
    branches: [ development, mainnet, nextnet ]
    paths:
      - 'applications/minotari_ledger_wallet/**'
      - 'tests/ledger_wallet/**'

jobs:
  ragger-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        device: [nanosp, flex]
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          pip install ledgered
          pip install 'ragger[speculos]'
          
      - name: Run Ragger tests
        run: |
          cd tests/ledger_wallet
          python -m pytest test_tari_ragger.py --device ${{ matrix.device }} -v
```

### Testing Commands with Docker

To run tests inside the development container:

```bash
# Run development container
docker run --rm -ti \
  -v "$(realpath .):/app" \
  --user $(id -u):$(id -g) \
  -v "/tmp/.X11-unix:/tmp/.X11-unix" \
  -e DISPLAY=$DISPLAY \
  ghcr.io/ledgerhq/ledger-app-builder/ledger-app-dev-tools:latest

# Inside container
python -m virtualenv venv --system-site-package
source ./venv/bin/activate
pip install -r tests/requirements.txt
python -m pytest tests/ledger_wallet/test_tari_ragger.py --device nanosp -v
```

## Proposed CI Improvements

### 1. Update Docker Image Version

The current workflow uses version `4.15.0`. We can update to the latest version:

```yaml
env:
  DOCKER_IMAGE: "ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:latest"
```

### 2. Add Automated Testing

We propose adding a testing job after compilation:

```yaml
  ragger-testing:
    needs: [builds]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        device: [nanosp, flex]
    
    steps:
      - name: Download built artifacts
        uses: actions/download-artifact@v4
        with:
          pattern: "minotari_ledger_wallet-*-${{ matrix.device }}-*"
          
      - name: Run Ragger tests
        run: |
          # Setup environment and run tests
          python -m pytest tests/ledger_wallet/test_tari_ragger.py --device ${{ matrix.device }} -v
```

### 3. Speculos Integration

For automated testing without GUI:

```yaml
- name: Run headless Speculos tests
  run: |
    # Run Speculos in headless mode
    speculos build/nanosplus/bin/app.elf --model nanosplus --display headless &
    # Run Ragger tests
    python -m pytest tests/ledger_wallet/test_tari_ragger.py --device nanosp -v
```

## Environment Configuration

### Required Variables

```bash
# For local compilation (equivalent to CI)
export LEDGER_SDK_PATH=/data/git/tari/ledger-secure-sdk

# For testing with Ragger
export RAGGER_DEVICE=nanosp  # or flex
```

### Manifest Configuration

The `ledger_app.toml` file must be correctly configured:

```toml
[app]
sdk = "rust"
build_directory = "applications/minotari_ledger_wallet/wallet"
devices = ["flex", "nanosp"]
```

## CI Troubleshooting

### Common Issues

1. **Flex compilation fails**
   - Solution: Clean cache before compiling
   ```bash
   cargo clean
   cargo ledger build flex
   ```

2. **Ragger cannot find manifest**
   - Verify `ledger_app.toml` is in root directory
   - Confirm `build_directory` path is correct

3. **Speculos fails to start in CI**
   - Use headless mode: `--display headless`
   - Verify binary is compiled correctly

### Logging and Debugging

Add detailed logging to workflow:

```yaml
- name: Debug build output
  run: |
    ls -la applications/minotari_ledger_wallet/wallet/target/${{ matrix.ledger_target }}/release/
    file applications/minotari_ledger_wallet/wallet/target/${{ matrix.ledger_target }}/release/minotari_ledger_wallet
```

## Additional Resources

- [ledger-app-builder repository](https://github.com/LedgerHQ/ledger-app-builder)
- [Ragger documentation](https://github.com/LedgerHQ/ragger)
- [Speculos documentation](https://github.com/LedgerHQ/speculos)

## Conclusion

The current CI integration is well configured using Ledger's official Docker image. The main proposed improvements are:
1. Add automated testing with Ragger
2. Update to the latest Docker image version
3. Improve troubleshooting and logging

The testing framework is ready to be integrated into the existing CI pipeline.
