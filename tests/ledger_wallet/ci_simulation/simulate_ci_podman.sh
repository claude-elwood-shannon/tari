#!/bin/bash

# CI Simulation Script for Ledger Wallet Testing with Podman
# This script simulates the GitHub Actions workflow locally using Podman

set -e  # Exit on any error

# Configuration
LEDGER_TARGET="${1:-nanosplus}"  # Default to nanosplus (Ledger builder)
SPECULOS_MODEL="${2:-nanosp}"    # Default to nanosp (Speculos)
WORKSPACE_DIR="/data/git/tari"
DIST_DIR="${WORKSPACE_DIR}/tests/ledger_wallet/dist"
TEST_RESULTS_DIR="${WORKSPACE_DIR}/tests/ledger_wallet/test_results"
LOG_DIR="${WORKSPACE_DIR}/tests/ledger_wallet/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Create necessary directories
mkdir -p "${DIST_DIR}" "${TEST_RESULTS_DIR}" "${LOG_DIR}"

# Step 1: Build Ledger Firmware
log "Step 1: Building Ledger firmware for target: ${LEDGER_TARGET}"

podman run --rm \
    -v "${WORKSPACE_DIR}:/app" \
    -w "/app/applications/minotari_ledger_wallet/wallet" \
    ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:latest \
    cargo ledger build "${LEDGER_TARGET}" -- --locked

success "Firmware built successfully for ${LEDGER_TARGET}"

# Step 2: Archive firmware files (simulating CI artifact creation)
log "Step 2: Archiving firmware files"

cd "${DIST_DIR}"
echo "Copying files to $(pwd)"

# Copy built files
cp -vf "${WORKSPACE_DIR}/applications/minotari_ledger_wallet/wallet/target/${LEDGER_TARGET}/release/"*.json .
cp -vf "${WORKSPACE_DIR}/applications/minotari_ledger_wallet/wallet/target/${LEDGER_TARGET}/release/"key*.gif .
cp -vf "${WORKSPACE_DIR}/applications/minotari_ledger_wallet/wallet/target/${LEDGER_TARGET}/release/"minotari_ledger_wallet.* .

# Create checksums
shasum --algorithm 256 * > "minotari_ledger_wallet-${LEDGER_TARGET}-local.sha256"
cat "minotari_ledger_wallet-${LEDGER_TARGET}-local.sha256"

success "Firmware files archived and checksums created"

# Step 3: Start Speculos emulator
log "Step 3: Starting Speculos emulator for ${SPECULOS_MODEL}"

# Stop any existing Speculos containers
podman stop speculos-${SPECULOS_MODEL} 2>/dev/null || true
podman rm speculos-${SPECULOS_MODEL} 2>/dev/null || true

# Start Speculos (headless mode for CI environment)
podman run -d --name "speculos-${SPECULOS_MODEL}" \
    -p 9999:9999 \
    -v "${WORKSPACE_DIR}/applications/minotari_ledger_wallet/wallet/target/${LEDGER_TARGET}/release:/app" \
    ghcr.io/ledgerhq/speculos:latest \
    --model "${SPECULOS_MODEL}" --display headless /app/minotari_ledger_wallet

# Wait for Speculos to start
sleep 5

# Check if Speculos is running
if podman ps | grep -q "speculos-${SPECULOS_MODEL}"; then
    success "Speculos emulator started successfully"
else
    error "Failed to start Speculos emulator"
    exit 1
fi

# Step 4: Run Ragger tests
log "Step 4: Running Ragger tests against Speculos"

cd "${WORKSPACE_DIR}/tests/ledger_wallet"

# Set environment variables for tests (Ragger uses these automatically)
export SPECULOS_MODEL="${SPECULOS_MODEL}"
export APP_FILE="../minotari_ledger_wallet"
export SPECULOS_HOST="localhost"
export SPECULOS_PORT="9999"

# Run tests with detailed output (Ragger handles Speculos configuration automatically)
python -m pytest test_tari_ragger.py -v \
    --device "${SPECULOS_MODEL}" \
    --log-level INFO \
    --junitxml="${TEST_RESULTS_DIR}/test-results-${SPECULOS_MODEL}.xml" \
    2>&1 | tee "${LOG_DIR}/test-execution-${SPECULOS_MODEL}.log"

TEST_EXIT_CODE=${PIPESTATUS[0]}

# Step 5: Cleanup
log "Step 5: Cleaning up"

podman stop "speculos-${SPECULOS_MODEL}" 2>/dev/null || true
podman rm "speculos-${SPECULOS_MODEL}" 2>/dev/null || true

# Step 6: Generate summary
log "Step 6: Generating test summary"

echo "## CI Simulation Test Results" > "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
echo "" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
echo "**Target Device:** ${LEDGER_TARGET}" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
echo "**Speculos Model:** ${SPECULOS_MODEL}" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
echo "**Test Exit Code:** ${TEST_EXIT_CODE}" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
echo "**Execution Time:** $(date)" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
echo "" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"

if [ ${TEST_EXIT_CODE} -eq 0 ]; then
    echo "✅ **Status:** All tests passed successfully" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
    success "CI simulation completed successfully!"
else
    echo "❌ **Status:** Some tests failed" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
    warning "CI simulation completed with test failures"
fi

echo "" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
echo "**Generated Files:**" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
echo "- Test Results: test-results-${SPECULOS_MODEL}.xml" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"
echo "- Execution Log: test-execution-${SPECULOS_MODEL}.log" >> "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"

cat "${TEST_RESULTS_DIR}/summary-${SPECULOS_MODEL}.md"

exit ${TEST_EXIT_CODE}
