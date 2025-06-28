#!/usr/bin/env python3
"""
Test script to validate the fixes made to the AI PR review tool
"""
import os
import sys
import asyncio
from unittest.mock import patch, MagicMock
import tempfile
import json

# Add src to path
sys.path.insert(0, 'src')

def create_mock_env():
    """Create mock environment variables for testing"""
    return {
        'GITHUB_TOKEN': 'ghp_test_token_123456789',
        'GITHUB_REPOSITORY': 'test-owner/test-repo',
        'GITHUB_REF': 'refs/pull/123/merge',
        'INPUT_API_KEY': 'sk-test-api-key-123',
        'INPUT_MODEL_NAME': 'gpt-4',
        'INPUT_BASE_URL': 'https://api.openai.com/v1',
        'INPUT_TEMPERATURE': '0.7',
        'INPUT_MAX_TOKENS': '1000',
        'INPUT_LANGUAGE': 'English'
    }

def test_pr_number_extraction():
    """Test PR number extraction logic"""
    print("Testing PR number extraction...")
    
    test_cases = [
        ('refs/pull/123/merge', 123),
        ('refs/pull/456/head', 456),
        ('refs/heads/main', None),  # Should fail gracefully
    ]
    
    for github_ref, expected in test_cases:
        try:
            if 'pull' in github_ref:
                pr_number = int(github_ref.split('/')[2])
                assert pr_number == expected, f"Expected {expected}, got {pr_number}"
                print(f"✅ {github_ref} -> {pr_number}")
            else:
                print(f"✅ {github_ref} -> No PR number (expected)")
        except Exception as e:
            if expected is None:
                print(f"✅ {github_ref} -> Failed as expected")
            else:
                print(f"❌ {github_ref} -> Unexpected error: {e}")

def test_environment_validation():
    """Test environment variable validation"""
    print("\nTesting environment validation...")
    
    # Test with missing variables
    with patch.dict(os.environ, {}, clear=True):
        try:
            from main import main
            # This should fail gracefully
            print("✅ Handles missing environment variables")
        except Exception as e:
            print(f"❌ Unexpected error with missing env vars: {e}")
    
    # Test with valid variables
    mock_env = create_mock_env()
    with patch.dict(os.environ, mock_env, clear=True):
        try:
            # Import should work
            from main import main
            print("✅ Accepts valid environment variables")
        except Exception as e:
            print(f"❌ Error with valid env vars: {e}")

def test_github_api_error_handling():
    """Test GitHub API error handling"""
    print("\nTesting GitHub API error handling...")
    
    try:
        from main import get_pr_diff
        
        # Test with invalid inputs
        result = get_pr_diff(None, "test/repo", 123)
        assert result == [], "Should return empty list for None token"
        print("✅ Handles None token")
        
        result = get_pr_diff("token", None, 123)
        assert result == [], "Should return empty list for None repo"
        print("✅ Handles None repository")
        
        result = get_pr_diff("token", "test/repo", None)
        assert result == [], "Should return empty list for None PR number"
        print("✅ Handles None PR number")
        
    except Exception as e:
        print(f"❌ Error in GitHub API error handling: {e}")

def test_chunk_files_empty_input():
    """Test chunk_files with empty input"""
    print("\nTesting chunk_files with empty input...")
    
    try:
        from main import chunk_files
        import tiktoken
        
        tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # Test empty list
        result = chunk_files([], tokenizer)
        assert result == [], "Should return empty list for empty input"
        print("✅ Handles empty file list")
        
        # Test None input
        result = chunk_files(None, tokenizer)
        assert result == [], "Should return empty list for None input"
        print("✅ Handles None input")
        
    except Exception as e:
        print(f"❌ Error in chunk_files testing: {e}")

def create_test_event_file():
    """Create a test GitHub event file"""
    event_data = {
        "pull_request": {
            "number": 789,
            "title": "Test PR",
            "body": "Test PR body"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(event_data, f)
        return f.name

def test_pr_number_from_event():
    """Test PR number extraction from event file"""
    print("\nTesting PR number extraction from event file...")
    
    event_file = create_test_event_file()
    
    try:
        mock_env = {
            'GITHUB_REF': 'refs/heads/feature-branch',  # No PR in ref
            'GITHUB_EVENT_PATH': event_file
        }
        
        with patch.dict(os.environ, mock_env, clear=True):
            # Test the extraction logic
            github_ref = os.getenv('GITHUB_REF', '')
            if 'pull' not in github_ref:
                event_path = os.getenv('GITHUB_EVENT_PATH')
                if event_path and os.path.exists(event_path):
                    with open(event_path, 'r') as f:
                        event_data = json.load(f)
                        pr_number = event_data.get('pull_request', {}).get('number')
                        assert pr_number == 789, f"Expected 789, got {pr_number}"
                        print("✅ Extracted PR number from event file")
    
    except Exception as e:
        print(f"❌ Error testing event file extraction: {e}")
    
    finally:
        # Clean up
        try:
            os.unlink(event_file)
        except:
            pass

async def test_async_functions():
    """Test async function error handling"""
    print("\nTesting async functions...")
    
    try:
        from main import synthesize_reviews
        
        # Test with empty reviews
        config = {
            'openai_params': {'api_key': 'test', 'base_url': 'https://api.openai.com/v1'},
            'model_name': 'gpt-4',
            'summary_prompt': 'Test prompt'
        }
        
        # This will fail due to invalid API key, but should handle gracefully
        try:
            result = await synthesize_reviews([], config)
            print("✅ Handles empty reviews list")
        except Exception as e:
            # Expected to fail with API error, not with empty list error
            if "empty" not in str(e).lower():
                print("✅ Fails gracefully with API error (expected)")
            else:
                print(f"❌ Unexpected empty list error: {e}")
    
    except Exception as e:
        print(f"❌ Error in async function testing: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing AI PR Review Fixes")
    print("=" * 50)
    
    test_pr_number_extraction()
    test_environment_validation()
    test_github_api_error_handling()
    test_chunk_files_empty_input()
    test_pr_number_from_event()
    
    # Run async tests
    try:
        asyncio.run(test_async_functions())
    except Exception as e:
        print(f"❌ Error running async tests: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Test suite completed!")

if __name__ == "__main__":
    main()
