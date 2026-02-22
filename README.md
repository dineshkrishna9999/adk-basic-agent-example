# ADK Bug Reproduction - Issue #4249

This repository reproduces a bug encountered with Google's Agent Development Kit (ADK) related to custom tool execution and response handling.

## Bug Description

This minimal reproducible example demonstrates an issue where:
- Custom tools return formatted strings
- Agent response handling may not properly process tool outputs
- Session management with custom tools shows unexpected behavior

## Overview

This reproduction case includes:
- A basic ADK agent with a custom `add` function
- Azure OpenAI integration via LiteLLM
- In-memory session management
- Minimal code to isolate the bug behavior

## Prerequisites

- Python 3.10 or higher
- Azure OpenAI API access
- Google ADK Python library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/dineshkrishna9999/adk-basic-agent-example.git
cd adk-basic-agent-example
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Azure OpenAI credentials

## Configuration

Create a `.env` file with the following variables:

```env
AZURE_API_KEY=your_azure_api_key
AZURE_API_BASE=your_azure_endpoint
AZURE_API_VERSION=2024-10-01-preview
AZURE_MODEL=azure/gpt-4.1
```

## Reproducing the Bug

Run the reproduction script:

```bash
python step1_basic_agent.py
```

### Expected Behavior
The agent should call the `add` function with arguments (1, 2), receive "3" as the result, and format a natural language response.

### Observed Behavior
[Document the actual bug behavior here when running the script]

## Project Structure

```
.
├── step1_basic_agent.py    # Minimal bug reproduction script
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Code Details

The reproduction script includes:
- **Custom Tool**: `add(a: int, b: int)` - Returns a string with the sum
- **Model**: Azure GPT-4.1 via LiteLLM
- **Session**: In-memory session service
- **Instruction**: Minimal agent instruction for clarity

## Environment

- Python 3.10+
- Google ADK Python library
- LiteLLM for Azure OpenAI integration
- python-dotenv for environment management

## Bug Report

**Issue**: #4249  
**Component**: ADK Python - Tool execution/response handling  
**Status**: Under investigation

## Contributing

If you've encountered similar issues or have insights into this bug, please:
1. Fork this repository
2. Document your findings
3. Submit a pull request with your observations

## License

MIT License - See LICENSE file for details

## Author

**Dinesh Karakambaka**
- GitHub: [@dineshkrishna9999](https://github.com/dineshkrishna9999)
- Email: kdineshkvkl@gmail.com

## Acknowledgments

- Google Agent Development Kit (ADK)
- LiteLLM for unified LLM API interface
