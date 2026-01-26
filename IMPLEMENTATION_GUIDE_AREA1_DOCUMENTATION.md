# Implementation Guide: Area 1 - Documentation Discovery & Progressive Disclosure

**Parent Document:** [UX_ENHANCEMENT_ANALYSIS.md](UX_ENHANCEMENT_ANALYSIS.md)  
**Target:** Documentation Discovery & Progressive Disclosure  
**Priority:** P1  
**Estimated Effort:** Medium (2-3 weeks)  
**For:** Coding Agents

---

## Overview

This guide provides step-by-step instructions for implementing enhanced documentation discovery and progressive disclosure in the Sono-Eval repository.

### Goals
1. Reduce time-to-first-assessment from 15-20 min to 5-7 min
2. Consolidate 100+ documentation files into discoverable structure
3. Implement progressive disclosure for different user personas
4. Add full-text search capability
5. Create visual documentation map

---

## Phase 1: Consolidate Quick Start (Priority: HIGHEST)

### Task 1.1: Merge Quick Start Documents

**Objective:** Create single, comprehensive 5-minute quick start guide

**Files to Modify:**
- `Documentation/START_HERE.md` (expand)
- `Documentation/Guides/QUICK_START.md` (consolidate into START_HERE)
- `README.md` (simplify, point to START_HERE)

**Implementation Steps:**

1. **Create Enhanced START_HERE.md**
   - Location: `Documentation/START_HERE.md`
   - Content structure:
     ```markdown
     # Start Here - 5 Minute Quick Start
     
     ## Choose Your Path (Interactive Tabs)
     
     ### Tab 1: 🚀 Try It (Default - 5 minutes)
     **For:** First-time users who want to see Sono-Eval in action
     
     #### Prerequisites Check
     - [ ] Docker installed? [Check now](#docker-check)
     - [ ] Git installed? [Check now](#git-check)
     
     #### Three Commands to Success
     ```bash
     # 1. Clone (30 seconds)
     git clone https://github.com/doronpers/sono-eval.git
     cd sono-eval
     
     # 2. Start (2 minutes)
     ./launcher.sh start
     
     # 3. Run First Assessment (2 minutes)
     ./launcher.sh cli assess run \
       --candidate-id demo \
       --content "def hello(): return 'world'" \
       --paths technical
     ```
     
     ✅ **Success!** You just ran your first assessment.
     
     **What Just Happened?**
     - Docker containers started (API, DB, Redis, Celery, Superset)
     - API available at http://localhost:8000/docs
     - Code assessed across Technical path
     - Results saved to memory
     
     **Next Steps:** [View Results](#view-results) | [Run Web UI](#web-ui) | [Learn More](#learn)
     
     ### Tab 2: 📚 Learn (15 minutes)
     **For:** Users who want to understand before trying
     
     #### What is Sono-Eval?
     [Expandable section with architecture, concepts, design philosophy]
     
     #### How It Works
     [Expandable section with assessment paths, scoring, memory]
     
     #### Then: [Go to Try It tab](#try-it)
     
     ### Tab 3: 🛠️ Build (30 minutes)
     **For:** Developers who want to contribute or extend
     
     #### Development Setup
     [Expandable section with local Python setup, testing, linting]
     
     #### Architecture Deep Dive
     [Link to Core/concepts/architecture.md]
     
     #### Contributing Guide
     [Link to CONTRIBUTING.md]
     ```

2. **Simplify README.md**
   - Remove duplicate "Quick Start" section
   - Add prominent CTA: "👉 **[Start Here →](Documentation/START_HERE.md)**"
   - Keep: Overview, Features (collapsed), Architecture diagram, Links
   - Move: Detailed setup instructions to START_HERE.md

3. **Archive Old QUICK_START.md**
   - Rename: `Documentation/Guides/QUICK_START.md` → `Documentation/Archive/QUICK_START_v0.3.md`
   - Add redirect notice in old file pointing to new START_HERE.md
   - Update all links in other documents

**Validation:**
```bash
# Test: Can a new user complete first assessment in 5 minutes?
time {
  git clone https://github.com/doronpers/sono-eval.git
  cd sono-eval
  ./launcher.sh start
  ./launcher.sh cli assess run --candidate-id demo --content "print('test')" --paths technical
}
# Expected: < 5 minutes
```

---

### Task 1.2: Implement Progressive Disclosure UI

**Objective:** Hide advanced options, show them on demand

**Files to Create:**
- `Documentation/components/collapsible-section.html` (if adding HTML viewer)
- `Documentation/scripts/progressive-disclosure.js` (if adding interactivity)

**Implementation Steps:**

1. **Add Collapsible Sections** (Markdown + HTML)
   - Use `<details>` and `<summary>` HTML tags (GitHub-compatible)
   - Example:
     ```markdown
     ## Installation
     
     ### Quick Start (Recommended)
     [3 commands here]
     
     <details>
     <summary>Advanced Installation Options</summary>
     
     #### Local Python Setup
     [Detailed steps here]
     
     #### Manual Docker Setup
     [Detailed steps here]
     
     #### Windows-Specific Instructions
     [Detailed steps here]
     
     </details>
     ```

2. **Apply to All Documentation**
   - Pattern: "80% use case" visible, "20% advanced" collapsed
   - Files to update:
     - `Documentation/Guides/user-guide/installation.md`
     - `Documentation/Guides/user-guide/configuration.md`
     - `Documentation/Guides/user-guide/cli-reference.md`
     - `Documentation/Guides/user-guide/api-reference.md`

3. **Add "Show All" Toggle**
   - JavaScript (for web viewer): Button to expand all `<details>` at once
   - Keyboard shortcut: `Shift+A` = "Show All"

**Validation:**
- Count ratio: Visible content vs collapsed content should be 80:20
- User test: Can 80% of users complete tasks without expanding sections?

---

## Phase 2: Full-Text Search (Priority: HIGH)

### Task 2.1: Generate Search Index

**Objective:** Enable full-text search across all documentation

**Files to Create:**
- `Documentation/search-index.json` (generated)
- `scripts/generate_search_index.py` (script)

**Implementation Steps:**

1. **Create Search Index Generator**
   ```python
   # scripts/generate_search_index.py
   import os
   import json
   import re
   from pathlib import Path
   
   def extract_headings(markdown_content):
       """Extract all headings and their content."""
       headings = re.findall(r'^(#{1,6})\s+(.+)$', markdown_content, re.MULTILINE)
       return headings
   
   def generate_search_index(docs_dir='Documentation'):
       """Generate search index from all markdown files."""
       index = []
       
       for md_file in Path(docs_dir).rglob('*.md'):
           with open(md_file, 'r', encoding='utf-8') as f:
               content = f.read()
           
           # Extract metadata
           headings = extract_headings(content)
           title = headings[0][1] if headings else md_file.stem
           
           # Create search entry
           entry = {
               'path': str(md_file),
               'title': title,
               'content': content,
               'headings': [h[1] for h in headings],
               'keywords': extract_keywords(content),
               'word_count': len(content.split()),
           }
           index.append(entry)
       
       # Write index
       with open('Documentation/search-index.json', 'w') as f:
           json.dump(index, f, indent=2)
       
       print(f"✅ Generated search index: {len(index)} documents")
   
   if __name__ == '__main__':
       generate_search_index()
   ```

2. **Add to Build Process**
   ```bash
   # Add to Makefile
   .PHONY: docs-index
   docs-index:
       python3 scripts/generate_search_index.py
   
   # Run before committing docs
   make docs-index
   ```

3. **Add Search Keywords to Documents**
   - Add YAML frontmatter to all docs:
     ```markdown
     ---
     keywords: [assessment, evaluation, quick-start, docker, api]
     persona: [beginner, developer, operator]
     reading_time: 5
     ---
     
     # Document Title
     ```

**Validation:**
```bash
# Generate index
python3 scripts/generate_search_index.py

# Verify
jq '.[] | {path, title, keyword_count: (.keywords | length)}' Documentation/search-index.json | head -20
```

---

### Task 2.2: Implement Search Interface

**Objective:** Add searchable documentation viewer

**Option A: GitHub Pages + Docsify (Recommended)**

**Files to Create:**
- `Documentation/index.html` (Docsify entry point)
- `Documentation/.nojekyll` (disable Jekyll)
- `Documentation/_sidebar.md` (navigation)

**Implementation:**

1. **Setup Docsify**
   ```html
   <!-- Documentation/index.html -->
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <title>Sono-Eval Documentation</title>
     <meta name="description" content="Explainable multi-path developer assessment">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
     <style>
       .search input {
         font-size: 16px;
         border-radius: 4px;
       }
     </style>
   </head>
   <body>
     <div id="app"></div>
     <script>
       window.$docsify = {
         name: 'Sono-Eval',
         repo: 'doronpers/sono-eval',
         loadSidebar: true,
         subMaxLevel: 2,
         search: {
           paths: 'auto',
           placeholder: 'Search documentation...',
           noData: 'No results found',
           depth: 6,
           maxAge: 86400000, // 1 day
         },
         pagination: {
           previousText: '← Previous',
           nextText: 'Next →',
         },
       }
     </script>
     <script src="//cdn.jsdelivr.net/npm/docsify@4"></script>
     <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
   </body>
   </html>
   ```

2. **Create Sidebar Navigation**
   ```markdown
   <!-- Documentation/_sidebar.md -->
   - [Start Here](START_HERE.md)
   - [Quick Search](SEARCH.md)
   
   - Getting Started
     - [Quick Start](Guides/QUICK_START.md)
     - [Installation](Guides/user-guide/installation.md)
     - [Configuration](Guides/user-guide/configuration.md)
   
   - User Guides
     - [CLI Reference](Guides/user-guide/cli-reference.md)
     - [API Reference](Guides/user-guide/api-reference.md)
     - [Mobile Companion](Guides/mobile-companion.md)
   
   - Core Concepts
     - [Architecture](Core/concepts/architecture.md)
     - [Glossary](Core/concepts/glossary.md)
   
   - Contributing
     - [Contributing Guide](../CONTRIBUTING.md)
     - [Agent Guidelines](../AGENT_KNOWLEDGE_BASE.md)
   ```

3. **Enable GitHub Pages**
   - Settings → Pages → Source: `main` branch, `/Documentation` folder
   - URL will be: `https://doronpers.github.io/sono-eval/`

**Option B: Local Search Script (CLI)**

```python
# scripts/search_docs.py
import sys
import json
from pathlib import Path

def search_docs(query, index_path='Documentation/search-index.json'):
    """Search documentation by keyword."""
    with open(index_path, 'r') as f:
        index = json.load(f)
    
    results = []
    for doc in index:
        if query.lower() in doc['content'].lower():
            # Calculate relevance score
            score = doc['content'].lower().count(query.lower())
            results.append((score, doc))
    
    # Sort by relevance
    results.sort(reverse=True, key=lambda x: x[0])
    
    # Display results
    print(f"\n🔍 Found {len(results)} results for '{query}':\n")
    for i, (score, doc) in enumerate(results[:10], 1):
        print(f"{i}. {doc['title']}")
        print(f"   📄 {doc['path']}")
        print(f"   📊 Relevance: {score} matches\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/search_docs.py <query>")
        sys.exit(1)
    
    search_docs(' '.join(sys.argv[1:]))
```

**Validation:**
- Test search: "quick start", "docker", "API authentication"
- Verify results are relevant and ranked correctly

---

## Phase 3: Documentation Map Visualization (Priority: MEDIUM)

### Task 3.1: Generate Visual Sitemap

**Objective:** Create interactive map showing all documentation relationships

**Files to Create:**
- `Documentation/sitemap.html` (interactive map)
- `scripts/generate_sitemap.py` (generator)

**Implementation:**

1. **Create Sitemap Generator**
   ```python
   # scripts/generate_sitemap.py
   import json
   from pathlib import Path
   import yaml
   
   def parse_markdown_frontmatter(filepath):
       """Extract YAML frontmatter from markdown."""
       with open(filepath, 'r') as f:
           content = f.read()
       
       if content.startswith('---'):
           parts = content.split('---', 2)
           if len(parts) >= 3:
               return yaml.safe_load(parts[1])
       return {}
   
   def generate_sitemap_data(docs_dir='Documentation'):
       """Generate sitemap data structure."""
       sitemap = {
           'nodes': [],
           'links': [],
       }
       
       for md_file in Path(docs_dir).rglob('*.md'):
           metadata = parse_markdown_frontmatter(md_file)
           
           node = {
               'id': str(md_file),
               'name': metadata.get('title', md_file.stem),
               'persona': metadata.get('persona', ['general']),
               'reading_time': metadata.get('reading_time', 0),
               'category': str(md_file.parent.name),
           }
           sitemap['nodes'].append(node)
           
           # Extract links to other docs
           with open(md_file, 'r') as f:
               content = f.read()
               import re
               links = re.findall(r'\[.*?\]\((.*?\.md)\)', content)
               for link in links:
                   sitemap['links'].append({
                       'source': str(md_file),
                       'target': str((md_file.parent / link).resolve()),
                       'type': 'reference',
                   })
       
       return sitemap
   
   if __name__ == '__main__':
       sitemap = generate_sitemap_data()
       with open('Documentation/sitemap.json', 'w') as f:
           json.dump(sitemap, f, indent=2)
       print(f"✅ Generated sitemap: {len(sitemap['nodes'])} nodes, {len(sitemap['links'])} links")
   ```

2. **Create Interactive Visualization**
   ```html
   <!-- Documentation/sitemap.html -->
   <!DOCTYPE html>
   <html>
   <head>
     <title>Sono-Eval Documentation Map</title>
     <script src="https://d3js.org/d3.v7.min.js"></script>
     <style>
       body { margin: 0; font-family: Arial, sans-serif; }
       #graph { width: 100vw; height: 100vh; }
       .node { cursor: pointer; }
       .node circle { stroke: #fff; stroke-width: 2px; }
       .node text { font-size: 12px; }
       .link { stroke: #999; stroke-opacity: 0.6; }
       .legend { position: fixed; top: 20px; right: 20px; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
     </style>
   </head>
   <body>
     <div id="graph"></div>
     <div class="legend">
       <h3>Documentation Map</h3>
       <div><span style="color: #4CAF50;">●</span> Getting Started</div>
       <div><span style="color: #2196F3;">●</span> User Guides</div>
       <div><span style="color: #FF9800;">●</span> Core Concepts</div>
       <div><span style="color: #9C27B0;">●</span> Developer</div>
     </div>
     
     <script>
       fetch('sitemap.json')
         .then(r => r.json())
         .then(data => {
           const width = window.innerWidth;
           const height = window.innerHeight;
           
           // Color scale by category
           const color = d3.scaleOrdinal()
             .domain(['Guides', 'Core', 'user-guide', 'Archive'])
             .range(['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']);
           
           // Create force simulation
           const simulation = d3.forceSimulation(data.nodes)
             .force('link', d3.forceLink(data.links).id(d => d.id).distance(100))
             .force('charge', d3.forceManyBody().strength(-300))
             .force('center', d3.forceCenter(width / 2, height / 2));
           
           // Create SVG
           const svg = d3.select('#graph')
             .append('svg')
             .attr('width', width)
             .attr('height', height);
           
           // Draw links
           const link = svg.append('g')
             .selectAll('line')
             .data(data.links)
             .enter().append('line')
             .attr('class', 'link');
           
           // Draw nodes
           const node = svg.append('g')
             .selectAll('g')
             .data(data.nodes)
             .enter().append('g')
             .attr('class', 'node')
             .call(d3.drag()
               .on('start', dragstarted)
               .on('drag', dragged)
               .on('end', dragended));
           
           node.append('circle')
             .attr('r', d => 5 + d.reading_time)
             .attr('fill', d => color(d.category));
           
           node.append('text')
             .attr('dx', 12)
             .attr('dy', '.35em')
             .text(d => d.name);
           
           // Add tooltips
           node.append('title')
             .text(d => `${d.name}\nCategory: ${d.category}\nReading time: ${d.reading_time} min`);
           
           // Click to open document
           node.on('click', function(event, d) {
             window.open(d.id, '_blank');
           });
           
           // Update positions on tick
           simulation.on('tick', () => {
             link
               .attr('x1', d => d.source.x)
               .attr('y1', d => d.source.y)
               .attr('x2', d => d.target.x)
               .attr('y2', d => d.target.y);
             
             node.attr('transform', d => `translate(${d.x},${d.y})`);
           });
           
           function dragstarted(event) {
             if (!event.active) simulation.alphaTarget(0.3).restart();
             event.subject.fx = event.subject.x;
             event.subject.fy = event.subject.y;
           }
           
           function dragged(event) {
             event.subject.fx = event.x;
             event.subject.fy = event.y;
           }
           
           function dragended(event) {
             if (!event.active) simulation.alphaTarget(0);
             event.subject.fx = null;
             event.subject.fy = null;
           }
         });
     </script>
   </body>
   </html>
   ```

**Validation:**
- Open `Documentation/sitemap.html` in browser
- Verify all nodes are visible and clickable
- Test drag-and-drop interaction
- Verify links show document relationships

---

## Phase 4: Integration & Testing

### Task 4.1: Update All Cross-References

**Objective:** Ensure all documentation links work after restructuring

**Implementation:**

1. **Create Link Checker Script**
   ```python
   # scripts/check_doc_links.py
   import re
   from pathlib import Path
   
   def check_markdown_links(docs_dir='Documentation'):
       """Check all markdown links are valid."""
       broken_links = []
       
       for md_file in Path(docs_dir).rglob('*.md'):
           with open(md_file, 'r') as f:
               content = f.read()
           
           # Find all markdown links
           links = re.findall(r'\[.*?\]\((.*?)\)', content)
           
           for link in links:
               if link.startswith('http'):
                   continue  # Skip external links
               
               # Resolve relative path
               target = (md_file.parent / link).resolve()
               
               if not target.exists():
                   broken_links.append({
                       'file': str(md_file),
                       'link': link,
                       'target': str(target),
                   })
       
       if broken_links:
           print(f"❌ Found {len(broken_links)} broken links:")
           for item in broken_links:
               print(f"   {item['file']}: {item['link']}")
           return False
       else:
           print("✅ All links are valid")
           return True
   
   if __name__ == '__main__':
       import sys
       sys.exit(0 if check_markdown_links() else 1)
   ```

2. **Add to CI/CD**
   ```yaml
   # .github/workflows/docs-check.yml
   name: Documentation Check
   
   on:
     pull_request:
       paths:
         - 'Documentation/**'
         - '**.md'
   
   jobs:
     check-docs:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Check documentation links
           run: python3 scripts/check_doc_links.py
   ```

3. **Run and Fix**
   ```bash
   # Check links
   python3 scripts/check_doc_links.py
   
   # Fix any broken links
   # Then regenerate search index
   python3 scripts/generate_search_index.py
   ```

---

### Task 4.2: User Acceptance Testing

**Objective:** Validate that improvements achieve goals

**Test Plan:**

1. **Timed First Assessment Test**
   - Recruit 10 new users (no prior Sono-Eval experience)
   - Task: "Complete your first assessment"
   - Measure: Time from landing on README to seeing results
   - Success criteria: <7 minutes (currently 15-20 min)

2. **Documentation Discovery Test**
   - Task: "Find how to configure Redis caching"
   - Measure: Time to find + confidence score
   - Success criteria: <2 minutes, 80% confidence

3. **A/B Test (if possible)**
   - Group A: Old documentation structure
   - Group B: New documentation structure
   - Measure: Completion rate, time, satisfaction
   - Success criteria: Group B 50% faster, 30% higher satisfaction

4. **Analytics Tracking**
   - Add Google Analytics to GitHub Pages docs
   - Track: Page views, bounce rate, search queries
   - Monitor for 2 weeks post-launch

---

## Rollout Plan

### Pre-Launch
1. Generate search index: `make docs-index`
2. Check all links: `python3 scripts/check_doc_links.py`
3. Deploy to GitHub Pages (test)
4. Internal team review

### Launch
1. Merge PR with all changes
2. Deploy GitHub Pages: Settings → Enable
3. Update README with new links
4. Announce in Discussions

### Post-Launch
1. Monitor analytics
2. Collect user feedback
3. Iterate on search relevance
4. Add missing keywords

---

## Success Metrics

### Quantitative
- Time-to-first-assessment: 5-7 min (baseline: 15-20 min)
- Documentation views: +50%
- Bounce rate: <20% (baseline: ~40%)
- Search usage: 50%+ of sessions

### Qualitative
- User feedback score: 4.5/5 (baseline: 3.5/5)
- Support questions: -30%
- "Documentation is confusing" feedback: -70%

---

## Maintenance

### Weekly
- Regenerate search index: `make docs-index`
- Check for broken links: `python3 scripts/check_doc_links.py`

### Monthly
- Review analytics: Most/least viewed pages
- Update based on feedback
- Refine search keywords

### Quarterly
- User survey: Documentation satisfaction
- Audit for outdated content
- Major restructure if needed

---

## Troubleshooting

### Issue: Search not working on GitHub Pages
**Solution:** Ensure `.nojekyll` file exists in `Documentation/`

### Issue: Links broken after restructure
**Solution:** Use link checker script, update redirect map

### Issue: Docsify not loading
**Solution:** Check browser console, verify CDN URLs, check CORS

---

## Related Documents
- [UX_ENHANCEMENT_ANALYSIS.md](UX_ENHANCEMENT_ANALYSIS.md) - Parent analysis
- [IMPLEMENTATION_GUIDE_AREA2_ONBOARDING.md](IMPLEMENTATION_GUIDE_AREA2_ONBOARDING.md) - Onboarding guide
- [IMPLEMENTATION_GUIDE_AREA3_ERROR_RECOVERY.md](IMPLEMENTATION_GUIDE_AREA3_ERROR_RECOVERY.md) - Error recovery guide

---

**Version:** 1.0  
**Last Updated:** January 25, 2026  
**Status:** Ready for Implementation
