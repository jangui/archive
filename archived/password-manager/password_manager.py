#!/usr/bin/env python2
import base64, bcrypt
from Crypto.Cipher import AES
from getpass import getpass

def getKey():
    return getpass('master key: ')

def encode(password, key):
    password = password.rjust(32)
    cipher = AES.new(key,AES.MODE_ECB)
    encoded = base64.b64encode(cipher.encrypt(password))
    return encoded

def decode(string, secret_key):
    cipher = AES.new(secret_key,AES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(string)).strip()


def main():
    key = getKey() #key must be size 16, 32, 64
    filename = raw_input("file: ") #can be an absolute or relative file path

    while True:
        print "\n---Password Manager---"
        option = raw_input("Select Option:\n  1. Add Password\n" +
        "  2. View Passwords\n  3. Edit Password\n  4. Delete Password\n  5. Quit\n")

        #encode and add password to file
        if option == '1':
            password = raw_input('Enter password: ')
            try:
                encoded = encode(password, key)
            except ValueError:
                print "ERROR: master key must be of length 16, 24, or 32"
                exit(1)
            with open(filename, 'a') as f:
                f.write(encoded + '\n')

        #read file line by line and decode each line
        elif option == '2':
            print '\n~Passwords~'
            with open(filename, 'r') as f:
                counter = 1
                for line in f:
                    print str(counter) + ". " + decode(line.strip(), key)
                    counter += 1
            raw_input('\nPress any key to continue...')

        #modify password
        elif option == '3':
            pass_id = int(raw_input("Enter password's id\n")) - 1
            password = raw_input("Enter new password: ")
            encoded = encode(password, key)
            lines = []

            with open(filename, 'r') as f:
                counter = 0
                for line in f:
                    if counter == pass_id:
                        lines.append(encoded)
                    else:
                        lines.append(line.strip())
                    counter += 1

            with open(filename, 'w') as f:
                for line in lines:
                    f.write(line + '\n')

        #delete password
        elif option == '4':
            pass_id = int(raw_input("Enter password's id\n")) - 1

            confirm = raw_input("Are you sure you want to delete password #" + str(pass_id+1) + "? (y/n)\n")
            if confirm == 'y':
                lines = []
                with open(filename, 'r') as f:
                    counter = 0
                    #add all lines except the one we want to delete
                    for line in f:
                        if counter != pass_id:
                            lines.append(line.strip())
                        counter += 1

                with open(filename, 'w') as f:
                    for line in lines:
                        f.write(line + '\n')
                raw_input("\nPassword successfully deleted\nPress any key to continue...")

            elif confirm == 'n':
                continue

        elif option == '5':
            break

if __name__ == "__main__":
    main()
