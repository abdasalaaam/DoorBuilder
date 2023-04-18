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

def reset_builder(builder, reset_interval):
    while True:
        time.sleep(reset_interval)
        builder_found = False
        while not builder_found:
            with builder_lock:
                if builder in builder_queue.queue:
                    builder_queue.queue.remove(builder)
                    print(f"Removed builder {builder} for reset")
                    builder_found = True
                else:
                    print(f"Builder {builder} not found in queue for reset, waiting...")
            if not builder_found:
                time.sleep(1)  # Wait for 1 second before checking again

        builder.hardResetDriver()

        with builder_lock:
            builder_queue.put(builder)
            print(f"Added builder {builder} back to the queue after reset")

def initialize_builders(num_builders):
    reset_intervals = [5 * 60, 10 * 60]
    for i in range(num_builders):
        print('initializing Builder')
        builder = DoorBuilder(doorbuilder.startDriver())
        builder_queue.put(builder)
        reset_thread = threading.Thread(target=reset_builder, args=(builder, reset_intervals[i % len(reset_intervals)]))
        reset_thread.daemon = True
        reset_thread.start()
        send_response('Initialized Builder!', '+14406507000')

def handle_message(user_msg, to_number):
    if 'help' in user_msg.lower():
        send_response(doorbuilder.help, to_number)
        return
    elif 'more' in user_msg.lower():
        send_response(doorbuilder.more, to_number)
        return

    builder = None
    unavalBuilders = []

    while builder is None:
        with builder_lock:
            if not builder_queue.empty():
                builder = builder_queue.get()
                if builder.unavailable == True:
                    unavalBuilders.append(builder)
                    builder = None
                print(f"Assigned builder: {builder}")
            else:
                print("No available builders")
                break
        time.sleep(1)

    for b in unavalBuilders:
        builder_queue.put(b)

    try:
        url = builder.build(user_msg)
        send_response(url, to_number)
        builder.resetDriver()
    except:
        if builder == None:
            send_response('Please try again in a few seconds', to_number)
            return
        else:
            send_response('Builder error, please try again in a few minutes', to_number)
            builder.setUnavailable(True)

    with builder_lock:
        builder_queue.put(builder)
        print(f"Released builder: {builder}")

def send_response(response, number):
    client.messages.create(
        messaging_service_sid=TWILIO['MSID'],
        body=response,
        to=number
    )

@application.route("/bot", methods=['GET', 'POST'])
def bot():
    user_msg = request.values.get('Body')
    to_number = request.values.get('From')

    threading.Thread(target=handle_message, args=(user_msg, to_number)).start()

    response = MessagingResponse()
    response.message('Processing your request')
    return "Bot Success", 200

@application.route("/", methods=['GET', 'POST'])
def home():
    return "Success", 200

@application.before_first_request
def on_start():
    num_builders = 2
    print('Ben is lovely')
    threading.Thread(target=initialize_builders, args=(num_builders,)).start()
    

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80)