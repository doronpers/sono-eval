# Mobile Companion Guide

**Optional, Interactive Companion for Desktop Users**

The Sono-Eval Mobile Companion is an optional, mobile-optimized interface that complements the primary desktop workflow. Use it when a guided, touch-friendly flow is helpful, while desktop remains the default experience.

---

## 🎯 What is the Mobile Companion?

The Mobile Companion is a web-based interface designed for mobile devices that:

- **Explains Everything**: Clear descriptions of what's being assessed and why
- **Guides You Through**: Step-by-step process with helpful tips
- **Lets You Choose**: Select which skill areas you want to focus on
- **Works Anywhere**: Fully responsive design for phones, tablets, and desktops
- **Saves Progress**: Your work is saved as you go (in browser session)

---

## ✨ Key Features

### For Candidates

- **📱 Mobile-First Design**: Optimized for touchscreens and small displays
- **💡 Explanatory**: Understand what's being assessed at each step
- **🎨 Interactive**: Engaging UI with smooth animations
- **🔀 Non-Linear**: Skip sections, come back later, choose your path
- **⏱️ Time Estimates**: Know how long each section takes
- **💾 Auto-Save**: Work saved in your browser session

### User Experience

- **Progressive Disclosure**: Information revealed when you need it
- **Personalization**: Tailor the experience to your goals
- **Clear Feedback**: Detailed results with actionable recommendations
- **No Account Required**: Try it out immediately

---

## 🚀 Quick Start

### Access the Mobile Companion (Optional)

1. Start the Sono-Eval API server:

   ```bash
   ./launcher.sh start
   # OR
   sono-eval server start
   ```

2. Open your mobile browser and navigate to:

   ```
   http://localhost:8000/mobile
   ```

3. Follow the interactive prompts!

---

## 📱 User Journey

### Step 1: Welcome Screen

The welcome screen introduces the assessment system and explains what makes it different:

- Clear value proposition
- Time estimates
- Privacy information
- Expandable "Learn More" sections

**Features:**

- Large, tappable buttons
- Easy-to-read typography
- Clear visual hierarchy

### Step 2: Getting Started

Enter your information:

- Identifier (name or email)
- Experience level (optional)
- Learning goals (optional)

**Personalization:**
The system uses this information to tailor feedback and recommendations.

### Step 3: Choose Focus Areas

Select 1-4 skill areas to assess:

- **Technical Skills** - Code quality, architecture, testing
- **Design Thinking** - Problem analysis, solution design
- **Collaboration** - Communication, teamwork, documentation
- **Problem Solving** - Analytical thinking, debugging

**Interactive Elements:**

- Tap cards to select/deselect
- "Learn more" buttons for detailed explanations
- Real-time time estimates
- Visual selection indicators

### Step 4: Complete Assessment

For each selected area:

- Submit code or describe your approach
- Explain your thinking process
- Answer optional follow-up questions

**Non-Linear Navigation:**

- Tab between sections
- Skip and return later
- Previous/Next navigation
- Progress indicator

### Step 5: View Results

Detailed feedback including:

- Overall score with confidence level
- Per-path scores and breakdowns
- Identified strengths
- Areas for improvement
- Specific recommendations

**Interactive Results:**

- Visual score displays
- Expandable sections
- Share functionality
- Option to take another assessment

---

## 💻 Implementation Details

### Architecture

```
Mobile Companion
├── FastAPI Backend (mobile/app.py)
│   ├── Page Routes (HTML templates)
│   └── API Routes (/api/mobile/*)
├── HTML Templates (mobile/templates/)
│   ├── base.html (shared layout)
│   ├── index.html (welcome)
│   ├── start.html (getting started)
│   ├── paths.html (path selection)
│   ├── assess.html (assessment)
│   └── results.html (results)
└── Static Assets (mobile/static/)
    ├── style.css (responsive styles)
    └── script.js (interactivity)
```

### Technology Stack

- **Backend**: FastAPI with Jinja2 templates
- **Frontend**: Vanilla JavaScript (no framework needed)
- **Styling**: Custom CSS with CSS variables
- **Storage**: Browser SessionStorage for state

### API Endpoints

#### Page Routes

- `GET /mobile/` - Welcome screen
- `GET /mobile/start` - Getting started
- `GET /mobile/paths` - Path selection
- `GET /mobile/assess` - Assessment interface
- `GET /mobile/results` - Results display

#### API Routes

- `POST /mobile/api/mobile/assess` - Submit assessment
- `GET /mobile/api/mobile/explain/{path}` - Get path explanation
- `GET /mobile/api/mobile/recommendations` - Get path recommendations
- `POST /mobile/api/mobile/track` - Submit interaction events
- `GET /mobile/api/mobile/easter-eggs` - List available easter eggs

---

## 🎨 Design Principles

### Mobile-First

- Touch-optimized tap targets (minimum 44×44px)
- Large, readable fonts (minimum 16px)
- Adequate spacing between interactive elements
- Smooth animations and transitions

### Progressive Disclosure

- Show only essential information initially
- Expandable sections for additional details
- "Learn more" buttons for deeper explanations
- Optional questions clearly marked

### Personalization

- User chooses which paths to evaluate
- Adjust experience based on skill level
- Time estimates based on selections
- Relevant recommendations based on goals

### Clear Communication

- Plain language, no jargon
- Visual icons and emoji for quick scanning
- Color-coded feedback (green = strength, orange = improvement)
- Specific, actionable recommendations

---

## 🔧 Configuration

### Customization Options

You can customize the mobile companion by modifying:

1. **Path Definitions** (`mobile/app.py`):

   ```python
   "paths": [
       {
           "id": "technical",
           "name": "Technical Skills",
           "icon": "⚙️",
           "description": "...",
           "time": "15-20 min",
       },
       # Add more paths...
   ]
   ```

2. **Styling** (`mobile/static/style.css`):

   ```css
   :root {
       --primary-color: #2196F3;  /* Change brand color */
       --success-color: #4CAF50;
       /* ... other colors */
   }
   ```

3. **Content** (templates in `mobile/templates/`):
   - Edit HTML templates to change text
   - Modify explanations and tips
   - Adjust layout and structure

---

## 📊 Analytics & Tracking

The mobile companion includes hooks for analytics:

```javascript
// In mobile/static/script.js
trackEvent('assessment', 'started', candidateId);
trackEvent('path', 'selected', pathId);
trackEvent('assessment', 'completed', assessmentId);
```

Integrate with your analytics platform (Google Analytics, Mixpanel, etc.) by implementing the `trackEvent` function.

---

## 🔒 Privacy & Security

### Data Handling

- No data sent to third parties
- Session storage cleared on browser close
- All communication over HTTPS (in production)
- No cookies required

### Best Practices

- Use HTTPS in production
- Implement rate limiting
- Add CSRF protection for forms
- Sanitize user inputs

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Test on various mobile devices (iOS, Android)
- [ ] Test on different screen sizes (phone, tablet)
- [ ] Test in different browsers (Safari, Chrome, Firefox)
- [ ] Test touch interactions (tap, swipe, scroll)
- [ ] Test with slow network connections
- [ ] Test offline behavior
- [ ] Test form validation
- [ ] Test navigation flow (back, forward, skip)

### Automated Testing

Add tests in `tests/test_mobile.py`:

```python
def test_mobile_home():
    """Test mobile home page loads."""
    response = client.get("/mobile/")
    assert response.status_code == 200
    assert "Welcome to Sono-Eval" in response.text
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Styles not loading**

- Check static files are mounted correctly
- Verify path: `/mobile/static/style.css`
- Clear browser cache

**Issue: Templates not found**

- Verify templates directory: `mobile/templates/`
- Check Jinja2Templates configuration
- Ensure templates use correct extends/includes

**Issue: API calls failing**

- Check CORS settings
- Verify API endpoints are registered
- Check browser console for errors

**Issue: Session data not persisting**

- SessionStorage is cleared on browser close
- Private browsing may block storage
- Check browser storage settings

---

## 🚀 Deployment

### Production Checklist

- [ ] Set environment variables
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Enable compression
- [ ] Minify CSS/JS
- [ ] Add error monitoring
- [ ] Test on real mobile devices
- [ ] Optimize images (if added)
- [ ] Add meta tags for SEO

### Docker Deployment

The mobile companion is automatically included when running:

```bash
./launcher.sh start
```

Access at: `http://localhost:8000/mobile`

### Standalone Deployment

Run just the mobile app:

```bash
python -m sono_eval.mobile.app
```

Access at: `http://localhost:8001`

---

## 📈 Future Enhancements

Potential improvements:

- Offline support with Service Workers
- Native mobile app wrappers (React Native)
- Push notifications for completed assessments
- Social sharing with preview cards
- Multi-language support
- Voice input for answers
- Screen reader optimizations
- Dark mode support
- Progressive Web App (PWA) features

---

## 💡 Tips for Evaluators

### Encouraging Mobile Usage

1. **Share the Direct Link**: `http://your-domain.com/mobile`
2. **Include in Emails**: Add mobile link to candidate invitations
3. **QR Codes**: Generate QR codes for easy access
4. **Test First**: Complete an assessment yourself to understand the flow

### Reviewing Mobile Assessments

Mobile assessments are marked with:

```json
{
  "submission_type": "mobile_interactive",
  "options": {
    "source": "mobile_companion"
  }
}
```

This helps you understand the context when reviewing results.

---

## 🤝 Contributing

Want to improve the mobile companion? See our [Contributing Guide](../CONTRIBUTING.md).

Ideas for contributions:

- Additional assessment paths
- Improved accessibility
- Better animations
- More personalization options
- Additional languages

---

## 📚 Related Documentation

- [Installation Guide](user-guide/installation.md)
- [API Reference](user-guide/api-reference.md)
- [Candidate Guide](resources/candidate-guide.md)
- [Architecture](../Core/concepts/architecture.md)

---

**Questions?** Check the [FAQ](faq.md) or [open an issue](https://github.com/doronpers/sono-eval/issues).

---

*Last Updated: January 15, 2026*
