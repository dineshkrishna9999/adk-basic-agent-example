# ADK Basic Agent Example

A simple demonstration of Google's Agent Development Kit (ADK) showing how to create a basic agent with custom tools and Azure OpenAI integration.

## Overview

This project demonstrates:
- Creating a basic ADK agent with custom tools
- Integrating with Azure OpenAI using LiteLLM
- Using in-memory session management
- Custom function calling with simple arithmetic operations

## Prerequisites

- Python 3.10 or higher
- Azure OpenAI API access
- Google ADK Python library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/dineshkrishna9999/reproduce-adk-bug-4249.git
cd reproduce-adk-bug-4249
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

## Usage

Run the basic agent example:

```bash
python step1_basic_agent.py
```

The agent will:
1. Accept a user message asking to add two numbers
2. Call the custom `add` function
3. Return the result in a natural language response

## Project Structure

```
.
├── step1_basic_agent.py    # Main agent implementation
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Features

- **Custom Tool Integration**: Demonstrates how to add custom Python functions as agent tools
- **Azure OpenAI**: Uses Azure OpenAI through LiteLLM for flexible model integration
- **Session Management**: In-memory session handling for conversation state
- **Simple Runner**: Shows basic agent execution pattern

## Example Output

```
The sum of 1 and 2 is 3!
```

## Development

The agent is configured with:
- Model: Azure GPT-4.1
- Instruction: "You are a helpful assistant. reply in one short sentence."
- Tools: `add(a: int, b: int)` function

## Contributing

This is a demonstration project for reproducing and testing ADK behavior. Feel free to fork and experiment!

## License

MIT License - See LICENSE file for details

## Author

**Dinesh Karakambaka**
- GitHub: [@dineshkrishna9999](https://github.com/dineshkrishna9999)
- Email: kdineshkvkl@gmail.com

## Acknowledgments

- Google Agent Development Kit (ADK)
- LiteLLM for unified LLM API interface
