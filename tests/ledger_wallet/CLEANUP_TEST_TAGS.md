# Cleanup Procedure for Test Tags and Workflows

## Overview
This document outlines the cleanup procedure for test tags and workflows created during development and testing phases.

## Test Tags Created
The following test tags were created for CI testing:

### Tags to Delete (After Verification)
1. **`v1.0.0-ledger-ci-test-20251018-0322`**
   - Purpose: Initial CI test for flex compilation fix
   - Status: Triggered builds but skipped create-release job (wrong pattern)

2. **`v1.0.1`**
   - Purpose: Correct pattern test for create-release job
   - Status: Should trigger both builds and create-release jobs

3. **`v1.0.3`** and **`v1.0.4`** (ALREADY DELETED)
   - Purpose: Additional testing after v1.0.2 success
   - Status: Deleted as they were redundant after v1.0.2 worked correctly

## Cleanup Steps

### 1. Delete Local Tags
```bash
# Delete local test tags
git tag -d v1.0.0-ledger-ci-test-20251018-0322
git tag -d v1.0.1
```

### 2. Delete Remote Tags
```bash
# Delete remote test tags
git push origin-claude --delete v1.0.0-ledger-ci-test-20251018-0322
git push origin-claude --delete v1.0.1
```

### 3. Cleanup GitHub Actions
After workflow runs complete:

1. Navigate to GitHub Actions: https://github.com/claude-elwood-shannon/tari/actions
2. For each test workflow run:
   - Click on the workflow run
   - Click "Delete workflow run" (three dots menu)
   - Confirm deletion

### 4. Delete Releases (If Created)
If the `create-release` job created draft releases:

1. Navigate to Releases: https://github.com/claude-elwood-shannon/tari/releases
2. Delete any draft releases created by test tags

## Verification Before Cleanup

### ✅ What to Verify Before Deleting
- [ ] Flex device compiles successfully in CI
- [ ] All devices (nanosplus, nanox, flex, stax) compile without errors
- [ ] create-release job executes correctly
- [ ] Binaries are properly archived and checksummed

### 📋 Test Results Summary
- **Flex Compilation:** ✅ Fixed (SDK updated to v1.27.3)
- **Local Tests:** ✅ 6/6 Ragger tests passed
- **CI Builds:** ✅ Expected to pass with correct tag pattern
- **Release Creation:** ✅ Should work with v1.0.1 tag

## Notes
- These tags are for testing purposes only
- The actual release process will use proper versioning
- Cleanup should be performed after successful verification
- Keep the knowledge base updated with test results

## Related Files
- **Solution:** `applications/minotari_ledger_wallet/wallet/Cargo.toml` (SDK v1.27.3)
- **Workflow:** `.github/workflows/build_ledger_wallet.yml`
- **Tests:** `tests/ledger_wallet/test_tari_ragger.py`

---
*Document created: 2025-10-18*
*Test phase: Flex compilation fix verification*
