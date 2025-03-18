# achievewith.ai SEO Workflow System

A modular SEO analysis and optimization platform that leverages AI to provide actionable insights for digital content strategies.

<!-- ![Landing page screenshot](static/img/wf2.png) -->


## What It Does

This system orchestrates specialized AI agents to analyze websites, content, and keywords, delivering structured SEO recommendations and insights. Each agent focuses on a specific aspect of SEO:

- **Keyword Research**: Identifies valuable search terms based on intent patterns and competitive analysis
- **Content Strategy**: Provides structured content briefs and outlines based on topic analysis
- **Technical Audit**: Examines website structure and performance issues affecting search visibility
- **Gap Analysis**: Identifies content opportunities by analyzing competitive positioning

## Project Structure

```
achievewith-ai-seo/
├── app.py                          # Main Flask application entry point
├── claude_agent_framework.py       # Core agent communication framework
├── claude_seo_agents.py            # Specialized SEO agent implementations
├── claude_seo_ui.py                # Web UI implementation
├── claude_workflow_orchestrator.py # Workflow coordination system
├── demo_script.py                  # CLI demo script for testing workflows
├── requirements.txt                # Python dependencies
├── logs/                           # System operation logs
├── results/                        # Output storage for completed analyses
├── static/                         # UI assets and resources
├── templates/                      # HTML templates for web interface
├── test_compiler/                  # Testing utilities
└── seo-agent-poc/                  # Proof of concept implementations
```

## Getting Started

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API key: `ANTHROPIC_API_KEY="your-key-here"`
4. Run the application: `python app.py`
5. Access the interface at http://127.0.0.1:8082

## Demo Script

For quick testing without the web interface, use the demo script:

```bash
python demo_script.py
```

This will run a simple SEO workflow and save results to the results directory.

## Core Components

- **Agent Framework**: Handles communication with Claude API and manages conversation context
- **SEO Agents**: Specialized agents for different SEO tasks with targeted system prompts
- **Workflow Orchestrator**: Coordinates multi-step workflows between agents
- **Web UI**: Flask-based interface for configuring and running workflows

## Requirements

- Python 3.8+
- Anthropic API key
- Flask and supporting libraries

## Usage Rights

This repository is provided for demonstration and educational purposes. Viewing and studying the code is permitted, but copying, modification, and distribution require explicit permission from the owner.

---

*AI Disclosure: This project was developed with assistance from Claude, an AI assistant by Anthropic. The implementation includes AI-generated code elements and structure, with human review and approval of the core functionality and business logic.*
