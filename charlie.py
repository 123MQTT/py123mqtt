from py123mqtt import Messaging
from py123mqtt import Connection
import os
import threading

def send_periodic_message():
    charlie.send_message(alice, 'hello Alice!')
    charlie.send_message(bob, 'hello Bob!')
    threading.Timer(5, send_periodic_message).start()

# initialize messaging channels
charlie = Messaging(private_key=os.environ.get('PRIVATEKEY'), username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'))
charlie.show_info()

# add connections
alice = Connection('Alice Wonder', 'Old-Engine-6372')
bob = Connection('Bob Lee', 'Silly-Headrest-2013')

# establish secure connections
charlie.establish_connection(alice)
charlie.establish_connection(bob)

# send periodic messages
send_periodic_message()

# loop forever
charlie.loop_forever()