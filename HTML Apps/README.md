# Canvasarchive - AI Bot Development Repository

## For Codex: Repository Purpose
This repository contains production-ready AI bots and development resources for creating new Poe platform bots. Primary use cases:
- **UI Testing**: Canvas apps provide interactive interfaces for testing bot concepts
- **Bot Development**: Server bot shows FastAPI + Modal deployment patterns  
- **Prompt Engineering**: Comprehensive prompt points reference for optimization
- **Code Generation**: HTML apps demonstrate frontend integration patterns

## Repository Structure
```
canvasarchive/
├── canvas-apps/            # 20 executable HTML/CSS/JS applications
├── prompt-bots/            # 12 instruction-based bots (.md format)
├── roleplay-bots/          # 4 character-driven bots (.md format)
├── server-bot/             # Python server bot + deployment config
├── Prompt Points perplexity.csv  # Comprehensive bot development reference
└── README.md               # This file
```

## 🎯 Key Development Resources

### Prompt Points Reference (CRITICAL FOR CODEX)
**File**: `Prompt Points perplexity.csv`
- **20+ development techniques** across Core Construction, Knowledge Enhancement, Response Behavior, Output Formatting
- **Strategic use cases** for each technique with supporting documentation
- **Bot type mappings** (Prompt Bot vs Server Bot capabilities)
- **Essential reading** for understanding Poe bot architecture and optimization

### Server Bot Implementation
**File**: `server-bot/DRBanger_server.py`
- **Modal + FastAPI** production deployment pattern
- **Chained bot logic** for complex multi-step processing
- **Legal research system** with parser → analysis → synthesis workflow
- **Reference implementation** for server bot development

## 🚀 Development Workflows

### Canvas Apps (Frontend Testing)
- **20 interactive applications** for UI concept validation
- **Modern web stack**: HTML5, CSS3, JavaScript ES6+
- **CDN dependencies**: Tailwind CSS, external APIs
- **Responsive design** patterns for multi-device compatibility
- **Direct browser execution** - no build process required

### Bot Creation Process
1. **Reference**: Use `Prompt Points perplexity.csv` for technique selection
2. **Prototype**: Test concepts in canvas apps for UI interactions
3. **Implement**: Follow `DRBanger_server.py` patterns for server bots
4. **Deploy**: Modal/FastAPI stack for production environments

## 🔧 Technical Architecture

### Canvas Apps Structure
- **Self-contained HTML** files with embedded CSS/JS
- **External API integration** patterns (image generation, AI models)
- **State management** examples for complex interactions
- **Error handling** and user feedback systems

### Server Bot Patterns
- **Modal containerization** for scalable deployment
- **FastAPI-Poe integration** for Poe platform compatibility
- **Async response handling** for streaming interactions
- **Bot chaining logic** for complex multi-step workflows

### Prompt Engineering Framework
- **Temperature controls** (0.0-2.0 for creativity vs consistency)
- **Stop sequences** for precise response termination
- **Knowledge base integration** (.txt, .pdf, .docx, .html files)
- **Metadata persistence** for conversation state management

## 💻 Development Commands (For Codex)

### Testing Canvas Apps
```bash
# Open any HTML file directly in browser
open canvas-apps/VG-IMGrok_canvas.html

# Or serve locally for development
python -m http.server 8000
# Then visit: http://localhost:8000/canvas-apps/
```

### Server Bot Development
```bash
# Install dependencies
pip install modal fastapi-poe aiohttp uvicorn

# Test locally
python server-bot/DRBanger_server.py

# Deploy to Modal
modal deploy server-bot/DRBanger_server.py
```

### Prompt Analysis
```bash
# Analyze prompt techniques
grep "Core Prompt Construction" "Prompt Points perplexity.csv"
grep "Server Bot" "Prompt Points perplexity.csv"
```

## 📊 Bot Categories & Use Cases

| Category | Count | Format | Primary Use | Development Focus |
|----------|-------|--------|-------------|-------------------|
| Canvas Apps | 20 | HTML/CSS/JS | UI Testing, Frontend | Interactive interfaces, API integration |
| Prompt Bots | 12 | Markdown | Instruction Copy-Paste | Prompt engineering, behavior definition |
| Roleplay Bots | 4 | Markdown | Character Interactions | Personality modeling, conversation flow |
| Server Bot | 1 | Python | Production Deployment | Backend logic, API orchestration |

## 🔍 For AI Development Teams
This repository serves as a **comprehensive reference implementation** for Poe platform bot development, covering frontend interfaces, backend logic, and deployment patterns. Use the Prompt Points reference as your primary development guide.