# Public Release Checklist for sono-eval

## Dark Horse Mitigation

### Required Actions Before Public Release

1. **Disable Dark Horse by Default**
   - [ ] Update `src/sono_eval/utils/config.py`:

     ```python
     dark_horse_mode: str = Field(default="disabled", alias="DARK_HORSE_MODE")
     ```

   - [ ] Or ensure `.env.example` has `DARK_HORSE_MODE=disabled`

2. **Test with Dark Horse Disabled**

   ```bash
   DARK_HORSE_MODE=disabled python -m sono_eval.cli.main assess <test_input>
   ```

   - [ ] Verify assessment works correctly
   - [ ] Verify no micro-motives are generated
   - [ ] Verify summary generation works without micro-motives

3. **Update Documentation**
   - [ ] Remove explicit "Dark Horse" references from public docs
   - [ ] Update README to mention micro-motive tracking is optional
   - [ ] Update any examples/tutorials

4. **Review Code Comments**
   - [ ] Check for any remaining "Dark Horse" references in code comments
   - [ ] Update docstrings to reflect optional nature

## Alternative: Complete Removal

If you prefer to completely remove Dark Horse code:

1. **Remove Code**
   - [ ] Delete `_identify_micro_motives()` method
   - [ ] Remove `MicroMotive` imports
   - [ ] Remove `dark_horse_mode` config option
   - [ ] Remove micro-motive references from CLI/UI

2. **Update Templates**
   - [ ] Remove micro-motive display from HTML templates
   - [ ] Update result formatting

3. **Test**
   - [ ] Full test suite passes
   - [ ] Assessment works correctly

## Quick Disable Command

For immediate testing:

```bash
export DARK_HORSE_MODE=disabled
```

Or add to your `.env` file:

```
DARK_HORSE_MODE=disabled
```

## Verification

After disabling, run:

```bash
# Should show no micro-motives
DARK_HORSE_MODE=disabled python -m sono_eval.cli.main assess <input> --verbose
```

Expected: Assessment completes successfully, but no "Micro-Motives" section appears.
