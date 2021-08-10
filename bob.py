from py123mqtt import Messaging
from py123mqtt import Connection
import os
import threading

def send_periodic_message():
    bob.send_message(alice, 'hello Alice!')
    threading.Timer(5, send_periodic_message).start()

bob = Messaging(private_key=os.environ.get('PRIVATEKEY'), username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'))
bob.show_info()

alice = Connection('Alice Wonder', 'Old-Engine-6372')
bob.establish_connection(alice)
send_periodic_message()
bob.loop_forever()