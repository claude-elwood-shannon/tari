# Ragger Testing Framework Usage Guide

This document explains how Ragger is used in the Tari Ledger Wallet testing framework.

## Overview

Ragger is Ledger's official testing framework that simplifies testing of Ledger applications by providing automatic Speculos management, APDU communication, and comprehensive logging.

## 1. Base Configuration (conftest.py)

```python
# tests/ledger_wallet/conftest.py
from ragger.conftest import configuration
pytest_plugins = ("ragger.conftest.base_conftest",)
```

**Purpose**: Imports Ragger's base configuration and defines fixtures that pytest will use automatically.

## 2. Automatic Ragger Fixtures

Ragger provides automatic fixtures injected into tests:

- **`backend`**: Configured Speculos backend
- **`firmware`**: Device firmware information  
- **`navigator`**: Ledger interface navigation

## 3. Backend Usage in Tests

```python
def test_get_app_name(backend):
    # Ragger automatically starts Speculos with the application
    response = backend.exchange(
        cla=WALLET_CLA,        # 0x80
        ins=GET_APP_NAME,      # 0x02
        p1=0x00,
        p2=0x00,
        data=b""
    )
```

**Backend Features:**
- ✅ **Automatic initialization**: Speculos starts automatically
- ✅ **Session management**: Persistent session during test
- ✅ **Integrated logging**: Automatic APDU logging
- ✅ **Error handling**: Automatic exception management

## 4. APDU Communication with Ragger

**Command Structure:**
```python
response = backend.exchange(
    cla=0x80,      # Class - Tari specific
    ins=0x02,      # Instruction - GetAppName
    p1=0x00,       # Parameter 1
    p2=0x00,       # Parameter 2
    data=b""       # Additional data (empty for simple commands)
)
```

**RAPDU Response:**
```python
# response is a RAPDU object with:
response.data      # Response data (bytes)
response.status    # Status code (0x9000 = success)
```

## 5. Device Configuration

**Specified when running:**
```bash
python3 -m pytest tests/ledger_wallet/test_tari_ragger.py --device flex
```

**Ragger automatically detects:**
- ✅ **API Level**: 24 (from application metadata)
- ✅ **Ports**: 5000 (API), 5001 (APDU)
- ✅ **SDK**: nbgl (for Ledger Flex)
- ✅ **Options**: `--model flex --api-port 5000 --apdu-port 5001`

## 6. Automatic Ragger Logging

Ragger generates automatic logs:
```
[INFO] ragger.apdu_logger - => 8002000000     # Command sent
[INFO] ragger.apdu_logger - <= 6d696e6f...9000 # Response received
```

## 7. Advantages Over Manual Approach

**With Ragger:**
```python
# Simple and automatic
response = backend.exchange(cla=0x80, ins=0x02, ...)
```

**Without Ragger (manual approach):**
```python
# Complex and manual
apdu = struct.pack('>BBBBBH', 0x80, 0x02, 0x00, 0x00, 0x00, 0x00)
# + connection management, parsing, error handling, etc.
```

## 8. Pytest Integration

**Specific Markers:**
```python
@pytest.mark.use_on_backend("speculos")
def test_speculos_only(backend):
    # Only runs with Speculos backend
```

## 9. Test Structure

**Complete Test Example:**
```python
def test_get_app_name(backend):
    """Test GetAppName command using Ragger backend"""
    
    # Send command using Ragger's exchange method
    response = backend.exchange(
        cla=WALLET_CLA,
        ins=GET_APP_NAME,
        p1=0x00,
        p2=0x00,
        data=b""
    )
    
    # Verify response
    assert len(response.data) > 0, "Empty response"
    assert response.status == 0x9000, f"Unexpected status: {hex(response.status)}"
    
    # Decode and log response
    app_name = response.data.decode('ascii', errors='ignore')
    print(f"App name: {app_name}")
```

## 10. Key Benefits of Ragger

1. **Automation**: Automatic Speculos management
2. **Fixtures**: Automatic configuration injection
3. **Logging**: Integrated APDU logging
4. **Error Handling**: Managed exceptions
5. **Portability**: Easy device switching
6. **Standard**: Official Ledger testing framework

## 11. Running Tests

**Basic test execution:**
```bash
python3 -m pytest tests/ledger_wallet/test_tari_ragger.py --device flex -v
```

**With detailed output:**
```bash
python3 -m pytest tests/ledger_wallet/test_tari_ragger.py --device flex -v -s
```

**Specific test:**
```bash
python3 -m pytest tests/ledger_wallet/test_tari_ragger.py::test_get_app_name --device flex
```

## 12. Troubleshooting

**Common Issues:**
- **Application not found**: Ensure the app is compiled to `applications/minotari_ledger_wallet/wallet/target/flex/release/minotari_ledger_wallet`
- **Port conflicts**: Change ports in `ledger_app.toml` if 5000/5001 are in use
- **API Level mismatch**: Ensure SDK 1.27.2+ with API_LEVEL=24

**Debug Mode:**
```bash
python3 -m pytest tests/ledger_wallet/test_tari_ragger.py --device flex -v -s --log-level=DEBUG
```

This documentation provides a comprehensive guide to using Ragger for testing the Tari Ledger Wallet application.
