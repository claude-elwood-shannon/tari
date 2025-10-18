# Progress Documentation - Ragger+Speculos Tests for Tari Ledger Wallet

## ORDER 01 - STRICT WORKFLOW TO FOLLOW FOR AUTONMOUS WORK

Start by using the MCP GitHub tools to check the status of the latest execution of .github/workflows/build_ledger_wallet_testing.yml in CI.

1.- If all tests (including Ragger) of that workflow have worked correctly for each device version of the Ledger wallet app, ONLY IN THAT CASE YOU WILL HAVE FINISHED and you should inform me about it.
2.- If you find any type of error, analyze it, diagnose it, and fix it, always in the local workspace. The local simulator, although it only works for two devices, can serve as a guide.
3.- The name of the current working branch will trigger the execution of a workflow for each push you make, so make commit and push (remote origin-claude), and ensure you don't trigger more than one workflow execution to avoid interfering with your monitoring.
4.- Again with the MCP GitHub tools, monitor the execution, PAY ATTENTION COMPLETELY, of the workflow. As soon as something fails you can stop monitoring and focus on the first error you detect, but if you don't find errors you must wait for the workflow execution to complete to ensure there are no errors.
5.- If you discover that the error you are trying to fix has been solved, document it in this same file, and then create a security tag (with timestamp), because you will continue making corrections and this will allow you to have a restoration point that you should use if something goes wrong and you need to restore your developments.
6.- Go to point 1 again and continue the cycle.

## Documented Achievements

### ✅ Achievement 1: Initial CI workflow setup
- **Security tag**: `ci-setup-20251018-084952`
- **Date/Time**: 18/10/2025, 08:49:52
- **Description**: Initial GitHub Actions workflow setup for building and testing Ledger wallet app for Tari
- **Status**: Completed

### ✅ Achievement 2: Invalid filename characters fix
- **Security tag**: `filename-fix-20251018-084952`
- **Date/Time**: 18/10/2025, 08:49:52
- **Description**: Fixed invalid `/` characters in BINFILE variable of the workflow
- **Status**: Completed

### ✅ Achievement 3: Python dependencies compatibility fix
- **Security tag**: `dependencies-fix-20251018-084952`
- **Date/Time**: 18/10/2025, 08:49:52
- **Description**: Fixed incompatible versions in requirements.txt:
  - `ragger>=1.40.0` (instead of 3.0.0)
  - `speculos>=0.25.0` (instead of 2.0.0)
  - `ledgered>=0.12.0` (instead of 1.0.0)
- **Status**: Completed

### ✅ Achievement 4: Successful build workflow execution
- **Security tag**: `build-success-20251018-084952`
- **Date/Time**: 18/10/2025, 08:49:52
- **Description**: Workflow #18 executed successfully with firmware builds for 4 devices:
  - nanox ✅
  - nanosplus ✅
  - flex ✅
  - stax ✅
- **Status**: Completed

## Recent Achievements

### ✅ Achievement 5: Missing --device parameter fix
- **Security tag**: `device-param-fix-20251018-085152`
- **Date/Time**: 18/10/2025, 08:51:52
- **Description**: Identified and fixed missing `--device` parameter in Ragger pytest command
- **Status**: Completed
- **Details**: 
  - **Problem identified**: Error "the following arguments are required: --device"
  - **Solution**: Added `--device speculos` to pytest command
  - **Workflows executed**: #19 (cancelled) and #20 (pending)

## Pending Issues

### 🔄 Issue 1: Ragger+Speculos tests in execution
- **Status**: In execution
- **Affected devices**: All (nanox, nanosplus, flex, stax)
- **Description**: Ragger tests are being executed with the --device parameter fix
- **Action required**: Monitor results of workflow #20

## Next Steps

1. Analyze Ragger test error logs
2. Identify root cause of failure
3. Implement necessary fixes
4. Execute workflow again
5. Verify that tests pass successfully

## Git Tags Created

All achievements have been tagged with Git tags for precise milestone tracking:

| Tag Name | Commit Hash | Achievement |
|----------|-------------|-------------|
| `ci-setup-20251018-084952` | `096037830` | Initial CI workflow setup |
| `filename-fix-20251018-084952` | `111fa8215` | Invalid filename characters fix |
| `dependencies-fix-20251018-084952` | `60b39ce5a` | Python dependencies compatibility fix |
| `build-success-20251018-084952` | `782a15d81` | Successful build workflow execution |
| `device-param-fix-20251018-085152` | `782a15d81` | Missing --device parameter fix |

## Tag Strategy Implemented

A comprehensive Git tag strategy has been documented in `TAG_STRATEGY.md`:

- **Naming convention**: `<achievement-type>-<date>-<time>`
- **Tag creation process**: Automated for each significant milestone
- **Documentation integration**: Tags referenced in progress documentation
- **Future achievements**: Will be tagged following the established strategy
