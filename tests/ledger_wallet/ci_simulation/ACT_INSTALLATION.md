# Act Installation Guide

Act is GitHub's official tool for running GitHub Actions locally. Here are the installation methods:

## Method 1: Using Package Managers (Recommended)

### macOS with Homebrew
```bash
brew install act
```

### Linux with Package Managers

#### Ubuntu/Debian
```bash
# Download and install the latest release
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

#### Arch Linux
```bash
yay -S act  # or use your preferred AUR helper
```

#### Fedora/RHEL
```bash
sudo dnf install act
```

### Windows with Chocolatey
```bash
choco install act
```

## Method 2: Manual Installation

### Download Binary
```bash
# Check latest version at: https://github.com/nektos/act/releases
VERSION=0.2.61  # Replace with latest version
wget https://github.com/nektos/act/releases/download/v${VERSION}/act_Linux_x86_64.tar.gz
tar -xzf act_Linux_x86_64.tar.gz
sudo mv act /usr/local/bin/
```

### Using Go (if you have Go installed)
```bash
go install github.com/nektos/act@latest
```

## Method 3: Using Docker (Alternative)

If you prefer not to install Act directly, you can use it via Docker:

```bash
# Run Act in a container
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/workspace -w /workspace nektos/act:latest
```

## Configuration for Podman

Since you have Podman, you'll need to configure Act to use it:

### Option A: Environment Variables
```bash
export ACT_EXPERIMENTAL=1
export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
```

### Option B: Command Line Flag
```bash
act --container-daemon-socket unix:///run/user/$(id -u)/podman/podman.sock
```

## Verification

After installation, verify Act is working:

```bash
act --version
act --list
```

## Usage with Our Workflow

Once installed, you can test our workflow:

```bash
# Test the builds job
act -W .github/workflows/build_ledger_wallet_testing.yml -j builds

# Test specific device
act -W .github/workflows/build_ledger_wallet_testing.yml -j builds --matrix ledger_target=nanosplus

# Test the complete workflow
act -W .github/workflows/build_ledger_wallet_testing.yml
```

## Troubleshooting

### Common Issues

1. **Permission errors with Podman:**
   ```bash
   # Ensure Podman socket is accessible
   ls -la /run/user/$(id -u)/podman/podman.sock
   ```

2. **Missing Docker images:**
   ```bash
   # Pull required images manually
   podman pull ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:latest
   podman pull ghcr.io/ledgerhq/speculos:latest
   ```

3. **Act not finding workflows:**
   ```bash
   # Run from project root directory
   cd /data/git/tari
   act --list
   ```

## Alternative: Use Our Podman Script

If Act installation is problematic, you can use our custom Podman script instead:

```bash
./tests/ledger_wallet/ci_simulation/simulate_ci_podman.sh
```

This provides similar functionality without requiring Act installation.
