from py123mqtt import Messaging
from py123mqtt import Connection
import os
import threading

def send_periodic_message():
    alice.send_message(bob, 'hello Bob!')
    alice.send_message(charlie, 'hello Charlie!')
    threading.Timer(5, send_periodic_message).start()

alice = Messaging(private_key=os.environ.get('PRIVATEKEY'), username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'))
alice.show_info()

# add connections
bob = Connection('Bob Lee', 'Silly-Headrest-2013')
charlie = Connection('Charlie Chaplin', 'Wordy-Motorboat-2966')

# establish secure connections
alice.establish_connection(bob)
alice.establish_connection(charlie)

# send periodic messages
send_periodic_message()

# loop forever
alice.loop_forever()