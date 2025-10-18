# Organized Structure of tests/ledger_wallet

## 📁 Directory Organization

### **scripts/**
- Automation scripts and utilities
- Local CI simulation
- Environment configuration

### **config/**
- Configuration files
- Environment variables
- Device-specific configurations

### **docs/**
- Technical documentation
- Usage guides
- Strategic analyses

### **test_results/**
- Test execution results
- Logs and reports
- Generated artifacts

### **ci_simulation/**
- Configuration for local CI simulation
- Specific scripts for Act+Podman
- Local testing environments

## 📄 Main Files

### **Tests**
- `test_tari_ragger.py` - Main tests with Ragger
- `test_tari_ledger_wallet.py` - Integration tests
- `conftest.py` - Pytest configuration

### **Documentation**
- `README.md` - Main documentation
- `RAGGER_USAGE.md` - Ragger usage guide
- `CI_INTEGRATION.md` - CI integration
- `WORKFLOW_EXECUTION.md` - Workflow execution
- `ledger-workflow-strategic-analysis.md` - Strategic analysis

### **Configuration and Utilities**
- `speculos_experiments.py` - Speculos experiments
- `TASK_PROGRESS.md` - Task tracking
- `CLEANUP_TEST_TAGS.md` - Tag cleanup (temporary)

## 🚀 Recommended Workflow

### **Local Development**
1. Use scripts in `scripts/` for configuration
2. Run tests from directory root
3. Save results in `test_results/`

### **CI Simulation**
1. Configure environment with `ci_simulation/`
2. Use Act+Podman to simulate GitHub Actions
3. Validate workflow before pushing to real CI

### **Documentation**
1. Keep documentation updated in `docs/`
2. Update `STRUCTURE.md` when adding new elements
3. Follow naming conventions

## 🔧 Conventions

### **File Naming**
- Scripts: `script_name.sh` or `script_name.py`
- Configuration: `config_name.yaml` or `name.config`
- Documentation: `TOPIC_DESCRIPTION.md`

### **Code Organization**
- Tests separated by functionality
- Modular configuration per device
- Reusable and documented scripts

---

*Last updated: October 18, 2025*
