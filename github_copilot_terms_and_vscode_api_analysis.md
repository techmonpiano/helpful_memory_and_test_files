# GitHub Copilot Terms & VSCode Language Model API Analysis

## Research Summary (January 2025)

### Question Investigated
Is using VSCode's Language Model API as an intermediary to access GitHub Copilot models a breach of GitHub's terms of service? Does one have to use VSCode specifically?

### Key Findings

**VSCode Language Model API is Officially Supported** ✅

The VSCode Language Model API is a **legitimate and official way** to access GitHub Copilot models. This is confirmed by:

1. **Official Microsoft Documentation**: VSCode's official API documentation explicitly covers using GitHub Copilot through the Language Model API
2. **GitHub Support**: GitHub officially supports and documents this integration path
3. **User Consent Model**: The API requires proper user consent, which aligns with GitHub's policies

### No VSCode Requirement Found

I did **not find any evidence** that using GitHub Copilot requires VSCode specifically. The terms and policies focus on:

- **User consent and authentication** (which VSCode's API handles properly)
- **Responsible usage** (rate limiting, appropriate use cases)
- **Developer compliance** with GitHub's acceptable use policies
- **Data privacy and security** protections

### Third-Party Integration Guidelines

The documentation shows that third-party extensions can legitimately use Copilot through VSCode's Language Model API, provided they:

1. **Obtain proper user consent** (handled by VSCode's authentication dialog)
2. **Follow GitHub's acceptable use policies**
3. **Implement defensive coding** (handle model unavailability gracefully)
4. **Comply with Microsoft AI guidelines** when publishing extensions

### Comparison: OpenCode vs KiloCode Approaches

**OpenCode Approach:**
- Direct GitHub Copilot API integration with OAuth authentication
- Uses GitHub device flow with client ID `Iv1.b507a08c87ecfe98`
- Exchanges device code for access token
- Converts GitHub token to Copilot API token via `https://api.github.com/copilot_internal/v2/token`

**KiloCode Approach:**
- Uses VSCode's Language Model API (`vscode.lm`) as intermediary
- Relies on VSCode's existing Copilot authentication and model access
- Simpler implementation since VSCode handles authentication complexity
- Model selection using `vendor: "copilot"` in selector

### GitHub Copilot Terms of Service Key Points

#### Extension Developer Policy Requirements
- Extensions must inform users of intended use cases, best practices, and limitations
- Must test to ensure outputs do not violate the Agreement
- Must provide feedback mechanisms and inform users of Extension capabilities
- Must request only necessary permissions
- Developers are "solely responsible for developing, operating, and maintaining all aspects of your Extensions"

#### Data Usage & Privacy
- Users can choose whether their prompts and Copilot's suggestions are collected and retained
- By default, GitHub does not use user data for AI model training
- GitHub does not use Copilot Business or Enterprise data to train its models

#### VSCode Language Model API Specific Rules
- Copilot's language models require consent from the user before an extension can use them
- Consent is implemented as an authentication dialog
- `selectChatModels` should be called as part of a user-initiated action
- Extensions must adhere to the "GitHub Copilot extensibility acceptable development and use policy"

#### Organizational Controls
- Organizations can set usage policies for Copilot Extensions
- Only organization admins can grant permissions for Copilot Extensions
- Users and organization owners must explicitly authorize permissions before installation

#### Current Limitations
- Custom API key feature is in preview and not available to Copilot Business or Enterprise users
- "Bringing your own model key" is not available for Business/Enterprise plans but will come later

### Conclusion

**Using VSCode's Language Model API to access Copilot models appears to be compliant** with GitHub's terms. The API is designed as an official integration path, not a workaround. The focus is on proper authentication, user consent, and responsible usage - all of which the VSCode Language Model API handles correctly.

Both OpenCode and KiloCode approaches appear to be legitimate:
- **OpenCode**: Direct API access (more complex but gives full control)
- **KiloCode**: VSCode API intermediary (simpler and officially supported)

### Recommendations

1. **For new projects**: VSCode Language Model API approach (KiloCode style) is simpler and officially supported
2. **For existing direct API integrations**: Continue using direct approach (OpenCode style) as it's also legitimate
3. **For enterprise/business**: Be aware of current limitations around custom API keys
4. **For compliance**: Ensure proper user consent, responsible usage, and adherence to GitHub's acceptable use policies

### Sources Referenced
- GitHub Copilot Extension Developer Policy
- VSCode Language Model API Documentation
- GitHub Copilot Terms of Service
- Microsoft AI Tools and Practices Guidelines
- GitHub Copilot Trust Center

## GitHub Models Marketplace - Separate Terms & Policies

### GitHub Models vs GitHub Copilot - Key Differences

**GitHub Models** is a separate marketplace service that allows developers to "learn, try, and test artificial intelligence models on GitHub.com" through the GitHub Marketplace.

**Key Distinctions:**

1. **Separate Terms of Service**
   - GitHub Models: Governed by "GitHub Terms for Additional Products and Features"
   - Usage subject to "the terms of the company hosting the model and the model license"
   - Separate from GitHub Copilot's terms

2. **Different Purpose & Access**
   - **GitHub Models**: Marketplace for accessing various AI models via API
   - **GitHub Copilot**: Integrated development assistant using multiple AI models for coding tasks
   - Models available include: GPT-4.1, GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, etc.

3. **API Access Method**
   - GitHub Models: Uses Azure Inference API (swapping models = changing model name)
   - Code snippets provided in JavaScript, Python, and REST
   - Integration via Azure AI Inference SDK

4. **Rate Limits & Pricing**
   - GitHub Models: Rate limited by requests per minute, daily requests, tokens per request, concurrent requests
   - Free tier available with rate limits
   - GitHub Copilot: Premium request system ($0.04 per premium request beyond allowance)

5. **Model Availability**
   - GitHub Models: Direct API access to individual models
   - GitHub Copilot: Integrated multi-model experience with base model (GPT-4.1) + premium models

### GitHub Copilot Premium Request System

**Premium Request Allowances:**
- Copilot Pro ($20/month): 300 monthly premium requests
- Copilot Business: 300 monthly premium requests  
- Copilot Enterprise: 1,000 monthly premium requests
- Additional requests: $0.04 USD per request

**Base vs Premium Models:**
- **Base Model**: GPT-4.1 (unlimited usage)
- **Premium Models**: Claude 3.5 Sonnet, Gemini 1.5 Pro, OpenAI o1-preview/o1-mini

### Terms Summary

**GitHub Models** has **separate terms and acceptable use policies** from GitHub Copilot:
- Governed by GitHub Terms for Additional Products and Features
- Subject to individual model provider terms (OpenAI, Anthropic, Google, etc.)
- Uses Azure hosting infrastructure with separate rate limits
- Marketplace-based access model

### GitHub Models Free Plan - Business Use Restrictions

**Critical Limitations for Business Use:**

1. **Production Use Prohibited**
   - Free tier explicitly "not designed for production use cases"
   - Limited to "learning, experimentation and proof-of-concept activities"
   - Operates under GitHub's pre-release terms

2. **Rate Limits**
   - Requests per minute/day restrictions
   - Limited tokens per request
   - Restricted concurrent requests
   - Mandatory content filters (cannot be disabled)

3. **Scaling Requirements**
   - For commercial/production use, must either:
     - Opt in to paid usage through GitHub Models billing
     - Use "Bring Your Own Key" (BYOK) with Azure/OpenAI accounts
     - Provision resources directly from Azure

4. **Business Use Implications**
   - Free tier may be used for business experimentation/prototyping
   - **Cannot be used for production business applications**
   - No guarantee of service availability or uptime
   - Content mistakes are expected ("you are experimenting with AI")

**Recommendation**: Businesses should consider "Azure AI or a paid service" for production use where content filters can be configured to meet specific requirements.

### Additional GitHub Models Findings & Updates

#### Recent Service Evolution (June 2025)
- **Pay-as-you-go billing**: Now available through GitHub account
- **Bring Your Own Key (BYOK)**: Two flexible paths to scale beyond free tier
- **Production-ready inference**: Access to higher-capacity, enterprise-grade model usage
- **Expanded model availability**: DeepSeek, Meta, Microsoft, and OpenAI models with production-grade rate limits

#### Governance Structure
- **Pre-release Terms**: Service operates under GitHub's Pre-release Terms
- **Multi-layered Terms**: Subject to GitHub Terms for Additional Products and Features + individual model provider terms + model licenses
- **Azure Integration**: For scaling, must provision resources from Azure account (not GitHub PAT authentication)

#### Rate Limiting Details
- **Free tier design**: "Rate limits are intended to help you get started with experimentation"
- **Scaling trigger**: "When you are ready to move beyond the free offering" - implies free tier is temporary/limited
- **Authentication change**: Production scaling requires Azure authentication instead of GitHub personal access token

#### Business Use Clarification
**Free Tier Business Use Status:**
- **Experimentation**: ✅ Allowed for business prototyping and proof-of-concept
- **Commercial Development**: ⚠️ Limited to non-production development activities
- **Production Deployment**: ❌ Explicitly prohibited - must upgrade to paid tier
- **Content Filtering**: ❌ Cannot be disabled on free tier (may not meet business requirements)

#### Cost Structure for Business Use
- **Free Tier**: Rate-limited experimentation only
- **Paid Usage**: Billing for all usage once opted in (no hybrid free/paid model)
- **BYOK Option**: Use existing Azure/OpenAI accounts for cost control
- **Enterprise Features**: Higher-capacity, enterprise-grade model usage available

#### Risk Considerations for Businesses
1. **Service Availability**: No SLA guarantees on free tier
2. **Content Mistakes**: GitHub explicitly warns "content mistakes are possible"
3. **Mandatory Filters**: Cannot customize content filtering for business needs
4. **Data Privacy**: Subject to multiple providers' terms (GitHub + model providers)
5. **Scalability**: Must migrate authentication/billing when moving to production

#### Compliance & Legal Considerations
- **Multiple Jurisdictions**: Subject to terms from GitHub, Microsoft (Azure), and individual model providers
- **Export Controls**: May be subject to GitHub's trade control policies
- **Data Residency**: Unclear where data processing occurs (likely Azure regions)
- **Audit Trail**: Limited visibility into usage patterns on free tier

#### Competitive Comparison
**GitHub Models vs Direct Provider Access:**
- **GitHub Models**: Simplified access but limited customization and additional terms layer
- **Direct Provider**: Full control but requires individual provider relationships
- **VSCode LM API**: Intermediate option with GitHub integration but Copilot-focused

**Key Insight**: GitHub Models appears designed as an "evaluation-to-production" funnel, where businesses are expected to graduate from free experimentation to paid production use, rather than a permanent free business solution.

### GitHub Models - Competitive Use & Model Training Restrictions

#### GitHub Models' Own Terms
**Limited Direct Restrictions**: GitHub's Terms for Additional Products and Features only briefly address GitHub Models:
- States usage is "subject to the terms of the company hosting the model and the model license"
- No explicit GitHub-specific restrictions on competitive model development found

#### Underlying Provider Restrictions (Critical Finding)
**Layered Terms Structure**: Since GitHub Models usage depends on underlying providers, restrictions vary by model:

**OpenAI Models via GitHub Models:**
- Subject to OpenAI's terms: "Use Output to develop models that compete with OpenAI" is prohibited
- Applies to original user generating the data (not downstream recipients)
- Exception for business terms: Limited permission for embeddings/classifiers and fine-tuning

**Azure OpenAI Models via GitHub Models:**
- **Critical Difference**: Azure OpenAI operates under Microsoft's terms
- **Does NOT appear to have** the same competing model restrictions as direct OpenAI API
- Training data "not used to train, retrain, or improve any Microsoft or third party base models"

**Other Providers (Anthropic, Google, Meta):**
- Each has individual terms and restrictions
- Anthropic prohibits using outputs to "train an AI model (e.g., 'model scraping')"

#### Industry Pattern - Competitive Training Restrictions
**Widespread Practice**: Multiple providers prohibit competitive model training:
- **Purpose**: Prevent IP theft and competitive advantage extraction
- **Scope**: Adobe, Aleph Alpha, Perplexity have similar restrictions
- **Enforcement**: OpenAI reportedly suspended ByteDance's account for violations

#### Practical Implications for GitHub Models Users
1. **Model-Specific Restrictions**: Depends entirely on which model you access through GitHub Models
2. **Azure Advantage**: Models accessed via Azure infrastructure may have fewer restrictions
3. **Ambiguous Interpretation**: What constitutes "competing models" remains legally unclear
4. **Data Security**: GitHub Models guarantees data "never leveraged for training" on their infrastructure

#### Risk Assessment for Competitive Use
**High Risk**: Using OpenAI models via GitHub Models for competitive model development
**Lower Risk**: Using Azure OpenAI models via GitHub Models (different terms structure)
**Unknown Risk**: Other providers' models - would need individual terms review
**Safe**: Using GitHub Models outputs for non-competitive purposes (embeddings, classifiers, etc.)

**Recommendation**: Review specific model provider terms before using GitHub Models outputs for any model training or development purposes, as restrictions are provider-specific rather than GitHub-imposed.

### GitHub Copilot - Competitive Use & Model Training Restrictions

#### GitHub Copilot Extension Developer Policy Restrictions

**Reverse Engineering**: Explicitly prohibited for extension developers:
- "Attempt to reverse engineer or otherwise derive source code, trade secrets, or know-how of the Platform" is forbidden

**General Framework**:
- GitHub reserves "right to develop, acquire, license, market, promote or distribute products, software or technologies that may compete with your Extensions"
- Usage governed by GitHub's Acceptable Use Policies
- Extensions must comply with GitHub Terms of Service including Acceptable Use Policy

#### Data Usage & Training Restrictions by Subscription Type

**Business & Enterprise Users:**
- GitHub does **NOT** use Copilot Business or Enterprise data to train models
- Data protection guaranteed for business/enterprise subscriptions

**Individual Users (Pro/Free):**
- **Free Users**: Data may be used for AI model training "where permitted and if you allow in your settings"
- **Pro Users**: Can opt-out of sharing prompts with GitHub (otherwise used to "finetune GitHub's foundational model")
- **Default Protection**: By default, GitHub does not use data for AI model training

#### Key Competitive Use Findings

**What GitHub Copilot Terms DON'T Explicitly Prohibit:**
- No explicit restriction found on using Copilot outputs to train competing models
- No direct prohibition on competitive AI model development using Copilot suggestions
- No specific terms preventing use of Copilot for other LLM development

**What GitHub Copilot Terms DO Restrict:**
- **Reverse engineering** the Copilot platform itself
- **Extension development** that violates acceptable use policies
- **Unpublished API usage**
- **Misleading users** about extension functionality

#### Training Data Sources

**Copilot Training Data**: 
- Trained on "natural language text and source code from publicly available sources"
- Includes "code in public repositories on GitHub"
- Uses models developed by GitHub, OpenAI, and Microsoft

#### Risk Assessment for Competitive Use

**Lower Risk Activities:**
- Using Copilot suggestions in competitive AI projects (no explicit prohibition found)
- Incorporating Copilot-generated code into other AI systems
- Learning from Copilot outputs for competitive development

**Higher Risk Activities:**
- Reverse engineering the Copilot platform/models
- Developing extensions that mislead users
- Using unpublished APIs

**Data Usage Risk by Plan:**
- **Business/Enterprise**: Low risk (data not used for training)
- **Individual Pro**: Medium risk (can opt-out of data sharing)
- **Individual Free**: Higher risk (data may be used for training if allowed)

#### Comparison with Other Services

**GitHub Copilot vs OpenAI Direct**: 
- Copilot appears to have **fewer explicit competitive restrictions** than direct OpenAI API
- OpenAI directly prohibits using outputs to "develop models that compete with OpenAI"
- Copilot terms focus more on platform protection than output usage restrictions

**Key Insight**: GitHub Copilot's terms appear more permissive regarding competitive use of outputs compared to direct OpenAI API or GitHub Models (which inherit provider restrictions). The main restrictions focus on platform protection rather than output usage limitations.

**Important Note**: Terms documents were not fully accessible for complete analysis - this assessment is based on available policy summaries. For definitive guidance, review complete GitHub Copilot Product Specific Terms directly.

**GitHub Copilot** operates under its own extension developer policy and product-specific terms, with integrated multi-model access and premium request billing.

### Conclusion Update

Both GitHub Models and GitHub Copilot provide legitimate access to AI models, but through different frameworks:
- **GitHub Models**: Direct API marketplace access with per-model terms
- **GitHub Copilot**: Integrated development experience with unified billing
- **VSCode Language Model API**: Official intermediary for Copilot access (as analyzed above)

All three approaches appear to be compliant with their respective terms of service when used appropriately.

*Research conducted: January 2025*