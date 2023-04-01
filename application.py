import threading
from queue import Queue

from twilio.rest import Client
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import time

from config import TWILIO
import doorbuilder
from doorbuilder import DoorBuilder

account_sid = TWILIO['SID']
auth_token = TWILIO['AUTH_TOKEN']
client = Client(account_sid, auth_token)
application = Flask(__name__)

builder_queue = Queue()
builder_lock = threading.Lock()

def initialize_builders(num_builders):
    for _ in range(num_builders):
        print('initializing Builder')
        builder = DoorBuilder(doorbuilder.startDriver())
        builder_queue.put(builder)

def handle_message(user_msg, to_number):
    
    builder = None
    while builder is None:
        with builder_lock:
            if not builder_queue.empty():
                builder = builder_queue.get()
                print(f"Assigned builder: {builder}")
            else:
                print("No available builders")
                break
        time.sleep(1)

    if 'help' in user_msg.lower():
        send_response(doorbuilder.help, to_number)
    elif 'more' in user_msg.lower():
        send_response(doorbuilder.more, to_number)
    else:
        url = builder.build(user_msg)
        send_response(url, to_number)
        builder.resetDriver()

    with builder_lock:
        builder_queue.put(builder)
        print(f"Released builder: {builder}")

@application.route("/bot", methods=['GET', 'POST'])
def bot():
    user_msg = request.values.get('Body')
    to_number = request.values.get('From')
    print(to_number)
    if user_msg:
        if 'abudsaysinitialize' in user_msg.lower():
            initialize_builders(3)
            return "Initialized Builders"

    threading.Thread(target=handle_message, args=(user_msg, to_number)).start()

    response = MessagingResponse()
    response.message('Processing your request')
    return "Bot Success", 200

@application.route("/", methods=['GET', 'POST'])
def home():
    return "Success", 200

def send_response(response, number):
    client.messages.create(
        messaging_service_sid=TWILIO['MSID'],
        body=response,
        to=number
    )

if __name__ == "__main__":
    num_builders = 3
    print('Ben is lovely')
    initialize_builders(num_builders)
    application.run(debug=True, host='0.0.0.0', port=5000)