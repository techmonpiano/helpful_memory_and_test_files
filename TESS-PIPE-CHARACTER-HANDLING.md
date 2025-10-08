# Handling Pipe Character (|) in TESS API Key

## Issue Description
The TESS API key contains a pipe character (`|`) which can cause authentication failures when not handled properly in shell commands and HTTP requests.

**Example API Key**: `70709|bud2zaVgV3bAizp2MY96iD0TW2PKCwxFMLQKwv3a099e04ff`

## Common Problems

### 1. Shell Command Issues
The pipe character is a special character in shell that creates a pipeline between commands.

**❌ WRONG - Will fail:**
```bash
curl -H "Authorization: Bearer 70709|bud2zaVgV3bAizp2MY96iD0TW2PKCwxFMLQKwv3a099e04ff" ...
```

**✅ CORRECT - Use quotes:**
```bash
curl -H "Authorization: Bearer '70709|bud2zaVgV3bAizp2MY96iD0TW2PKCwxFMLQKwv3a099e04ff'" ...
```

### 2. Environment Variable Best Practice
Always use environment variables to avoid escaping issues:

```bash
# Set the environment variable
export TESS_API_KEY='70709|bud2zaVgV3bAizp2MY96iD0TW2PKCwxFMLQKwv3a099e04ff'

# Use it in commands
curl -H "Authorization: Bearer $TESS_API_KEY" ...
```

## Working Examples

### Node.js with dotenv
```javascript
// .env file
TESS_API_KEY=70709|bud2zaVgV3bAizp2MY96iD0TW2PKCwxFMLQKwv3a099e04ff

// JavaScript code
require('dotenv').config();
const apiKey = process.env.TESS_API_KEY; // Pipe character handled automatically

// In axios
axios.create({
  headers: {
    'Authorization': `Bearer ${apiKey}`
  }
});
```

### Direct Node.js
```javascript
// Store as string - no escaping needed
const apiKey = '70709|bud2zaVgV3bAizp2MY96iD0TW2PKCwxFMLQKwv3a099e04ff';

// Use in headers
const headers = {
  'Authorization': `Bearer ${apiKey}`,
  'Content-Type': 'application/json'
};
```

### TypeScript/Express
```typescript
// config/env.ts
export const config = {
  tess: {
    apiKey: process.env.TESS_API_KEY || '', // Loaded from .env
  }
};

// Using in service
this.client = axios.create({
  headers: {
    'Authorization': `Bearer ${config.tess.apiKey}`, // Template literal handles it
  }
});
```

## Testing Authentication

### Quick Test Script
```javascript
// test-auth.js
require('dotenv').config();
const axios = require('axios');

async function testAuth() {
  try {
    const response = await axios.get('https://tess.pareto.io/api/agents/3176', {
      headers: {
        'Authorization': `Bearer ${process.env.TESS_API_KEY}`,
        'Accept': 'application/json'
      }
    });
    console.log('✅ Authentication successful!');
    console.log('Agent:', response.data.title);
  } catch (error) {
    console.log('❌ Authentication failed:', error.response?.data || error.message);
  }
}

testAuth();
```

## Key Rules

1. **Always use environment variables** for API keys
2. **Use single quotes** in shell commands when directly passing the key
3. **Template literals** in JavaScript/TypeScript handle the pipe character correctly
4. **dotenv** automatically handles special characters when loading from .env files
5. **Never escape the pipe** with backslash - use proper quoting instead

## Common Error Messages

- `"message": "Unauthenticated."` - Usually means the pipe character was interpreted as a shell pipe
- `401 Unauthorized` - API key not properly included in Authorization header
- `Invalid API key` - Key might be truncated due to pipe character handling

## Working Endpoint Format

The correct TESS API endpoint format:
```
https://tess.pareto.io/api/agents/{agentId}/openai/chat/completions
```

With proper authorization:
```javascript
Authorization: Bearer 70709|bud2zaVgV3bAizp2MY96iD0TW2PKCwxFMLQKwv3a099e04ff
```

Remember: The pipe character is part of the API key and must be preserved exactly as-is!