# Fixed: "Not Found" Error

## Problem
When accessing the mobile interface at `/mobile/`, you were getting `{"detail":"Not Found"}` errors.

## Root Cause
1. **Static file paths**: Templates were using absolute paths `/static/...` which don't work when the app is mounted at `/mobile`
2. **API route paths**: Routes were defined as `/api/mobile/...` which became `/mobile/api/mobile/...` (redundant and incorrect)

## Fixes Applied

### 1. Static File Paths (base.html)
**Before:**
```html
<link rel="stylesheet" href="/static/style.css">
<script src="/static/script.js"></script>
```

**After:**
```html
<link rel="stylesheet" href="{{ request.base_url }}static/style.css">
<script src="{{ request.base_url }}static/script.js"></script>
```

This uses the request's base URL to correctly resolve static files when mounted.

### 2. API Route Definitions (app.py)
**Before:**
```python
@app.post("/api/mobile/assess")
@app.get("/api/mobile/explain/{path}")
```

**After:**
```python
@app.post("/api/assess")
@app.get("/api/explain/{path}")
```

Since the mobile app is mounted at `/mobile`, these routes are now accessible at:
- `/mobile/api/assess`
- `/mobile/api/explain/{path}`

### 3. JavaScript API Calls (templates)
**Before:**
```javascript
fetch('/api/mobile/explain/${pathId}')
fetch('/api/mobile/assess', {...})
```

**After:**
```javascript
fetch(`/mobile/api/explain/${pathId}`)
fetch('/mobile/api/assess', {...})
```

## Testing

After these fixes, the following should work:

1. **Home page**: http://localhost:8000/mobile/
2. **Static files**: http://localhost:8000/mobile/static/style.css
3. **API endpoints**: 
   - POST http://localhost:8000/mobile/api/assess
   - GET http://localhost:8000/mobile/api/explain/{path}

## Files Changed

1. `src/sono_eval/mobile/templates/base.html` - Fixed static file paths
2. `src/sono_eval/mobile/app.py` - Fixed API route paths
3. `src/sono_eval/mobile/templates/paths.html` - Fixed API call
4. `src/sono_eval/mobile/templates/assess.html` - Fixed API call

## Next Steps

1. Restart the server if it's running
2. Clear browser cache if needed
3. Test the mobile interface at http://localhost:8000/mobile/

The "Not Found" errors should now be resolved! ✅
