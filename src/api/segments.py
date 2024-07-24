from api.graph_api import GraphAPI

async def get_session_segments(graph_api: GraphAPI, call_record_id: str, session_id: str):
    segments = await graph_api.get_session_segments(call_record_id, session_id)
    return segments