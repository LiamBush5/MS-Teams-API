import aiohttp
from utils.config import Config

class AuthManager:
    def __init__(self, config: Config):
        self.config = config
        self.token_url = f"https://login.microsoftonline.com/{config.tenant_id}/oauth2/v2.0/token"

    async def get_access_token(self):
        async with aiohttp.ClientSession() as session:
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.config.client_id,
                'client_secret': self.config.client_secret,
                'scope': 'https://graph.microsoft.com/.default'
            }
            async with session.post(self.token_url, data=data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    return token_data['access_token']
                else:
                    error_text = await response.text()
                    print(f"Failed to obtain access token. Status: {response.status}")
                    print(f"Error details: {error_text}")
                    raise Exception(f"Failed to obtain access token: {response.status}")