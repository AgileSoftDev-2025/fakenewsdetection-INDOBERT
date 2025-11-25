"""
Test Hugging Face connection and model availability.
Run this script to verify your HF_TOKEN and model repo configuration.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def test_hf_config():
    """Test Hugging Face configuration."""
    print("=" * 60)
    print("HUGGING FACE CONFIGURATION TEST")
    print("=" * 60)

    # Check environment variables
    hf_repo = os.getenv("HF_MODEL_REPO")
    hf_token = os.getenv("HF_TOKEN")

    print("\n1. Environment Variables:")
    print(f"   HF_MODEL_REPO: {hf_repo if hf_repo else '❌ NOT SET'}")
    print(
        f"   HF_TOKEN: {'✓ SET (hidden)' if hf_token and hf_token != 'your_huggingface_token_here' else '❌ NOT SET'}"
    )

    if not hf_repo:
        print("\n❌ ERROR: HF_MODEL_REPO is not set in .env file")
        return False

    if not hf_token or hf_token == "your_huggingface_token_here":
        print("\n❌ ERROR: HF_TOKEN is not set properly in .env file")
        print("   Please get your token from: https://huggingface.co/settings/tokens")
        return False

    # Try to import huggingface_hub
    print("\n2. Checking huggingface-hub installation...")
    try:
        from huggingface_hub import HfApi, list_repo_files

        print("   ✓ huggingface-hub is installed")
    except ImportError:
        print("   ❌ huggingface-hub is not installed")
        print("   Run: pip install huggingface-hub")
        return False

    # Test authentication
    print("\n3. Testing authentication...")
    try:
        api = HfApi()
        user_info = api.whoami(token=hf_token)
        print(f"   ✓ Authenticated as: {user_info['name']}")
    except Exception as e:
        print(f"   ❌ Authentication failed: {e}")
        print("   Please check your HF_TOKEN")
        return False

    # Test repository access
    print(f"\n4. Testing access to repository: {hf_repo}")
    try:
        files = list_repo_files(hf_repo, token=hf_token)
        print(f"   ✓ Repository accessible")
        print(f"   ✓ Found {len(files)} files in repository")

        # Check for required model files
        required_files = [
            "config.json",
            "model.safetensors",
            "tokenizer.json",
            "vocab.txt",
        ]
        found_files = [f for f in required_files if f in files]
        print(f"\n   Required model files:")
        for file in required_files:
            status = "✓" if file in files else "❌"
            print(f"   {status} {file}")

        if len(found_files) == len(required_files):
            print(f"\n   ✓ All required files present!")
        else:
            print(
                f"\n   ⚠️  Missing {len(required_files) - len(found_files)} required files"
            )

    except Exception as e:
        print(f"   ❌ Cannot access repository: {e}")
        print("   Please check:")
        print("   - Repository name is correct")
        print("   - Repository exists on Hugging Face")
        print("   - Token has access to the repository (if private)")
        return False

    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nYou can now start the backend server.")
    print(
        "Model will be automatically downloaded on first startup if not present locally.\n"
    )
    return True


if __name__ == "__main__":
    success = test_hf_config()
    exit(0 if success else 1)
