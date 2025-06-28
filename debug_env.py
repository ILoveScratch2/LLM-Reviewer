#!/usr/bin/env python3
"""
Debug script to check environment variables and API connectivity
"""
import os
import sys
import requests
from openai import OpenAI

def check_env_vars():
    """Check required environment variables"""
    print("=== Environment Variables ===")
    
    required_vars = [
        'GITHUB_TOKEN',
        'GITHUB_REPOSITORY', 
        'GITHUB_REF',
        'INPUT_API_KEY',
        'INPUT_MODEL_NAME',
        'INPUT_BASE_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'TOKEN' in var or 'KEY' in var:
                display_value = f"{'*' * 10}...{value[-4:]}" if len(value) > 4 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    return missing_vars

def test_github_api():
    """Test GitHub API connectivity"""
    print("\n=== GitHub API Test ===")
    
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    
    if not token or not repo:
        print("❌ Missing GitHub credentials")
        return False
    
    try:
        headers = {'Authorization': f'token {token}'}
        response = requests.get(f'https://api.github.com/repos/{repo}', headers=headers)
        
        if response.status_code == 200:
            print("✅ GitHub API connection successful")
            return True
        else:
            print(f"❌ GitHub API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ GitHub API connection failed: {e}")
        return False

def test_llm_api():
    """Test LLM API connectivity"""
    print("\n=== LLM API Test ===")
    
    api_key = os.getenv('INPUT_API_KEY')
    base_url = os.getenv('INPUT_BASE_URL', 'https://api.openai.com/v1')
    model_name = os.getenv('INPUT_MODEL_NAME', 'gpt-4')
    
    if not api_key:
        print("❌ Missing API key")
        return False
    
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("✅ LLM API connection successful")
        print(f"Model: {model_name}")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ LLM API connection failed: {e}")
        return False

def extract_pr_number():
    """Extract and validate PR number"""
    print("\n=== PR Number Extraction ===")
    
    github_ref = os.getenv('GITHUB_REF', '')
    print(f"GITHUB_REF: {github_ref}")
    
    try:
        if 'pull' in github_ref:
            pr_number = int(github_ref.split('/')[2])
            print(f"✅ Extracted PR number: {pr_number}")
            return pr_number
        else:
            # Try event path
            event_path = os.getenv('GITHUB_EVENT_PATH')
            if event_path and os.path.exists(event_path):
                import json
                with open(event_path, 'r') as f:
                    event_data = json.load(f)
                    pr_number = event_data.get('pull_request', {}).get('number')
                    if pr_number:
                        print(f"✅ Extracted PR number from event: {pr_number}")
                        return pr_number
            
            print("❌ Could not extract PR number")
            return None
            
    except Exception as e:
        print(f"❌ Error extracting PR number: {e}")
        return None

def main():
    print("🔍 AI PR Review Debug Tool")
    print("=" * 50)
    
    # Check environment variables
    missing_vars = check_env_vars()
    
    # Extract PR number
    pr_number = extract_pr_number()
    
    # Test APIs
    github_ok = test_github_api()
    llm_ok = test_llm_api()
    
    print("\n=== Summary ===")
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
    if not pr_number:
        print("❌ Could not determine PR number")
    if not github_ok:
        print("❌ GitHub API connection failed")
    if not llm_ok:
        print("❌ LLM API connection failed")
    
    if not missing_vars and pr_number and github_ok and llm_ok:
        print("✅ All checks passed! Ready to run AI PR review.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
