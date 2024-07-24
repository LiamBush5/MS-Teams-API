from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

def process_recent_calls(call_records_response: Dict[str, Any], days_ago: int = 7) -> List[Dict[Any, Any]]:
    current_time = datetime.utcnow()
    time_threshold = current_time - timedelta(days=days_ago)

    if not isinstance(call_records_response, dict):
        logging.error(f"Unexpected response type: {type(call_records_response)}")
        return []

    call_records = call_records_response.get('value', [])
    if not isinstance(call_records, list):
        logging.error(f"'value' is not a list: {type(call_records)}")
        return []

    recent_calls = []
    for record in call_records:
        if not isinstance(record, dict):
            logging.warning(f"Unexpected record type: {type(record)}")
            continue

        if 'startDateTime' in record:
            try:
                call_time = datetime.fromisoformat(record['startDateTime'].rstrip('Z'))
                if call_time >= time_threshold:
                    recent_calls.append(record)
            except ValueError:
                logging.warning(f"Invalid startDateTime format: {record['startDateTime']}")
        else:
            logging.warning(f"Call record missing startDateTime: {record}")

    return sorted(recent_calls, key=lambda x: x['startDateTime'], reverse=True)

def get_call_duration(call_record: Dict[str, Any]) -> timedelta:
    if 'startDateTime' in call_record and 'endDateTime' in call_record:
        start_time = datetime.fromisoformat(call_record['startDateTime'].rstrip('Z'))
        end_time = datetime.fromisoformat(call_record['endDateTime'].rstrip('Z'))
        return end_time - start_time
    else:
        logging.warning(f"Call record missing start or end time: {call_record}")
        return timedelta(0)

def print_call_summary(call_record: Dict[str, Any]):
    start_time = datetime.fromisoformat(call_record['startDateTime'].rstrip('Z'))
    duration = get_call_duration(call_record)

    print(f"Call ID: {call_record.get('id', 'N/A')}")
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}")
    print(f"Type: {call_record.get('type', 'N/A')}")
    print(f"Modalities: {', '.join(call_record.get('modalities', ['N/A']))}")

def print_session_summary(session: Dict[str, Any]):
    print(f"Session ID: {session.get('id', 'N/A')}")
    print(f"Modalities: {', '.join(session.get('modalities', ['N/A']))}")
    print(f"Start Time: {session.get('startDateTime', 'N/A')}")
    print(f"End Time: {session.get('endDateTime', 'N/A')}")

# def print_participant_summary(participant: Dict[str, Any]):
#     print(f"  Name: {participant.get('name', 'N/A')}")
#     identity = participant.get('identity', {}).get('user', {})
#     associated_identity = participant.get('associatedIdentity', {})
#     print(f"  Display Name: {identity.get('displayName', associated_identity.get('displayName', 'N/A'))}")
#     print(f"  User Principal Name: {associated_identity.get('userPrincipalName', 'N/A')}")
#     print(f"  User ID: {identity.get('id', associated_identity.get('id', 'N/A'))}")
#     print(f"  Tenant ID: {identity.get('tenantId', associated_identity.get('tenantId', 'N/A'))}")

#     user_agent = participant.get('userAgent', {})
#     print(f"  Platform: {user_agent.get('platform', 'N/A')}")
#     print(f"  Product Family: {user_agent.get('productFamily', 'N/A')}")

#     print(f"  CPU: {participant.get('cpuName', 'N/A')}")
#     print(f"  CPU Cores: {participant.get('cpuCoresCount', 'N/A')}")
#     print(f"  CPU Speed: {participant.get('cpuProcessorSpeedInMhz', 'N/A')} MHz")

def print_participant_summary(participant):
    print(f"  Name: {participant.get('name', 'N/A')}")

    identity = participant.get('identity', {}).get('user', {})
    associated_identity = participant.get('associatedIdentity', {})

    display_name = identity.get('displayName') or associated_identity.get('displayName', 'N/A')
    print(f"  Display Name: {display_name}")

    upn = associated_identity.get('userPrincipalName', 'N/A')
    print(f"  User Principal Name: {upn}")

    user_id = identity.get('id') or associated_identity.get('id', 'N/A')
    print(f"  User ID: {user_id}")

    tenant_id = identity.get('tenantId') or associated_identity.get('tenantId', 'N/A')
    print(f"  Tenant ID: {tenant_id}")

    user_agent = participant.get('userAgent', {})
    print(f"  Platform: {user_agent.get('platform', 'N/A')}")
    print(f"  Product Family: {user_agent.get('productFamily', 'N/A')}")

    print(f"  CPU: {participant.get('cpuName', 'N/A')}")
    print(f"  CPU Cores: {participant.get('cpuCoresCount', 'N/A')}")
    print(f"  CPU Speed: {participant.get('cpuProcessorSpeedInMhz', 'N/A')} MHz")