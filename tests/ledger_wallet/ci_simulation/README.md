# CI Simulation with Podman

This directory contains scripts and configuration for simulating GitHub Actions CI workflows locally using Podman.

## Overview

The CI simulation system allows you to test the complete Ledger wallet testing workflow locally before pushing to GitHub Actions. This includes:

- Building Ledger firmware with the official builder image
- Running Speculos emulator for device simulation
- Executing Ragger tests against the emulated device
- Generating test reports and summaries

## Prerequisites

- **Podman**: Container runtime (alternative to Docker)
- **Python 3.11+**: For running Ragger tests
- **Required Python packages**: See `requirements.txt` in parent directory

## Quick Start

### Basic Usage

Run the simulation for a specific Ledger device:

```bash
# Run for nanosplus (default)
./simulate_ci_podman.sh

# Run for specific device
./simulate_ci_podman.sh nanosplus nanosplus
./simulate_ci_podman.sh nanox nanox
./simulate_ci_podman.sh stax stax
./simulate_ci_podman.sh flex flex
```

### Advanced Usage

```bash
# Run with custom paths
LEDGER_TARGET=nanosplus SPECULOS_MODEL=nanosplus ./simulate_ci_podman.sh

# Run with verbose output
bash -x ./simulate_ci_podman.sh nanosplus nanosplus
```

## Script Details

### `simulate_ci_podman.sh`

Main simulation script that replicates the GitHub Actions workflow:

**Parameters:**
- `$1`: Ledger target device (default: `nanosplus`)
- `$2`: Speculos model (default: `nanosplus`)

**Supported Devices:**
- `nanosplus` - Nano S Plus
- `nanox` - Nano X
- `stax` - Stax
- `flex` - Flex

**Workflow Steps:**
1. **Build Firmware**: Uses official Ledger app builder container
2. **Archive Artifacts**: Creates distribution files and checksums
3. **Start Speculos**: Launches device emulator
4. **Run Tests**: Executes Ragger tests against emulator
5. **Generate Reports**: Creates JUnit XML and HTML reports
6. **Cleanup**: Stops containers and generates summary

## Generated Output

The script creates the following files:

### Test Results
- `test_results/test-results-{model}.xml` - JUnit XML format
- `test_results/test-report-{model}.html` - HTML report
- `test_results/summary-{model}.md` - Markdown summary

### Logs
- `logs/test-execution-{model}.log` - Complete test execution log

### Distribution Files
- `dist/minotari_ledger_wallet-{target}-local.sha256` - Checksums

## Integration with GitHub Actions

This simulation closely matches the `build_ledger_wallet_testing.yml` workflow. The main differences are:

- **Local execution**: Uses Podman instead of GitHub Actions runner
- **Manual triggering**: No automatic triggers or schedules
- **Artifact handling**: Local file system instead of GitHub artifacts

## Alternative: Using Act

If you prefer to use GitHub's official Act tool, see [ACT_INSTALLATION.md](./ACT_INSTALLATION.md) for installation and usage instructions.

## Troubleshooting

### Common Issues

1. **Podman not running:**
   ```bash
   systemctl --user start podman.socket
   ```

2. **Missing container images:**
   ```bash
   podman pull ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:latest
   podman pull ghcr.io/ledgerhq/speculos:latest
   ```

3. **Python dependencies missing:**
   ```bash
   pip install -r ../requirements.txt
   pip install speculos
   ```

### Debug Mode

Run with debug output:
```bash
bash -x ./simulate_ci_podman.sh nanosplus nanosplus
```

## Best Practices

1. **Test locally first**: Always run simulation before pushing to CI
2. **Check logs**: Review generated logs for detailed information
3. **Validate reports**: Check HTML and XML reports for test results
4. **Clean between runs**: Script automatically cleans up containers

## Related Files

- `ACT_INSTALLATION.md` - Act tool installation guide
- `../STRUCTURE.md` - Overall project structure
- `../RAGGER_USAGE.md` - Ragger testing guide
