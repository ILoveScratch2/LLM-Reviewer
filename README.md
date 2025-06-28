### 1. Set API Key Secret

In your GitHub repository:

```yaml
Settings → Secrets and variables → Actions → New repository secret
Name: INPUT_API_KEY  # make sure this is the name of the secret
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
          api-key: ${{ secrets.INPUT_API_KEY }}
          model-name: "llama3-70b-8192"
          base-url: "https://api.groq.com/openai/v1"
          temperature: "0.7"
          max-tokens: "1000"
          language: "English"
```
Set the llm model api key in your github secrets as `INPUT_API_KEY`. Also make sure you gave `read` permission to the `contents` and `write` premission to the `pull-requests`.

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
(To be done)
## Example Output 📝

## .github/workflows 
### test.yml
- [LOW] [Code Quality] Line 1-31: The file name 'test.yml' might be misleading as it seems to be a workflow for AI PR review rather than a test. Consider renaming it to something more descriptive like 'ai-pr-review.yml'. 
```yml
name: AI PR Review
```
- [MEDIUM] [Security] Line 22: The 'github-token' is passed as an input to the 'ai-pr-review' action. Although it's using the 'secrets.GITHUB_TOKEN', ensure that the 'pritom007/ai-pr-review' action handles the token securely.
```yml
      - name: AI PR Review
        uses: pritom007/ai-pr-review@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```
- [MEDIUM] [Service boundaries] Line 20-30: The workflow uses an external action 'pritom007/ai-pr-review' which interacts with an external API 'https://api.groq.com/openai/v1'. This might introduce service boundary issues, such as dependency on the external API or potential data leaks.
```yml
      - name: AI PR Review
        uses: pritom007/ai-pr-review@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          repository: ${{ github.repository }}
          ref: ${{ github.event.ref }}
          api-key: ${{ secrets.API_KEY }}
          api-url: https://api.groq.com/openai/v1
```

- [HIGH] [Error handling] Line 19-30: There is no error handling mechanism in place for the 'ai-pr-review' action. Consider adding try-except blocks or error handling mechanisms to handle potential errors or exceptions raised by the action.
```yml
      - name: AI PR Review
        uses: pritom007/ai-pr-review@v1
        with:
          # ...

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
