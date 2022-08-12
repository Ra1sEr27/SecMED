# SecMED
  An application that allow the doctor to manage the patient information safely, able to access from anywhere using the registered IP address
  - Features
    - Use of Advanced Encryption System (AES) to encrypt & decrypt the data.
    - Use of Ciphertext-policy attribute-based encryption (CP-ABE) to encrypt the symmetric key.
    - Use of Rivest-Shamir-Adleman encryption (RSA) to transform the ciphertext to digital signature.
    - Use of Homomorphic encryption to create an additional key which is used to enchance the confidentiality of digital signature.
    - Use of SHA-256 Hashing Algorithm to create an index of ciphertext.
  - System Diagrams
    - System Overview

      ![image](https://user-images.githubusercontent.com/94690219/183926103-a93729b3-2323-4406-bd31-ca3fc130d8bb.png)
    - Encryption

      ![image](https://user-images.githubusercontent.com/94690219/183926783-d1019d66-4570-4481-a06b-da8c1abc9aa9.png)
    - Decryption

      ![image](https://user-images.githubusercontent.com/94690219/183926994-75e51236-f3fc-47d8-8b62-5abc8f4171f3.png)
    - Auditing

      ![image](https://user-images.githubusercontent.com/94690219/183927700-061808f7-6065-4c8d-87bc-b08d3c534823.png)
  - Data Structure of patient document
    - Patient document (Plaintext)

      ![image](https://user-images.githubusercontent.com/94690219/173511853-7f2c5aa0-54c3-486e-93a7-4ea6f5797d76.png)
    - Patient document for storing on cloud (Ciphertext)

      ![image](https://user-images.githubusercontent.com/94690219/183928523-e03c23ec-cbe5-4925-a02c-a64a8ee4ec31.png)
      - MD_id  : a hash value of patient id which is used as an index for retrieving the document for the medicat treatment record of the patient.
      - CT     : an encrypted form of MTR of the patient.
      - enc_SK : an encrypted form of the secret key SK which is encrypted by a CP-ABE method.
      - DS*R   : a digital signature of the latest updater shuffled with the random value (R). 
      - R1     : a new random value of the original R. It is generated by applying shuffling between R and another random value (R’). 
    - Audit log
    
      ![image](https://user-images.githubusercontent.com/94690219/183930409-bbbb6d8d-03b3-401b-8c36-61f0343e14bb.png)
      - MD_id  : a hash value of patient id which is used as an index for retrieving the document for the medicat treatment record of the patient.
      - certid : a certificate ID of data owner or editor.
      - CT     : an encrypted form of MTR of the patient.
      - Priv_key: a private key of data owner or editor.
      - DS*R   : a digital signature of the latest updater shuffled with the random value (R). 
      - R1     : a new random value of the original R. It is generated by applying shuffling between R and another random value (R’). 

