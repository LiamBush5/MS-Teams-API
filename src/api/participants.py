from api.graph_api import GraphAPI

async def get_segment_participants(graph_api: GraphAPI, call_record_id: str, session_id: str, segment_id: str):
    participants = await graph_api.get_segment_participants(call_record_id, session_id, segment_id)
    print(f"Received {len(participants)} participants for segment {segment_id}")
    return participants