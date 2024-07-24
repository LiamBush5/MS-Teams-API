import asyncio
import logging
import json
from auth.auth_manager import AuthManager
from api.graph_api import GraphAPI
from utils.config import load_config
from api.call_records import get_and_process_call_records
from api.sessions import get_call_sessions
from api.segments import get_session_segments
from api.participants import get_segment_participants

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    config = load_config()
    auth_manager = AuthManager(config)
    graph_api = GraphAPI(auth_manager)

    try:
        await auth_manager.get_access_token()
        logging.info("Successfully obtained access token")

        # Get recent calls
        recent_calls = await get_and_process_call_records(graph_api, days_ago=7)

        if recent_calls:
            first_call = recent_calls[0]
            call_record_id = first_call['id']

            # Get sessions for the call record
            sessions = await get_call_sessions(graph_api, call_record_id)

            for session in sessions:
                if isinstance(session, dict) and 'id' in session:
                    session_id = session['id']
                    print(f"Processing session: {session_id}")

                    # Get segments for the session
                    segments = await get_session_segments(graph_api, call_record_id, session_id)

                    if segments:
                        for segment in segments:
                            if isinstance(segment, dict) and 'id' in segment:
                                segment_id = segment['id']
                                print(f"Processing segment: {segment_id}")

                                # Get participants for the segment
                                try:
                                    participants = await get_segment_participants(graph_api, call_record_id, session_id, segment_id)
                                    print(json.dumps(participants, indent=2))
                                except Exception as e:
                                    print(f"Error fetching participants for segment {segment_id}: {str(e)}")
                            else:
                                print(f"Unexpected segment format: {segment}")
                    else:
                        print(f"No segments found for session {session_id}")
                else:
                    print(f"Unexpected session format: {session}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
