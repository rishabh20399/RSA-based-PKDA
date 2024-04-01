import socket
import rsa
import pickle
import time
import random



# Setup for public keys
public_keys = {"PKDA":(185, 323)}  # Dictionary to store public keys of pkda, client
host = 'localhost'  # Server's hostname or IP address
pkda_port1 = 9000  
pkda_port2 = 9005

client1_port1 = 9001
client1_port2 = 9003

client2_port1 = 9002
client2_port2 = 9004


# Function to encrypt a message using RSA
def encrypt(message, public_key):
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    # print("Encrypted:\n",''.join(str(p) for p in encrypted_message))
    return encrypted_message

# Function to decrypt an encrypted message using RSA
def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    # print("Decrypted: ",decrypted_message)
    return decrypted_message

# Function to generate a random nonce
def generate_nonce():
    return random.randint(0, 2**32 - 1)
    
# # Function to get public key of a client from PKDA
# def get_public_key_from_pkda(client_id, public_keys):
#     return public_keys.get(client_id, None)

# # Function to store public key of a client in PKDA
# def store_public_key_in_pkda(client_id, public_key, public_keys):
#     public_keys[client_id] = public_key




# Sending . . .
def send_message(sock, public_key, message):
    encrypted_message = encrypt(message, public_key)
    sock.sendall(str(encrypted_message).encode())

# Receiving . . .
def receive_message(sock, private_key):
    while True:
        data = sock.recv(1024)
        if data:
            encrypted_message = eval(data.decode())
            decrypted_message = decrypt(encrypted_message, private_key)
            return decrypted_message

# Connecting . . .        
def connect_to_port(host,own_port,port_to_connect,id):
    sokt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sokt.bind((host, own_port))  # Bind to the specified port
    # s.listen(5)
    while True:  # Wait for client to come online to connect
        try:
            sokt.connect((host, port_to_connect))
            print("Connected to", id)
            return sokt
        except ConnectionRefusedError:
            # print("Connection to", id, "failed. Retrying...")
            time.sleep(3)  # Wait for 3 sec before retrying



def main(): 
        
    # STEP 0: Sharing client1 public key with PKDA [E(PU_pkda(PUa))]
    s_pkda=connect_to_port(host,client1_port1,pkda_port1,"PKDA")
    print("Sharing client1 public key with PKDA -->", public_keys[client1_id])
    send_message(s_pkda,public_keys["PKDA"],str(public_keys[client1_id]))

    # STEP 1: Sending -- Request || T1 --> to PKDA
    timestamp = time.localtime(time.time())
    time_string = time.strftime("%H:%M:%S", timestamp)
    step1 = (client2_id,time_string)
    print("Sending Request || T1 --> ",step1)
    send_message(s_pkda,public_keys["PKDA"],str(step1))

    # STEP 2: Receiving <-- E(PR_auth[PU_b||Request||T1]) -- from PKDA
    step2=eval(receive_message(s_pkda,public_keys["PKDA"]))
    print("Receiving E(PR_auth[PU_b||Request||T1]) --> ",step2)
    public_keys[client2_id]=step2[0]

    # STEP 3: Sending -- E(PU_b,[ID_a||N1]) --> to client 2
    s2=connect_to_port(host,client1_port2,client2_port1,client2_id)
    n1= generate_nonce()
    step3= (client1_id,n1)
    print("Sending E(PU_b,[ID_a||N1]) --> ",step3)
    send_message(s2,public_keys[client2_id],str(step3))

    # STEP 4,5: Take place in client 2
    # STEP 6: Receiving  <-- E(PU_a[N1 || N2]) -- from client 2
    step6=eval(receive_message(s2,client1_private_key))
    print("Receiving E(PU_a[N1 || N2]) --> ",step6)
    n2=step6[1]

    # STEP 7: Sending -- E(PU_b[N2]) --> to client 2 
    step7= (n2)
    print("Sending E(PU_b[N2]) --> ",step7)
    send_message(s2,public_keys[client2_id],str(step7))


    while True:

        message = input("Enter client 1 message:\n")
        send_message(s2,public_keys[client2_id],str(message))
        
        recv_message=receive_message(s2,client1_private_key)
        print("Client 2 says:\n", recv_message)


if __name__ == "__main__":
    
    
    # Setup Clients
    client1_id = "client1"
    client2_id = "client2"

    
    client1_public_key, client1_private_key = rsa.generate_rsa_keys()
    print("client1_public_key: ",client1_public_key,"\nclient1_private_key: ", client1_private_key)
    public_keys[client1_id]=eval(str(client1_public_key))

    main()

    # store_public_key_in_pkda(client1_id, client1_public_key, public_keys)
    # client1_public_key_from_pkda = get_public_key_from_pkda(client1_id, public_keys)
    # print(client1_public_key_from_pkda)


    # message_to_client1 = (191, 323)
    # encrypted_message_to_client1 = encrypt(str(message_to_client1), client1_public_key_from_pkda)
    # print(''.join(str(p) for p in encrypted_message_to_client1))
    # decrypted_message_to_client1 = eval(decrypt(encrypted_message_to_client1, client1_private_key))
    # print(decrypted_message_to_client1)
