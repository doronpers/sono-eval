# Mobile Companion - Quick Reference

## 🚀 Quick Start

### Start the Server
```bash
# Using Docker (recommended)
./launcher.sh start

# Or standalone
python -m sono_eval.api.main
```

### Access Mobile Interface
Open in your mobile browser:
```
http://localhost:8000/mobile
```

## 📱 Features

- **Mobile-optimized UI** - Designed for touchscreens
- **Step-by-step guidance** - Clear instructions at each stage
- **Interactive path selection** - Choose your focus areas
- **Non-linear navigation** - Skip and return to sections
- **Detailed explanations** - Understand what's being evaluated
- **Visual feedback** - See results with clear visualizations

## 🎯 User Flow

1. **Welcome** (`/mobile/`) - Introduction and overview
2. **Start** (`/mobile/start`) - Enter your information
3. **Paths** (`/mobile/paths`) - Select assessment focus areas
4. **Assess** (`/mobile/assess`) - Complete interactive assessment
5. **Results** (`/mobile/results`) - View detailed feedback

## 🛠️ Development

### File Structure
```
mobile/
├── app.py              # FastAPI application
├── templates/          # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── start.html
│   ├── paths.html
│   ├── assess.html
│   └── results.html
└── static/             # CSS and JavaScript
    ├── style.css
    └── script.js
```

### API Endpoints

**Pages:**
- `GET /mobile/` - Home page
- `GET /mobile/start` - Getting started
- `GET /mobile/paths` - Path selection
- `GET /mobile/assess` - Assessment
- `GET /mobile/results` - Results

**API:**
- `POST /mobile/api/mobile/assess` - Submit assessment
- `GET /mobile/api/mobile/explain/{path}` - Get path details

## 📖 Full Documentation

See [docs/mobile-companion.md](../../docs/mobile-companion.md) for complete documentation.

## 🎨 Customization

Edit templates in `templates/` and styles in `static/style.css` to customize the appearance and content.

## 🧪 Testing

Run tests with:
```bash
pytest tests/test_mobile.py
```

## 📝 Notes

- Session storage is used to persist state during assessment
- Works on iOS, Android, and desktop browsers
- No account or authentication required
- Responsive design adapts to screen size
