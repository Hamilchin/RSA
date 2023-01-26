import RSA
import prime_generation


def create_message(message, file_name):
    with open("decrypted_messages/" + file_name, "w") as f:
        f.write(message) #writes to new file


def encrypt_message(file_name, public_key):
    with open("decrypted_messages/" + file_name) as f:
        text = "".join(f.readlines())
    
    binary = ''.join(format(ord(i), '08b') for i in text) #makes a concatenated binary string according to ASCII
    integer = int(binary, 2) #turns into a decimal integer from binary

    with open("encrypted_messages/" + file_name, "w") as f:
        f.write(str(pow(integer, public_key[0], public_key[1])))
    
    print(f"Message securely encrypted at ./encrypted_messages/{file_name}")


def decrypt_message(file_name, key_pair):
    with open("encrypted_messages/" + file_name) as f:
        encrypted_int = int(f.readline())

    decrypted_int = pow(encrypted_int, key_pair[1], key_pair[0][1])
    byte_number = decrypted_int.bit_length() + 7 // 8
    
    binary_array = decrypted_int.to_bytes(byte_number, "big")
    
    ascii_text = binary_array.decode()
    print(f"Decrypted message from {file_name}:")
    print(ascii_text)


key_pair = RSA.asymmetric_key_pair(2048)

print(key_pair)
public_key = key_pair[0]

create_message("I like ice cubes in milk", "secret.txt")
encrypt_message("secret.txt", key_pair[0])
decrypt_message("secret.txt", key_pair)

#https://docs.google.com/presentation/d/1Aj1mg3Iw-eUVcxCsD6oZNh0eUS9alf5nkMuqum6kQ9I/edit#slide=id.g1ead824ddac_0_10