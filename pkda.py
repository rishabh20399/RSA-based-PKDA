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
    
    # Create a TCP/IP socket
        
          
    
        
    # STEP 0.1: Receiving public key of client 2
    s2=connect_to_port(host,pkda_port2,client2_port2,client2_id)
    step0_1=eval(receive_message(s2,pkda_private_key))
    print("Receiving public key of client 2 --> ",step0_1)
    public_keys[client2_id]=step0_1

    # STEP 0.2: Receiving public key of client 1
    s1=connect_to_port(host,pkda_port1,client1_port1,client1_id)
    step0_2=eval(receive_message(s1,pkda_private_key))
    print("Receiving public key of client 1 --> ",step0_2)
    public_keys[client1_id]=step0_2


    # STEP 1: Receiving <-- Request || T1 -- from client 1
    step1=eval(receive_message(s1,pkda_private_key))
    print("Receiving Request || T1 --> ",step1)
    req_id= step1[0]
    t1= step1[1]

    # STEP 2: Sending -- E(PR_auth[PU_b||Request||T1]) --> to client 1
    step2 = (public_keys[req_id],req_id,t1)
    print("Sending E(PR_auth[PU_b||Request||T1]) --> ",step2)
    send_message(s1,pkda_private_key,str(step2))

    # STEP 3: Receiving <-- Request || T1 -- from client 2
    step3=eval(receive_message(s2,pkda_private_key))
    print("Receiving Request || T1 --> ",step3)
    req_id= step3[0]
    t2= step3[1]

    # STEP 4: Sending -- E(PR_auth[PU_a||Request||T2]) --> to client 2
    step4 = (public_keys[req_id],req_id,t2)
    print("Sending E(PR_auth[PU_a||Request||T2]) --> ",step4)
    send_message(s2,pkda_private_key,str(step4))
                        

if __name__ == "__main__":
    
    
    # Setup Clients
    client1_id = "client1"
    client2_id = "client2"

    pkda_public_key, pkda_private_key = (185, 323), (137, 323)
    main()
