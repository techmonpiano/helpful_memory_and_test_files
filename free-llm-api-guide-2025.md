# Free LLM API Guide 2025
*Last Updated: June 26, 2025*

A comprehensive guide to accessing free LLM APIs including Microsoft Phi-4, Codestral, Llama, and other open-source models.

## 📋 Table of Contents
- [Quick Comparison](#quick-comparison)
- [Top 3 Recommended Options](#top-3-recommended-options)
- [Additional Free Options](#additional-free-options)
- [Detailed Service Information](#detailed-service-information)
- [Important Considerations](#important-considerations)
- [Community Resources](#community-resources)
- [Source References](#source-references)

## 🚀 Quick Comparison

| Service | Models Available | Rate Limits | Verification | Direct URL |
|---------|-----------------|-------------|--------------|------------|
| **GitHub Models** | Phi-4, Codestral, Llama, GPT-4o | Varies by Copilot tier | GitHub account | [Access](https://github.com/marketplace/models) |
| **Groq** | Llama 3.3 70B, Llama 4 Scout | 14,400 req/day | Phone required | [Access](https://groq.com) |
| **OpenRouter** | Multiple Llama variants | 20 req/min (free) | Account required | [Access](https://openrouter.ai) |
| **Hugging Face** | Models <10GB | 1 req/sec | Account required | [Access](https://huggingface.co) |
| **Together AI** | Llama 3.3, FLUX | 0.3-10 RPM | Account required | [Access](https://www.together.ai) |
| **Cloudflare Workers AI** | Llama 3.1/3.2/3.3 | 10,000 neurons/day | CF account | [Access](https://ai.cloudflare.com) |

## 🏆 Top 3 Recommended Options

### 1. GitHub Models (Best Overall)
- **Direct Access**: https://github.com/marketplace/models
- **Documentation**: https://docs.github.com/en/github-models
- **Why Choose**: Most comprehensive model selection, integrated with GitHub ecosystem
- **Available Models**: Phi-4 (all variants), Codestral, Llama models, GPT-4o, Claude
- **Setup**: Create GitHub PAT with `models:read` permission

### 2. Groq (Fastest Inference)
- **Direct Access**: https://groq.com
- **Why Choose**: Known for extremely fast inference speeds
- **Available Models**: Llama 3.3 70B, Llama 3.1 8B, Llama 4 Scout/Maverick
- **Rate Limits**: ~14,400 requests/day, 6,000 tokens/minute

### 3. OpenRouter (Most Flexible)
- **Direct Access**: https://openrouter.ai
- **Why Choose**: Gateway to multiple providers, easy model switching
- **Available Models**: Multiple Llama variants (3.1, 3.2, 3.3, 4)
- **Rate Limits**: 20 req/min, 50 req/day (free); 1,000/day with $10 lifetime top-up

## 🔧 Detailed Service Information

### GitHub Models

**What is it?**
GitHub Models is a free AI model playground integrated directly into GitHub, providing access to leading AI models through a single API endpoint.

**Key Features:**
- Free for all GitHub users
- No additional sign-up required
- Models hosted on Azure infrastructure
- Integrated with GitHub Codespaces and Actions

**API Endpoint**: `https://models.inference.ai.azure.com`

**Quick Start Example:**
```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.inference.ai.azure.com"
model_name = "Phi-3-small-8k-instruct"
token = os.environ["GITHUB_TOKEN"]  # Your GitHub PAT

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="What is the capital of France?"),
    ],
    model=model_name,
)

print(response.choices[0].message.content)
```

**cURL Example:**
```bash
curl -X POST "https://models.inference.ai.azure.com/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "model": "Phi-3-small-8k-instruct"
  }'
```

**Source URLs:**
- Announcement: https://github.blog/changelog/2024-10-29-github-models-is-now-available-in-public-preview/
- API Documentation: https://github.blog/changelog/2025-05-15-github-models-api-now-available/

### Hugging Face Inference API

**Direct Access**: https://huggingface.co/pricing
**Documentation**: https://huggingface.co/docs/api-inference

**Free Tier Details:**
- Free monthly credits (amount varies)
- Limited to models smaller than 10GB
- Rate limits: 1 request/second, 500,000 tokens/minute

**Important Notes:**
- Users report sudden limit changes (March 2025)
- PRO users ($9/month) get $2 included credits
- Pay-as-you-go available after credits exhausted

**Source URLs:**
- Pricing: https://huggingface.co/docs/inference-providers/en/pricing
- Community Discussion: https://discuss.huggingface.co/t/api-limits-on-free-inference-api/57711

### Together AI

**Direct Access**: https://www.together.ai
**Documentation**: https://docs.together.ai

**Free Tier Limits:**
- DeepSeek R1: 0.3 requests per minute
- FLUX.1 [schnell]: 10 images/minute
- Llama 3.3 70B Instruct Turbo: 6 requests/minute

**Source URL**: https://docs.together.ai/docs/rate-limits

### Replicate

**Direct Access**: https://replicate.com
**Pricing**: https://replicate.com/pricing

**Details:**
- Some free usage initially before billing required
- API rate limits: 600 requests/minute for predictions
- Pay-as-you-go model after free trial
- Only pay for active processing time

### Perplexity

**Direct Access**: https://www.perplexity.ai
**API Documentation**: https://docs.perplexity.ai

**Free Tier:**
- 5 Pro searches per day
- Unlimited basic searches
- API requires payment (Pro subscribers get $5/month credit)

**Source URLs:**
- Rate Limits: https://docs.perplexity.ai/guides/usage-tiers
- Pricing: https://docs.perplexity.ai/guides/pricing

### Additional Options

**Cloudflare Workers AI**
- Direct Access: https://ai.cloudflare.com
- Free allocation: 10,000 neurons/day
- Supports Llama 3.1/3.2/3.3 models

**Google AI Studio (Gemini)**
- Direct Access: https://aistudio.google.com
- Free tier with rate limits
- Requires Google account

## ⚠️ Important Considerations

### Rate Limits and Restrictions
- All free tiers have strict rate limits
- Phone verification required for most services
- Context window often limited to 8K tokens
- Designed for experimentation, not production

### Data Privacy
- Some services use data for training outside EU/UK
- Check each provider's data usage policy
- Consider privacy implications for sensitive data

### Community Guidelines
From the community-maintained resource:
> "Please don't abuse these services, else we might lose them"

### Licensing
Many open-source models have specific licensing restrictions:
- Check commercial use restrictions
- Some prohibit training other models
- User count limitations may apply

## 📚 Community Resources

### Primary Resource
**GitHub Free LLM API Resources**
- URL: https://github.com/cheahjs/free-llm-api-resources
- Community-maintained list of legitimate free APIs
- Regularly updated with new services
- Excludes reverse-engineered or illegitimate services

### Related Communities
- **r/LocalLLaMA**: Active Reddit community for local LLM discussions
- **Hugging Face Forums**: https://discuss.huggingface.co
- **GitHub Discussions**: Various model repositories have active discussions

## 📖 Source References

### Research Sources
1. **GitHub Models Documentation**
   - Official Docs: https://docs.github.com/en/github-models
   - Marketplace: https://github.com/marketplace/models
   - Changelog: https://github.blog/changelog/

2. **API Comparison Articles**
   - "30+ Free and Open Source LLM APIs": https://apidog.com/blog/free-open-source-llm-apis/
   - "Top 8 Free and Paid APIs for Your LLM": https://www.analyticsvidhya.com/blog/2024/10/free-and-paid-apis/
   - "Best AI API's 2025 For Free": https://aimlapi.com/best-ai-apis-for-free

3. **Community Resources**
   - Free LLM API Resources: https://github.com/cheahjs/free-llm-api-resources
   - Awesome LLM: https://github.com/Hannibal046/Awesome-LLM
   - Open LLMs: https://github.com/eugeneyan/open-llms

4. **Service-Specific Documentation**
   - Together AI Docs: https://docs.together.ai
   - Replicate Docs: https://replicate.com/docs
   - Perplexity Docs: https://docs.perplexity.ai
   - Hugging Face Docs: https://huggingface.co/docs

## 🎯 Quick Start Recommendations

1. **For General Use**: Start with GitHub Models - comprehensive selection, easy setup
2. **For Speed**: Use Groq for fastest inference
3. **For Flexibility**: Try OpenRouter to access multiple providers
4. **For Small Models**: Hugging Face Inference API
5. **For Image Generation**: Together AI (FLUX models)

## 📝 Notes

- This guide compiled from web research on June 26, 2025
- Services and limits may change - always check official documentation
- Consider upgrading to paid tiers for production use
- Join community discussions for latest updates and user experiences

---

*Remember: These free services are provided for experimentation and learning. Please use them responsibly to ensure continued availability for the community.*