import aiohttp
from auth.auth_manager import AuthManager

class GraphAPI:
    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.base_url = "https://graph.microsoft.com/v1.0"

    async def _make_request(self, endpoint: str):
        access_token = await self.auth_manager.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{endpoint}", headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API request failed: {response.status}\nDetails: {error_text}")

    async def get_call_records(self):
        return await self._make_request("/communications/callRecords")

    async def get_call_record_sessions(self, call_record_id: str):
        return await self._make_request(f"/communications/callRecords/{call_record_id}/sessions")

    async def get_session_segments(self, call_record_id: str, session_id: str):
        return await self._make_request(f"/communications/callRecords/{call_record_id}/sessions/{session_id}/segments")

    async def get_segment_participants(self, call_record_id: str, session_id: str, segment_id: str):
        return await self._make_request(f"/communications/callRecords/{call_record_id}/sessions/{session_id}/segments/{segment_id}/participants")