# ADK Bug Reproduction - Issue #4249

**Status: ✅ FIXED in ADK v1.23+**

This repository reproduces [Issue #4249](https://github.com/google/adk-python/issues/4249) from google/adk-python: *"Unintended user message injection breaks tool calling with LiteLLM + OpenAI/Azure"*

## Bug Description

When using LiteLLM with OpenAI/Azure OpenAI models (ADK versions > 1.22.1), after tool execution, ADK incorrectly injects the message:

```
"Handle the requests as specified in the System Instruction."
```

This triggers Azure OpenAI's **jailbreak detection** and causes the request to fail with:

```
openai.BadRequestError: Error code: 400 - The response was filtered due to the prompt 
triggering Azure OpenAI's content management policy.
{'jailbreak': {'filtered': True, 'detected': True}}
```

## Root Cause

In `lite_llm.py`, the `_part_has_payload()` function did not recognize `function_response` as valid payload. When tool responses were returned, ADK thought the Content was empty and triggered fallback logic that appended the problematic text, which OpenAI's safety filters flagged as prompt injection.

## The Fix

The fix (merged in commit [d0102ec](https://github.com/google/adk-python/commit/d0102ecea331e062190dbb7578a4ef7f4044306e)) adds `function_response` recognition to `_part_has_payload()`:

```python
def _part_has_payload(part: types.Part) -> bool:
    if part.text:
        return True
    if part.function_response:  # ← Added this check
        return True
    if part.inline_data and part.inline_data.data:
        return True
    if part.file_data and (part.file_data.file_uri or part.file_data.data):
        return True
    return False
```

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

**Note**: This bug affects ADK versions > 1.22.1 and < 1.23. To reproduce:

1. Install the affected version:
```bash
pip install google-adk==1.22.2  # or any version > 1.22.1 and < 1.23
```

2. Run the reproduction script:
```bash
python step1_basic_agent.py
```

### Expected Behavior
The agent should:
1. Receive user message: "Hello, add these numbers: 1 and 2"
2. Call the `add(1, 2)` tool
3. Receive "3" as the tool response
4. Generate a natural language response like "The sum is 3"

### Actual Behavior (Bug)
The agent flow is interrupted when ADK injects `"Handle the requests as specified in the System Instruction."` after the tool response, causing:
- Azure OpenAI jailbreak detection to trigger
- Request failure with content policy violation
- Error: `content_filter_result: {'jailbreak': {'filtered': True, 'detected': True}}`

### Workaround for Affected Versions

If stuck on an affected version, use this workaround:

```python
class OpenAILiteLlm(LiteLlm):
    """LiteLlm with fix for OpenAI API compatibility."""
    
    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        # Add inline_data to function_response parts so _part_has_payload returns True
        for content in llm_request.contents or []:
            if content.role != "user":
                continue
            for part in content.parts or []:
                if part.function_response and not part.inline_data:
                    part.inline_data = types.Blob(data=b" ", mime_type="text/plain")
        
        async for response in super().generate_content_async(llm_request, stream):
            yield response
```

Or downgrade to:
```bash
pip install google-adk==1.22.1
```

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

- **Python**: 3.10+
- **Affected ADK versions**: > 1.22.1 and < 1.23
- **Fixed in**: ADK v1.23+ (commit d0102ec)
- **Model**: Azure OpenAI GPT-4.1 via LiteLLM
- **Issue**: Content policy violations from unintended message injection

## Bug Impact

This bug prevented the use of:
- ❌ Any tool/function calling with LiteLLM
- ❌ OpenAI models via ADK
- ❌ Azure OpenAI models via ADK
- ✅ Workaround: Downgrade to google-adk==1.22.1

## Issue Timeline

- **Reported**: January 2026 by [@GitMarco27](https://github.com/GitMarco27)
- **Debugged & Reproduced**: By [@dineshkrishna9999](https://github.com/dineshkrishna9999) (this repo author), [@sandangel](https://github.com/sandangel), and others
- **Fixed**: February 2026 in commit [d0102ec](https://github.com/google/adk-python/commit/d0102ecea331e062190dbb7578a4ef7f4044306e)
- **Status**: ✅ Closed and merged

## Related Pull Requests

- [#4314](https://github.com/google/adk-python/pull/4314) - Fix unintended user message injection
- [#4315](https://github.com/google/adk-python/pull/4315) - Fix unintended user message text
- [#4316](https://github.com/google/adk-python/pull/4316) - Handle function_response in payload check (merged)

## Contributing

This bug has been fixed! This repository serves as documentation of the issue and reproduction case. If you encounter similar issues:
1. Check your ADK version: `pip show google-adk`
2. Upgrade to latest: `pip install --upgrade google-adk`
3. Report new issues at: https://github.com/google/adk-python/issues

## License

MIT License - See LICENSE file for details

## Author

**Dinesh Karakambaka**
- GitHub: [@dineshkrishna9999](https://github.com/dineshkrishna9999)
- Email: kdineshkvkl@gmail.com

## Acknowledgments

- Google Agent Development Kit (ADK)
- LiteLLM for unified LLM API interface
