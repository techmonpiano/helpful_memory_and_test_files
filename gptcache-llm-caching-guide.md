# GPTCache - LLM Caching for Open Interpreter Guide

## Overview
GPTCache is a semantic cache for LLMs that can significantly reduce API costs and improve response times. It works perfectly with Open Interpreter to cache LLM responses locally.

**GitHub**: https://github.com/zilliztech/GPTCache (7.6k stars)

## Key Benefits
- **10x cost reduction** through semantic caching
- **100x speed improvement** for cached responses
- **Local storage** - your data stays on your machine
- **Privacy** - prompts/responses aren't sent anywhere else

## Installation
```bash
pip install gptcache
```

## Basic Setup with OpenAI
```python
from gptcache import cache
from gptcache.adapter import openai

cache.init()
cache.set_openai_key()
```

## Using with OpenRouter (280+ models)
Since OpenRouter is OpenAI-compatible, you can use it with GPTCache:

```python
from gptcache import cache
from gptcache.adapter import openai

cache.init()

# Configure OpenAI client to use OpenRouter
import openai
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "your-openrouter-api-key"
```

## Supported Providers
- **Direct Support**: OpenAI, LangChain, LlamaCPP, Dolly, MiniGPT-4
- **Via LangChain**: Anthropic Claude, Google PaLM/Gemini, Cohere, HuggingFace, Azure OpenAI, AWS Bedrock, Ollama (local models)
- **Via OpenAI Compatibility**: OpenRouter (280+ models), any OpenAI-compatible API

## Storage Options
### Default (Local)
- SQLite - local database file

### Other Local Options
- MySQL, PostgreSQL
- Redis
- FAISS (vector store)

### Cloud Options (if needed)
- Milvus
- Zilliz Cloud

## How It Works
1. **Semantic Matching**: Uses embeddings to find similar queries
2. **Local Processing**: All matching happens on your machine
3. **Persistent Cache**: Survives restarts, stored locally
4. **No External Calls**: Cached responses served directly

## Integration with Open Interpreter
While Open Interpreter doesn't have built-in caching, you can:
1. Initialize GPTCache before starting Open Interpreter
2. Configure Open Interpreter to use the cached OpenAI adapter
3. GPTCache will automatically cache and reuse similar queries

## Cost Optimization Tips
1. Use expensive models (GPT-4, Claude Opus) with caching
2. Switch to cheaper models for non-cached queries
3. Cache persists between sessions - build up common query patterns
4. Semantic matching means slight variations still hit cache

## Note
Open Interpreter stores conversation history in `~/.cache/open-interpreter/` but this is for telemetry/contribution purposes, not for caching LLM responses. GPTCache provides the actual response caching functionality.