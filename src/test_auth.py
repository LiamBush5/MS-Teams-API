import asyncio
from auth.auth_manager import AuthManager
from utils.config import load_config

async def main():
    config = load_config()
    auth_manager = AuthManager(config)

    try:
        token = await auth_manager.get_access_token()
        print("Successfully obtained access token:")
        print(token[:50] + "...") # Print first 50 characters of the token
    except Exception as e:
        print(f"Failed to obtain access token: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())