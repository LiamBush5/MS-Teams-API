from api.graph_api import GraphAPI
import logging

async def get_call_sessions(graph_api: GraphAPI, call_record_id: str):
    sessions_response = await graph_api.get_call_record_sessions(call_record_id)
    if isinstance(sessions_response, dict) and 'value' in sessions_response:
        return sessions_response['value']
    else:
        logging.warning(f"Unexpected sessions response format for call {call_record_id}")
        return []