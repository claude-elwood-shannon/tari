# Workflow Execution Guide for Ledger Wallet CI

This document explains how to trigger the execution of the Ledger Wallet build workflow in GitHub Actions.

## Current Workflow Triggers

The workflow `.github/workflows/build_ledger_wallet.yml` is configured to run on:

### 1. **Tag Push** (Primary Trigger)
```yaml
push:
  tags:
    - "v[0-9]+.[0-9]+.[0-9]*"
```
- **Action**: Push a version tag (e.g., `v1.0.0`, `v2.3.1`)
- **Result**: Builds firmware and creates a release draft

### 2. **Specific Branch Patterns**
```yaml
push:
  branches:
    - "build-all-*"
    - "build-ledger-*"
```
- **Action**: Push to branches matching these patterns
- **Examples**: `build-all-feature-x`, `build-ledger-test`

### 3. **Scheduled Execution**
```yaml
schedule:
  - cron: "05 00 * * *"
```
- **Action**: Runs daily at 00:05 UTC
- **Purpose**: Regular automated builds

### 4. **Manual Trigger** (workflow_dispatch)
```yaml
workflow_dispatch:
```
- **Action**: Manual execution via GitHub UI or API
- **Flexibility**: Can run on demand

## Methods to Trigger Workflow Execution

### Method 1: Create and Push a Version Tag (Recommended)

**Steps:**
1. **Create a tag:**
   ```bash
   git tag v1.0.0-test
   ```

2. **Push the tag:**
   ```bash
   git push origin-claude v1.0.0-test
   ```

3. **Verify execution:**
   - Check GitHub Actions tab
   - Look for "Build minotari_ledger_wallet" workflow

**Example:**
```bash
# From current branch
git tag v1.0.0-ledger-ci-test
git push origin-claude v1.0.0-ledger-ci-test
```

### Method 2: Create a Build Branch

**Steps:**
1. **Create a branch with build pattern:**
   ```bash
   git checkout -b build-ledger-ci-test
   ```

2. **Make a small change and push:**
   ```bash
   # Add a small change (e.g., update README)
   echo "# CI Test" >> tests/ledger_wallet/README.md
   git add tests/ledger_wallet/README.md
   git commit -m "ci: test workflow trigger"
   git push origin-claude build-ledger-ci-test
   ```

3. **Delete branch after test:**
   ```bash
   git push origin-claude --delete build-ledger-ci-test
   git branch -D build-ledger-ci-test
   ```

### Method 3: Manual Trigger via GitHub UI

**Steps:**
1. Navigate to GitHub repository
2. Go to "Actions" tab
3. Select "Build minotari_ledger_wallet" workflow
4. Click "Run workflow" button
5. Choose branch and click "Run workflow"

### Method 4: Manual Trigger via GitHub API

**Using curl:**
```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/claude-elwood-shannon/tari/actions/workflows/build_ledger_wallet.yml/dispatches \
  -d '{"ref":"feature/ledger-test-env-c0e6928-flex-ci"}'
```

## Quick Test Execution

### Option A: Tag-Based Test (Fastest)

```bash
# From current CI branch
git tag v1.0.0-ci-test-$(date +%s)
git push origin-claude v1.0.0-ci-test-$(date +%s)

# Clean up after test
git tag -d v1.0.0-ci-test-$(date +%s)
git push origin-claude --delete v1.0.0-ci-test-$(date +%s)
```

### Option B: Branch-Based Test

```bash
# Create temporary build branch
git checkout -b build-ledger-ci-$(date +%s)

# Make minimal change
touch .ci-test-trigger
git add .ci-test-trigger
git commit -m "ci: trigger workflow test"
git push origin-claude HEAD

# Clean up
git checkout feature/ledger-test-env-c0e6928-flex-ci
git branch -D build-ledger-ci-$(date +%s)
git push origin-claude --delete build-ledger-ci-$(date +%s)
```

## Expected Workflow Behavior

### When Triggered by Tag:
1. **Builds firmware** for all supported devices (nanosplus, flex, nanox, stax)
2. **Creates artifacts** with proper naming and checksums
3. **Generates release draft** (if tag starts with "v")

### When Triggered by Branch:
1. **Builds firmware** for all supported devices
2. **Creates artifacts** but does not create release
3. **Artifacts available** for download from Actions tab

### When Triggered Manually:
1. **Same as branch trigger** but on-demand
2. **Can specify branch** to build from

## Verification Steps

After triggering the workflow:

1. **Check GitHub Actions tab** for running workflow
2. **Monitor job progress** for each device (nanosplus, flex, etc.)
3. **Verify artifacts** are created successfully
4. **Check logs** for any compilation errors
5. **Download artifacts** to verify binary integrity

## Troubleshooting

### Workflow Not Triggering
- **Check branch/tag patterns** match exactly
- **Verify push permissions** to repository
- **Check workflow file** is in correct location (.github/workflows/)

### Build Failures
- **Review logs** for specific error messages
- **Check Docker image** availability (ghcr.io/ledgerhq/ledger-app-builder)
- **Verify Rust toolchain** compatibility

### Artifact Issues
- **Check artifact names** follow expected pattern
- **Verify checksums** are generated correctly
- **Test artifact download** and extraction

## Best Practices

1. **Use descriptive tags** for test executions
2. **Clean up test tags/branches** after verification
3. **Monitor resource usage** during builds
4. **Keep workflow configuration** up to date with Ledger SDK changes
5. **Test regularly** to ensure CI pipeline health

## Conclusion

The workflow can be triggered using multiple methods, with tag-based triggers being the most comprehensive (including release creation). For testing purposes, branch-based triggers or manual execution provide quick feedback without creating permanent releases.
