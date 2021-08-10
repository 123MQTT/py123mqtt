from py123mqtt import Messaging
from py123mqtt import Connection
import threading

def send_periodic_message():
    bob.send_message(alice, 'hello Alice!')
    threading.Timer(5, send_periodic_message).start()

bob = Messaging(private_key='bb3f488769037d24358f8060111b76fd', username='Silly-Headrest-2013', password='jTeMIfTy')
bob.show_info()

alice = Connection('Alice Wonder', 'Old-Engine-6372')
bob.establish_connection(alice)
send_periodic_message()
bob.loop_forever()