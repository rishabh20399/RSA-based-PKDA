**1. Introduction:**
  The project's goal was to create a secure communication system using Python that uses RSA
  encryption to encrypt client communications. To securely distribute public keys among clients, a
  Public Key Distribution Authority( PKDA) was established.
 
**2. Implementation:**
  a. PKDA (pkda.py):
    ● Setup: The PKDAspecifies communication ports and public and private keys when it is
    initialized.
    ● KeyManagement: Adictionary contains the client's public keys.
    ● Encryption and Decryption Functions: RSA encryption and decryption are used to
    provide secure communication.
    ● Communication Functions:
    ● send_message() and receive_message(): To receive and send encrypted
    messages.
    ● connect_to_port(): Establishes client relationships.
    ![pkda](https://github.com/rishabh20399/RSA-based-PKDA/assets/88918267/ae53e4f5-a3d6-4fa5-8960-a8ae9a1aecee)

  b. Client 1 (client1.py) and Client 2 (client2.py):
    ● Setup: The public and private keys are used to initialize each client.
    ● KeyExchange: Shares its public key with PKDA so that others can access it.
    ● RequestPublic Key: Sends requests for another client's public key to the PKDA.
    ● SecureMessage Exchange:
    ● Noncesare securely generated and exchanged.
    ● Usesreceived public keys to encrypt and decrypt messages
    ![Cli1Cli2](https://github.com/rishabh20399/RSA-based-PKDA/assets/88918267/f89a6eb3-4f13-4d2e-8c2a-e25943487979)

**3. Working of Functions:**
  a. Encryption and Decryption:
    ● Utilizes RSA algorithm to encrypt and decrypt messages.
    ● encrypt(message, public_key): Encrypts a message using the public key.
    ● decrypt(encrypted_message, private_key): Decrypts an encrypted message using the
    private key.
  b. Communication Functions:
    ● send_message(sock, public_key, message): Sends an encrypted message over a
    socket.
    ● receive_message(sock, private_key): Receives and decrypts a message from a
    socket.
