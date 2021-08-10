from py123mqtt import Messaging
from py123mqtt import Connection
import threading

def send_periodic_message():
    alice.send_message(bob, 'hello Bob!')
    threading.Timer(5, send_periodic_message).start()

alice = Messaging(private_key='ff746ad94861f073d07196d6c901b45f', username='Old-Engine-6372', password='0CewA5a1')
alice.show_info()

bob = Connection('Bob Lee', 'Silly-Headrest-2013')
alice.establish_connection(bob)
send_periodic_message()
alice.loop_forever()