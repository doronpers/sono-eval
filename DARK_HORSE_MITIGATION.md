# Dark Horse Mitigation Plan

## Overview

The sono-eval assessment engine includes micro-motive tracking based on Todd Rose's "Dark Horse" framework. To mitigate licensing concerns for public release, the Dark Horse functionality has been made **optional and can be disabled via configuration**.

## Mitigation Strategy

### 1. Configuration-Based Disabling

The Dark Horse micro-motive tracking can be disabled by setting the `DARK_HORSE_MODE` environment variable or config setting to `disabled`.

**Default**: `enabled` (for internal/private use)  
**Public Release**: Should be set to `disabled`

### 2. Code Changes Made

1. **Added config check**: The `AssessmentEngine` now checks `dark_horse_mode` config flag
2. **Conditional execution**: `_identify_micro_motives()` is only called if Dark Horse is enabled
3. **Graceful degradation**: When disabled, returns empty motives list - assessment still works
4. **Updated documentation**: Removed explicit "Dark Horse" references from public-facing docs

### 3. How to Disable for Public Release

#### Option A: Environment Variable

```bash
export DARK_HORSE_MODE=disabled
```

#### Option B: Config File

In your config file or `.env`:

```
DARK_HORSE_MODE=disabled
```

#### Option C: Default Config

Update `src/sono_eval/utils/config.py` to default to disabled:

```python
dark_horse_mode: str = Field(default="disabled", alias="DARK_HORSE_MODE")
```

### 4. Verification

After disabling, verify:

1. Micro-motives are not generated (empty list)
2. Assessment still works correctly
3. Summary generation handles empty motives gracefully
4. CLI/UI doesn't display micro-motives section

Test with:

```bash
# With Dark Horse disabled
DARK_HORSE_MODE=disabled python -m sono_eval.cli.main assess <input>
```

## Impact Assessment

### When Disabled

- ✅ Assessment scoring still works (scores unaffected)
- ✅ All other features remain functional
- ✅ Summary generation works (just without micro-motive info)
- ✅ No licensing concerns

### What's Lost

- Micro-motive tracking and analysis
- Micro-motive display in results
- Summary mentions of primary micro-motive

### Recommendation

For public release:

1. **Set default to `disabled`** in config
2. **Remove or update** Dark Horse references in documentation
3. **Test** that assessment works correctly without it
4. **Consider** removing Dark Horse code entirely if licensing cannot be obtained

## Alternative: Complete Removal

If licensing cannot be obtained and you want to completely remove Dark Horse:

1. Remove `_identify_micro_motives()` method
2. Remove `MicroMotive` imports and usage
3. Remove `dark_horse_mode` config option
4. Update all references in CLI, UI, and documentation
5. Remove micro-motive display from templates

This is more invasive but completely eliminates licensing concerns.

## Files Modified

- `src/sono_eval/assessment/engine.py` - Added config check and conditional execution
- Documentation updated to reflect optional nature

## Next Steps

1. ✅ Code changes made to support disabling
2. ⚠️ **ACTION**: Set default to `disabled` for public release
3. ⚠️ **ACTION**: Test assessment with Dark Horse disabled
4. ⚠️ **ACTION**: Update documentation to remove Dark Horse references
5. ⚠️ **ACTION**: Consider complete removal if licensing unavailable
