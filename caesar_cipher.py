def encrypt():
    text=input("input text ")
    shift=int(input("input shift "))
    encrypted=""

    for character in text:
        if character.isnumeric():
            character=str((int(character)+shift)%10)
        
        elif character.isalpha():
            if character.islower():
                character=chr((ord(character)-ord("a")+shift)%26+ord("a"))
            elif character.isupper():
                character=chr((ord(character)-ord("A")+shift)%26+ord("A"))
        encrypted+=character

    print("encrypted text: ", encrypted)
    return encrypted, shift

def decrypt(encrypted, shift):
    text=encrypted
    shift=-shift
    decrypted=""

    for character in text:
        if character.isnumeric():
            character=str((int(character)+shift)%10)
        
        elif character.isalpha():
            if character.islower():
                character=chr((ord(character)-ord("a")+shift)%26+ord("a"))
            elif character.isupper():
                character=chr((ord(character)-ord("A")+shift)%26+ord("A"))
        decrypted+=character

    print("decrypted text: ", decrypted)
    return decrypted

encrypted, shift=encrypt()
decrypt(encrypted, shift)
