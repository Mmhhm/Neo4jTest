from datetime import datetime


def get_query_properties(call_data):
    try:
        caller = call_data['devices'][0]
        caller_location = call_data['devices'][0]['location']
        receiver = call_data['devices'][1]
        receiver_location = call_data['devices'][1]['location']
        call = call_data['interaction']
    except Exception as ex:
        return (f"Couldn't parse the json data: {str(ex)}")

    data = {
        "caller_id": caller["id"],
        "caller_brand": caller["brand"],
        "caller_model": caller["model"],
        "caller_os": caller["os"],
        "caller_latitude": caller_location["latitude"],
        "caller_longitude": caller_location["longitude"],
        "caller_altitude_meters": caller_location["altitude_meters"],
        "caller_accuracy_meters": caller_location["accuracy_meters"],
        "receiver_id": receiver["id"],
        "receiver_brand": receiver["brand"],
        "receiver_model": receiver["model"],
        "receiver_os": receiver["os"],
        "receiver_latitude": receiver_location["latitude"],
        "receiver_longitude": receiver_location["longitude"],
        "receiver_altitude_meters": receiver_location["altitude_meters"],
        "receiver_accuracy_meters": receiver_location["accuracy_meters"],
        "from_device": call["from_device"],
        "to_device": call["to_device"],
        "method": call["method"],
        "bluetooth_version": call["bluetooth_version"],
        "signal_strength_dbm": call["signal_strength_dbm"],
        "distance_meters": call["distance_meters"],
        "duration_seconds": call["duration_seconds"],
        "timestamp": datetime.strptime(call["timestamp"], '%Y-%m-%dT%H:%M:%S')
    }

    return data
