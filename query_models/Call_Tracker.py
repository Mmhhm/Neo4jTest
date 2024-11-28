from datetime import datetime

from generic_service import get_query_properties


class CallTracking():
    def __init__(self, driver):
        self.driver = driver

    def add_call(self, call_data):
        query = """
        MERGE (caller:Device {
                id: $caller_id, brand: $caller_brand, model: $caller_model,
                os: $caller_os, latitude: $caller_latitude, longitude: $caller_longitude,
                altitude_meters: $caller_altitude_meters, accuracy_meters: $caller_accuracy_meters
            })
        MERGE (receiver:Device {
                id: $receiver_id, brand: $receiver_brand, model: $receiver_model,
                os: $receiver_os, latitude: $receiver_latitude, longitude: $receiver_longitude,
                altitude_meters: $receiver_altitude_meters, accuracy_meters: $receiver_accuracy_meters
            })
        CREATE (caller)-[call:CONNECTED {
                from_device: $from_device, to_device: $to_device, method: $method,
                bluetooth_version: $bluetooth_version, signal_strength_dbm: $signal_strength_dbm,
                distance_meters: $distance_meters, duration_seconds: $duration_seconds,
                timestamp: $timestamp
        }]->(receiver)
        RETURN toString(call.timestamp) as timestamp
        """

        try:
            with self.driver.session() as session:
                result = session.run(query, get_query_properties(call_data))
                return result.single()['timestamp']
        except Exception as ex:
            print(f"Error occurred during neo4j session {ex}")
            return None


    def connected_by_bluetooth(self):
        query = """
        MATCH (start:Device)
        MATCH (end:Device)
        WHERE start <> end
        MATCH path = shortestPath((start)-[:CONNECTED*]->(end))
        WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
        WITH path, length(path) as pathLength
        ORDER BY pathLength DESC
        LIMIT 1
        RETURN length(path) as path_length
        """
        try:
            with self.driver.session() as session:
                result = session.run(query)
                return result.single()['path_length']
        except Exception as e:
            print(f"error occurred during noe4j session: {e}")
            return None


    def strong_signal_call(self):
        query = """
        MATCH (caller)-[r]->(receiver)
        WHERE r.signal_strength_dbm > -60
        RETURN caller.id as caller_id, receiver.id as receiver_id, r.signal_strength_dbm as signal_strength
        """

        with self.driver.session() as session:
            result = session.run(query)

            if result is not None:
                devices = []

                for record in result:
                    data = {
                        'caller_id': record.get('caller_id'),
                        'receiver_id': record.get('receiver_id'),
                        'signal_strength': record.get('signal_strength')
                    }
                    devices.append(data)

                return devices
            else:
                return None


    def connected_devices(self, device_id):
        query = """
        MATCH (caller{id: $device_id})-[]->(receiver)
        RETURN count(receiver) as connected_devices
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, {'device_id': device_id})
                return result.single()['connected_devices']
        except Exception as e:
            print(f"error occurred during noe4j session: {e}")
            return None


    def are_connected(self, device1_id, device2_id):
        query = """
        MATCH ({id: $device1_id})-[r1]-({id: $device2_id})
        RETURN count(r1) + count(r1) > 0 as is_connected
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, {'device1_id': device1_id, 'device2_id': device2_id})
                return result.single()['is_connected']
        except Exception as e:
            print(f"error occurred during noe4j session: {e}")
            return None

    def recent_calls(self, device_id):
        query = """
        MATCH ({id: $device_id})-[r]-()
        RETURN r.to_device as receiver, toString(r.timestamp) as timestamp ORDER BY r.timestamp descending
        """
        try:
            with self.driver.session() as session:
                calls = []
                result = session.run(query, {'device_id': device_id})
                for record in result:
                     calls.append(dict(record))
                return calls
        except Exception as e:
            print(f"error occurred during noe4j session: {e}")
            return None





