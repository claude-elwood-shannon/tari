# QR Code Testing Plan for Ledger Flex

## Problem Identified
**Root cause**: Ledger wallets generate interactive addresses with different features (`INTERACTIVE_ONLY`) vs normal wallets (`INTERACTIVE | ONE_SIDED`). The current QR code uses `address_interactive` which is incorrect for Ledger wallets.

**Proposed solution**: Change `address_interactive` to `address_one_sided` in `app_state.rs`.

## Action Plan for Tomorrow

### Phase 1: QR Code Generation for Testing (15-30 min)
1. **Create QR code generation script**
   - Script that generates QR codes using both addresses
   - Format: `tari://{network}/transactions/send?tariAddress={address}`
   - Generate both with `address_interactive` and `address_one_sided`

2. **Implement temporary script in wallet console**
   - Temporarily modify `app_state.rs` to print QR codes to console
   - Allow quick testing without TUI interface

### Phase 2: Testing with Android App (30-45 min)
1. **Test generated QR codes**
   - Scan QR code with `address_interactive` (should fail)
   - Scan QR code with `address_one_sided` (should work)
   - Verify connectivity with Ledger Flex

2. **Validate behavior**
   - Confirm problem reproduces with `address_interactive`
   - Confirm solution works with `address_one_sided`

### Phase 3: Correction Implementation (15 min)
1. **Apply permanent correction**
   - Change `address_interactive` to `address_one_sided` in `app_state.rs`
   - Commit and push to branch

2. **Verify build**
   - Compile wallet console with correction
   - Verify no regressions

### Phase 4: Final Testing (15 min)
1. **Test implemented correction**
   - Generate QR code with corrected wallet console
   - Scan with Android app
   - Verify successful connectivity

## Scripts to Create

### Script 1: QR Code Generator
```bash
# qr_test_generator.sh
#!/bin/bash
# Generates QR codes for testing

# Get addresses from Ledger wallet
INTERACTIVE_ADDR="..."  # Get from Ledger wallet
ONE_SIDED_ADDR="..."    # Get from Ledger wallet
NETWORK="mainnet"       # or "testnet" based on configuration

# Generate URLs
QR_INTERACTIVE="tari://$NETWORK/transactions/send?tariAddress=$INTERACTIVE_ADDR"
QR_ONE_SIDED="tari://$NETWORK/transactions/send?tariAddress=$ONE_SIDED_ADDR"

# Print for testing
echo "QR Code with address_interactive:"
echo "$QR_INTERACTIVE"
echo ""
echo "QR Code with address_one_sided:"
echo "$QR_ONE_SIDED"
```

### Script 2: Temporary Wallet Console Modification
```rust
// In app_state.rs - temporary modification for testing
fn print_qr_codes_for_testing(wallet_identity: &WalletIdentity) {
    let qr_interactive = format!(
        "tari://{}/transactions/send?tariAddress={}",
        wallet_identity.network(),
        wallet_identity.address_interactive.to_base58()
    );
    
    let qr_one_sided = format!(
        "tari://{}/transactions/send?tariAddress={}",
        wallet_identity.network(),
        wallet_identity.address_one_sided.to_base58()
    );
    
    println!("=== QR CODES FOR TESTING ===");
    println!("INTERACTIVE (current - should fail):");
    println!("{}", qr_interactive);
    println!("");
    println!("ONE-SIDED (proposed - should work):");
    println!("{}", qr_one_sided);
    println!("=============================");
}
```

## Commands to Execute Tomorrow

### 1. Prepare environment
```bash
cd /data/git/tari
git status  # Verify current branch
```

### 2. Generate QR codes for testing
```bash
# Execute generation script or temporarily modify wallet console
cargo build --bin minotari_console_wallet
./target/debug/minotari_console_wallet --print-qr-test
```

### 3. Test with Android app
- Scan generated QR code
- Verify connectivity with Ledger Flex
- Document results

### 4. Implement correction
```bash
# Apply permanent change in app_state.rs
git add applications/minotari_console_wallet/src/ui/state/app_state.rs
git commit -m "fix: use address_one_sided for QR code generation in Ledger wallets"
git push origin-claude fix-qr-code-ledger-flex
```

## Expected Results

- **Current behavior**: QR code with `address_interactive` should fail to connect
- **Corrected behavior**: QR code with `address_one_sided` should connect successfully
- **No regressions**: Normal wallets should continue to work correctly

## Files to Modify

- `applications/minotari_console_wallet/src/ui/state/app_state.rs` - Line 400
- Change `wallet_identity.address_interactive.to_base58()` to `wallet_identity.address_one_sided.to_base58()`
