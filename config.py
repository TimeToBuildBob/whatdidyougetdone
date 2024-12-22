from pathlib import Path
import os
from platformdirs import user_config_dir

# Define app name and author for config directory
APP_NAME = "whatdidyougetdone"
APP_AUTHOR = "brayo"

def get_config_dir() -> Path:
    """Get the platform-specific config directory."""
    config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_github_token() -> str:
    """
    Get GitHub token from config file or environment.
    Updates config file if token is in environment.
    Exits if no token is found.
    """
    config_file = get_config_dir() / ".env"
    
    # Try reading from config file first
    if config_file.exists():
        with open(config_file) as f:
            for line in f:
                if line.startswith('GITHUB_TOKEN='):
                    return line.split('=')[1].strip()
    
    # Check environment variable
    token = os.getenv("GITHUB_TOKEN")
    if token:
        # Save to config file for future use
        with open(config_file, 'w') as f:
            f.write(f"GITHUB_TOKEN={token}\n")
        return token
    
    # No token found
    print("GitHub token not found!")
    print("Either:")
    print(f"1. Create {config_file} with GITHUB_TOKEN=your_token")
    print("2. Set GITHUB_TOKEN environment variable")
    print("\nYou can create a token at: https://github.com/settings/tokens")
    print("Required scopes: repo, read:user")
    exit(1)
