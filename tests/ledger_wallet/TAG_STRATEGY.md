# Git Tag Strategy for Milestone Tracking

## Overview

This document outlines the strategy for using Git tags to mark significant achievements and milestones in the Tari Ledger Wallet testing framework development.

## Tag Naming Convention

### Format
```
<achievement-type>-<date>-<time>
```

### Components
- **achievement-type**: Descriptive name of the achievement (kebab-case)
- **date**: YYYYMMDD format (e.g., 20251018)
- **time**: HHMMSS format (e.g., 084952)

### Examples
- `ci-setup-20251018-084952` - Initial CI workflow setup
- `filename-fix-20251018-084952` - Invalid filename characters fix
- `dependencies-fix-20251018-084952` - Python dependencies compatibility fix
- `build-success-20251018-084952` - Successful build workflow execution
- `device-param-fix-20251018-085152` - Missing --device parameter fix

## When to Create Tags

### ✅ Achievement Categories

1. **Setup Milestones**
   - Initial project setup
   - CI/CD pipeline configuration
   - Environment configuration

2. **Bug Fixes**
   - Critical bug resolutions
   - Compatibility fixes
   - Workflow errors resolved

3. **Feature Implementations**
   - New testing capabilities
   - Integration with external tools
   - Performance improvements

4. **Success Milestones**
   - Successful workflow executions
   - Test suite completions
   - Deployment successes

### 🔄 Ongoing Work
- Do not create tags for work in progress
- Only tag completed, verified achievements
- Tags should represent stable, working states

## Tag Creation Process

### Step 1: Identify Achievement
- Achievement must be completed and verified
- Should represent a significant milestone
- Must be documented in `PROGRESS_DOCUMENTATION.md`

### Step 2: Generate Tag Name
```bash
# Use current date and time
DATE=$(date +%Y%m%d)
TIME=$(date +%H%M%S)
TAG_NAME="achievement-type-${DATE}-${TIME}"
```

### Step 3: Create Tag
```bash
# Create tag pointing to specific commit
git tag ${TAG_NAME} <commit-hash>

# Verify tag creation
git tag -l | grep ${TAG_NAME}
```

### Step 4: Push Tags (Optional)
```bash
# Push specific tag
git push origin-claude ${TAG_NAME}

# Push all tags
git push origin-claude --tags
```

## Current Tags Created

| Tag Name | Commit Hash | Achievement Description |
|----------|-------------|-------------------------|
| `ci-setup-20251018-084952` | `096037830` | Initial CI workflow setup |
| `filename-fix-20251018-084952` | `111fa8215` | Invalid filename characters fix |
| `dependencies-fix-20251018-084952` | `60b39ce5a` | Python dependencies compatibility fix |
| `build-success-20251018-084952` | `782a15d81` | Successful build workflow execution |
| `device-param-fix-20251018-085152` | `782a15d81` | Missing --device parameter fix |

## Tag Verification

### Check Existing Tags
```bash
# List all tags
git tag -l

# Filter by achievement type
git tag -l | grep "fix\|setup\|success"
```

### Tag Details
```bash
# Show tag details
git show ${TAG_NAME}

# Compare tags
git log --oneline ${TAG1}..${TAG2}
```

## Integration with Documentation

### Update Progress Documentation
After creating a tag, update `PROGRESS_DOCUMENTATION.md`:

```markdown
### ✅ Achievement: [Description]
- **Security tag**: `[tag-name]`
- **Date/Time**: [date/time]
- **Description**: [detailed description]
- **Status**: Completed
```

### Tag References
- Use tags in commit messages when referencing achievements
- Include tag names in documentation for traceability
- Reference tags in issue tracking systems

## Best Practices

### Tag Management
- **Keep tags lightweight**: Tags should reference existing commits
- **Descriptive names**: Use clear, meaningful tag names
- **Consistent format**: Follow the established naming convention
- **Documentation**: Always update documentation with tag references

### Tag Usage
- **Version control**: Tags provide precise points in development history
- **Rollback points**: Tags mark stable states for potential rollbacks
- **Progress tracking**: Visual representation of development milestones
- **Team coordination**: Shared understanding of project progress

## Future Considerations

### Automated Tagging
Consider implementing automated tagging for:
- Successful CI/CD pipeline runs
- Passing test suites
- Release candidates

### Tag Cleanup
Periodic cleanup of temporary or obsolete tags:
```bash
# Delete local tag
git tag -d ${TAG_NAME}

# Delete remote tag
git push origin-claude --delete ${TAG_NAME}
```

## Conclusion

This tag strategy provides a systematic approach to tracking project milestones, ensuring that significant achievements are properly marked and documented for future reference and team coordination.
