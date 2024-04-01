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
        
    # STEP 0: Sharing client2 public key with PKDA [E(PU_pkda(PUa))]
    s_pkda=connect_to_port(host,client2_port2,pkda_port2,"PKDA")
    print("Sharing client2 public key [E(PU_pkda(PUa))] with PKDA -->", public_keys[client2_id])
    send_message(s_pkda,public_keys["PKDA"],str(public_keys[client2_id]))

    # STEP 1-3: Took course in client1

    # STEP 3: Receiving <-- E(PU_b[ID_a || N1]) -- from client 1
    s1=connect_to_port(host,client2_port1,client1_port2,client1_id)
    step3=eval(receive_message(s1,client2_private_key))
    print("Receiving E(PU_b[ID_a || N1]) from client 1--> ",step3)
    contact_id=step3[0]
    n1 = step3[1]

    # STEP 4: Sending -- Request || T1 --> to PKDA
    timestamp = time.localtime(time.time())
    time_string = time.strftime("%H:%M:%S", timestamp)
    step4 = (contact_id,time_string)
    print("Sending Request || T2 to PKDA --> ",step4)
    send_message(s_pkda,public_keys["PKDA"],str(step4))

    # STEP 5: Receiving <-- E(PR_auth[PU_b||Request||T1]) -- from PKDA
    step5=eval(receive_message(s_pkda,public_keys["PKDA"]))
    print("Receiving E(PR_auth[PU_b||Request||T1]) from PKDA --> ",step5)
    public_keys[client1_id]=step5[0]

    # STEP 6: Sending -- E(PU_a[N1 || N2]) --> to client 1
    n2= generate_nonce()
    step6= (n1,n2)
    print("Sending E(PU_b,[ID_a||N1]) to client 1 --> ",step6)
    send_message(s1,public_keys[client1_id],str(step6))
    
    # STEP 7: Receiving <-- E(PU_b[N2]) from client 1
    step7=eval(receive_message(s1,client2_private_key))
    print("Receiving E(PU_b[N2]) from client 1 --> ", step7)

    x=0
    while True:
        x+=1
        recv_message=receive_message(s1,client2_private_key)
        print("Client 1 says:\n", recv_message)

        message = "Gotit "+ str(x)
        send_message(s1,public_keys[client1_id],str(message))


if __name__ == "__main__":
    
    
    # Setup Clients
    client1_id = "client1"
    client2_id = "client2"

    
    client2_public_key, client2_private_key = rsa.generate_rsa_keys()
    print("client1_public_key: ",client2_public_key,"\nclient1_private_key: ", client2_private_key)
    public_keys[client2_id]=eval(str(client2_public_key))

    main()

    # store_public_key_in_pkda(client2_id, client2_public_key, public_keys)
    # client2_public_key_from_pkda = get_public_key_from_pkda(client2_id, public_keys)
    # print(client2_public_key_from_pkda)


    # message_to_client2 = (191, 323)
    # encrypted_message_to_client2 = encrypt(str(message_to_client2), client2_public_key_from_pkda)
    # print(''.join(str(p) for p in encrypted_message_to_client2))
    # decrypted_message_to_client2 = eval(decrypt(encrypted_message_to_client2, client2_private_key))
    # print(decrypted_message_to_client2)
