from flask import Blueprint, jsonify, request
from main_service.init_db import neo4j_driver
from query_models.Call_Tracker import CallTracking


phone_blueprint = Blueprint('calls', __name__)

@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   print(request.json)
   data = request.get_json()

   try:
      session = CallTracking(neo4j_driver)
      result = session.add_call(data)
      return jsonify({"success": f"timestamp: {result}"}), 201
   except Exception as ex:
      print(f"Error occurred in ")
      return jsonify({'Error': 'internal server error'}), 500


@phone_blueprint.route("/api/phone_tracker/bluetooth_connected", methods=['GET'])
def get_bluetooth_connected_devices():
   try:
      session = CallTracking(neo4j_driver)
      result = session.connected_by_bluetooth()

      if result is not None:
         return jsonify({"success": f"result: {result}"}), 200
      else:
         return jsonify({'message': 'no matching records found'})

   except Exception as e:
      print(f"Error occurred in /api/phone_tracker/bluetooth_connected {e}")
      return jsonify({'Error': 'internal server error'}), 500


@phone_blueprint.route("/api/phone_tracker/strong_signal", methods=['GET'])
def get_strong_signal_calls():
   try:
      session = CallTracking(neo4j_driver)
      result = session.strong_signal_call()

      if result is not None:
         return jsonify({"success": f"result: {result}"}), 200
      else:
         return jsonify({'message': 'no matching records found'})

   except Exception as ex:
      print(f"Error occurred in /api/phone_tracker/strong_signal: {ex}")
      return jsonify({'Error': 'internal server error'}), 500


@phone_blueprint.route("/api/phone_tracker/connected/<device_id>", methods=['GET'])
def get_connected_devices(device_id):
   session = CallTracking(neo4j_driver)
   try:
      result = session.connected_devices(device_id)
      if result is not None:
         return jsonify({"success": f"result: {result}"}), 200
      else:
         return jsonify({'message': f'no matching records found {result}'}), 400
   except Exception as ex:
      print(f'/api/phone_tracker/connected/<device_id> error occurred {ex} ')
      return jsonify({'Error': 'internal server error'}), 500


@phone_blueprint.route("/api/phone_tracker/are_connected", methods=['GET'])
def are_connected():
   device1_id = request.args.get('device_1')
   device2_id = request.args.get('device_2')

   session = CallTracking(neo4j_driver)
   try:
      result = session.are_connected(device1_id, device2_id)
      return jsonify({"success": f"result: {result}"}), 200
   except Exception as e:
      print(f"/api/phone_tracker/are_connected error occurred {e}")
      return jsonify({'Error': 'internal server error'}), 500


@phone_blueprint.route("/api/phone_tracker/ordered_by_timestamp/<device_id>", methods=['GET'])
def get_ordered_call(device_id):
   session = CallTracking(neo4j_driver)
   try:
      result = session.recent_calls(device_id)
      return jsonify({"success": f"result: {result}"}), 200
   except Exception as e:
      print(f"/api/phone_tracker/ordered_by_timestamp/<device_id> error occurred {e}")
      return jsonify({'Error': 'internal server error'}), 500






