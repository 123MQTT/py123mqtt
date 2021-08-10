from ecdsa import ECDH, SigningKey, VerifyingKey, SECP128r1
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from paho.mqtt.client import Client as mqttClient
import os
import json

CHAT_MODE_UNSECURED = 0
CHAT_MODE_SIGNED = 1
CHAT_MODE_ENCRYPTED = 2


class Connection:
    'Connection Class'

    def __init__(self, name, username):
        self.name = name
        self.username = username
        self.chat_mode = CHAT_MODE_UNSECURED
        self.publickey = 'none'
        self.shared_secret = 'none'
    
    def chat_mode(self, mode):
        self.chat_mode = mode
    
    def list_connections(self):
        print(self.connections)

    def cb_process_publickey(self, client, userdata, msg):
        # received public key and generate shared secret
        self.publickey = msg.payload
        Messaging.ecdh.load_received_public_key_bytes(bytearray.fromhex(self.publickey.decode()))
        self.shared_secret = Messaging.ecdh.generate_sharedsecret_bytes()
        self.chat_mode = CHAT_MODE_ENCRYPTED
        # remove callback hook
        client.message_callback_remove(msg.topic)
        print('Shared secret: ' + self.shared_secret.hex())

    def cb_process_request(self, client, userdata, msg):
        client.publish('public-data/' + Messaging.username + '/' + self.username + '/publickey', Messaging.vk.to_string().hex(), 2)

    def cb_process_message(self, client, userdata, msg):
        # got a message
        received = json.loads(msg.payload)
        # decrypting message when shared secret is obtained
        if (self.shared_secret != 'none' and received['encryption'] != 'none'):
            decrypto = AES.new(self.shared_secret, AES.MODE_CBC, bytes.fromhex(received['iv']))
            decrypted_text_bytes = decrypto.decrypt(bytes.fromhex(received['message']))
            print(msg.topic + ': ' + decrypted_text_bytes.decode())
        elif (self.shared_secret == 'none' and received['encryption'] != 'none'):
            print('Warning: no shared secret to decrypt message')
            print(msg.topic + ': ' + received['message'])
        elif (received['encryption'] == 'none'):
            print('Warning: received unencrypted message')
            print(msg.topic + ': ' + received['message'])
        else:
            pass


class Messaging:
    'Messaging Class 123MQTT'

    sk_string = bytearray.fromhex(os.environ.get('PRIVATEKEY'))
    sk = SigningKey.from_string(sk_string, SECP128r1)
    vk = sk.verifying_key
    ecdh = ECDH(curve=SECP128r1)
    ecdh.load_private_key(sk)
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')

    def __init__(self, private_key, username, password):
        self.mqttClient = mqttClient()
        self.mqttClient.on_connect = self._on_connect
        self.mqttClient.username_pw_set(username=username, password=password)
        self.mqttClient.connect("123mqtt.com", 1883, 60)
        self.mqttTopics = []
        print('Init done')

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected to 123MQTT with result code " + str(rc))
        if (rc == 0):
            for topic in self.mqttTopics:
                print('Subcribing to topic: ' + topic)
                self.mqttClient.subscribe(topic)
    
    def establish_connection(self, Connection):
        # subscribe to topics
        self.mqttTopics.append('public-data/' + Connection.username + '/' + self.username + '/request')
        self.mqttTopics.append('public-data/' + Connection.username + '/' + self.username + '/publickey')
        self.mqttTopics.append('public-data/' + Connection.username + '/' + self.username + '/message')
        # callback hooks
        self.mqttClient.message_callback_add('public-data/' + Connection.username + '/' + self.username + '/request', Connection.cb_process_request)
        self.mqttClient.message_callback_add('public-data/' + Connection.username + '/' + self.username + '/publickey', Connection.cb_process_publickey)
        self.mqttClient.message_callback_add('public-data/' + Connection.username + '/' + self.username + '/message', Connection.cb_process_message)
        # immediate request a public key from Connection
        self.mqttClient.publish('public-data/' + self.username + '/' + Connection.username + '/request', 'publickey', 2)

    def send_message(self, Connection, message):
        if (Connection.chat_mode == CHAT_MODE_UNSECURED):
            # send unencrypted message
            print('Warning: sending unencrypted message')
            message = {"message" : message, "encryption" : "none", "iv" : "none"}
            self.mqttClient.publish('public-data/' + self.username + '/' + Connection.username + '/message', json.dumps(message), 2)
        else:
            # send encrypted message
            self.signature = self.sk.sign(pad(message.encode(), AES.block_size))
            iv = os.urandom(16)
            crypto = AES.new(Connection.shared_secret, AES.MODE_CBC, iv)
            encrypted_text_bytes = crypto.encrypt(pad(message.encode(), AES.block_size))
            encrypted_text_hex = encrypted_text_bytes.hex()
            message = {"message" : encrypted_text_hex, "encryption" : "AES-128-CBC", "iv" : iv.hex()}
            self.mqttClient.publish('public-data/' + self.username + '/' + Connection.username + '/message', json.dumps(message), 2)

    def show_info(self):
        print('')
        print('Private information:')
        print('====================')
        print('Private key  : ' + self.sk.to_string().hex())
        print('MQTT username: ' + self.username)
        print('MQTT password: ' + self.password)
        print('')
    
    def loop_forever(self):
        self.mqttClient.loop_forever()

# END Class Messaging123Mqtt