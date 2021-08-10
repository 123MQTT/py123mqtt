from py123mqtt import Messaging
from py123mqtt import Connection
import os
import threading

def send_periodic_message():
    bob.send_message(alice, 'hello Alice!')
    bob.send_message(charlie, 'hello Charlie!')
    threading.Timer(5, send_periodic_message).start()

# initialize messaging channels
bob = Messaging(private_key=os.environ.get('PRIVATEKEY'), username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'))
bob.show_info()

# add connections
alice = Connection('Alice Wonder', 'Old-Engine-6372')
charlie = Connection('Charlie Chaplin', 'Wordy-Motorboat-2966')

# establish secure connections
bob.establish_connection(alice)
bob.establish_connection(charlie)

# send periodic messages
send_periodic_message()

# loop forever
bob.loop_forever()