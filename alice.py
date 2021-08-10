from py123mqtt import Messaging
from py123mqtt import Connection
import os
import threading

def send_periodic_message():
    alice.send_message(bob, 'hello Bob!')
    threading.Timer(5, send_periodic_message).start()

alice = Messaging(private_key=os.environ.get('PRIVATEKEY'), username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'))
alice.show_info()

bob = Connection('Bob Lee', 'Silly-Headrest-2013')
alice.establish_connection(bob)
send_periodic_message()
alice.loop_forever()