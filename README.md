# AI-Powered Pull Request Review Action 🔍🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub Actions Version](https://img.shields.io/github/v/release/pritom007/ai-pr-review)](https://github.com/pritom007/ai-pr-review/releases)
[![Build Status](https://github.com/pritom007/ai-pr-review/actions/workflows/test.yml/badge.svg)](https://github.com/pritom007/ai-pr-review/actions)
[![Issues](https://img.shields.io/github/issues/pritom007/ai-pr-review)](https://github.com/pritom007/ai-pr-review/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/pritom007/ai-pr-review)](https://github.com/pritom007/ai-pr-review/pulls)
[![Stars](https://img.shields.io/github/stars/pritom007/ai-pr-review)](https://github.com/pritom007/ai-pr-review/stargazers)

Automated code review for GitHub pull requests powered by large language models (LLMs). Supports OpenAI, Groq, Azure OpenAI, and any OpenAI-compatible API endpoint.

![PR Review Example](https://via.placeholder.com/800x400.png?text=AI+PR+Review+Demo+Output)

## Table of Contents

- [Features] (#features)

- [Supported Providers] (#supported-providers)

- [Quick Start] (#quick-start)

- [Configuration] (#configuration)

- [Example Output] (#example-output)

- [Roadmap] (#roadmap)

- [Troubleshooting] (#troubleshooting)

- [License] (#license)

## Features ✨

- **Smart Analysis:** Detect bugs, security issues, and optimization opportunities
- **Multi-LLM Support:** Works seamlessly with leading AI providers
- **Customizable Feedback:** Control review depth, creativity, and response length (To-Do)
- **Rich Markdown Formatting:** Clear, structured, and detailed review outputs
- **Enterprise Ready:** Dockerized with secure handling of secrets
- **Multi-language Support:** Reviews available in 100+ languages (Any language supported by the LLM provider)

## Supported Providers 🤖

| Provider     | Base URL                           | Models                                 |
|--------------|------------------------------------|----------------------------------------|
| OpenAI       | `https://api.openai.com/v1`        | `gpt-4`, `gpt-3.5-turbo`               |
| Groq         | `https://api.groq.com/openai/v1`   | `llama3-70b-8192`, `mixtral-8x7b-32768`|
| Azure OpenAI | Your Azure endpoint                | `gpt-4`, `gpt-35-turbo`                |
| Local/Custom | `http://localhost:port/v1`         | OpenAI-compatible                      |

## Quick Start 🚀

### 1. Set API Key Secret

In your GitHub repository:

```yaml
Settings → Secrets and variables → Actions → New repository secret
Name: GROQ_API_KEY  # or OPENAI_API_KEY
Value: your-api-key-here
```

### 2. Add Workflow File

Create `.github/workflows/pr-review.yml`:

```yaml
name: AI Code Review
on: [pull_request]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: pritom007/ai-pr-review@v1
        with:
          api-key: ${{ secrets.GROQ_API_KEY }}
          model-name: "llama3-70b-8192"
          base-url: "https://api.groq.com/openai/v1"
          temperature: "0.7"
          max-tokens: "1000"
          language: "English"
```

## Configuration ⚙️

| Parameter    | Required | Default                | Description                   |
|--------------|----------|------------------------|-------------------------------|
| api-key      | ✅       | -                      | Your LLM provider's API key   |
| model-name   | ✅       | -                      | Specific LLM model to use     |
| base-url     | ❌       | OpenAI endpoint        | API URL of your LLM provider  |
| temperature  | ❌       | 0.7                    | 0 (Precise) ↔ 2 (Creative)    |
| max-tokens   | ❌       | 1000                   | Limit of response length      |
| language     | ❌       | English                | Language for the review       |

### Advanced Usage

```yaml
with:
  system-prompt: "Act as a principal engineer at a leading tech company"
  review-focus: "security,performance,readability"
```

## Example Output 📝

```markdown
## AI Code Review Summary

### 🛠️ Code Quality
- ✅ **Good:** Consistent error handling across modules
- ⚠️ **Improvement:** Abstract repetitive validation logic into helper functions

### 🚨 Potential Issues
- 🔒 **Security:** Unsanitized inputs detected (`userProfile.js:82`)
- 🐞 **Bug Risk:** Possible null-pointer exception (`dataProcessor.js:45`)

### 🚀 Optimization
- ⚡ **Performance:** Implement caching for frequent `fetchUserData()` calls
- 📦 **Memory Efficiency:** Stream large datasets rather than fully loading them

### 📚 Documentation
- 📝 Add detailed JSDoc comments for public methods
- 📖 Update the README with new API usage examples
```

## Roadmap 🗺️

- [ ] Support for customizable prompt templates
- [ ] Enhanced security review capabilities
- [ ] Integration with additional code hosting platforms

## Troubleshooting 🛠️

### Common Errors

### 401 Unauthorized

- Ensure your secret key matches the configured workflow input

Test your API key:

```bash
curl -H "Authorization: Bearer $KEY" $BASE_URL/models
```

### Model Not Found

- Verify exact model ID and regional availability

## Long Response Times

- Lower `max-tokens` or switch to lighter models

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> **Important:** AI reviews should complement human judgment, not replace it. Always manually verify critical changes.
