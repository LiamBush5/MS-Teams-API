from api.graph_api import GraphAPI
from utils.call_processor import process_recent_calls

async def get_and_process_call_records(graph_api: GraphAPI, days_ago: int = 7):
    call_records_response = await graph_api.get_call_records()
    recent_calls = process_recent_calls(call_records_response, days_ago=days_ago)
    return recent_calls