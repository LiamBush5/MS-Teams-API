import asyncio
import argparse
import logging
import json
from auth.auth_manager import AuthManager
from api.graph_api import GraphAPI
from utils.config import load_config
from api.call_records import get_and_process_call_records
from api.sessions import get_call_sessions
from utils.call_processor import print_call_summary, print_session_summary, print_participant_summary
from datetime import datetime, timedelta


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Fetch and display call records from Microsoft Graph API")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back for call records")
    parser.add_argument("--limit", type=int, default=5, help="Limit the number of call records to process")
    parser.add_argument("--level", choices=['basic', 'detailed', 'full', 'raw'], default='basic',
                        help="Level of detail to print (basic, detailed, full, or raw)")
    parser.add_argument("--show-sessions", action="store_true", help="Show session information for each call")
    return parser.parse_args()

async def fetch_raw_data(graph_api, days_ago):
    calls = await get_and_process_call_records(graph_api, days_ago=days_ago, raw=True)
    return calls

async def main():
    args = parse_arguments()
    config = load_config()
    auth_manager = AuthManager(config)
    graph_api = GraphAPI(auth_manager)

    try:
        await auth_manager.get_access_token()
        logging.info("Successfully obtained access token")

        if args.level == 'raw':
            raw_calls = await fetch_raw_data(graph_api, days_ago=args.days)
            print(json.dumps(raw_calls, indent=2))
            return

        recent_calls = await get_and_process_call_records(graph_api, days_ago=args.days)
        limited_calls = recent_calls[:args.limit]
        logging.info(f"Found {len(recent_calls)} calls in the last {args.days} days")
        logging.info(f"Displaying information for up to {args.limit} calls:")

        for call in limited_calls:
            call_record_id = call['id']
            print("\n" + "="*50)
            print(f"Call Record ID: {call_record_id}")

            if args.level in ['detailed', 'full']:
                print_call_summary(call)

            if args.show_sessions and args.level in ['detailed', 'full']:
                try:
                    sessions = await get_call_sessions(graph_api, call_record_id)
                    print(f"\nSessions: {len(sessions)}")
                    for session in sessions:
                        if isinstance(session, dict) and 'id' in session:
                            if args.level == 'full':
                                print("\n" + "-"*40)
                                print_session_summary(session)
                            caller = session.get('caller', {})
                            if caller:
                                print("Participant:")
                                print_participant_summary(caller)
                            callee = session.get('callee', {})
                            if callee:
                                print("Callee:")
                                print_participant_summary(callee)
                        else:
                            logging.warning(f"Unexpected session format for call {call_record_id}: {session}")
                except Exception as e:
                    logging.error(f"Error fetching sessions for call record {call_record_id}: {str(e)}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

