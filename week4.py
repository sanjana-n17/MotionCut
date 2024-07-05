import random
import string

def generate_password(length):

    # Create character sets
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    spl = "-!@#$%^&*+"

    # Ensure at least one character from each set is included
    password = [random.choice(upper), random.choice(lower), random.choice(digits), random.choice(spl)]

    # Fill the rest of the password length with random choices from all sets
    characters = upper + lower + digits + spl
    password += random.choices(characters, k=length-4)

    # Shuffle the list to ensure randomness and convert to a string
    random.shuffle(password)
    return ''.join(password)

def main():
    try:
        print("Welcome to the Password Generator :)")
        length = int(input("Enter the required password length: "))
        if length < 8:
            raise ValueError("Password length should be at least 8")

        count = int(input("Enter the number of passwords to be generated: "))

        for i in range(count):
            print(f"Password {i+1}: {generate_password(length)}")
    
    except ValueError as ve:
        print(f"Error: {ve}")

if __name__ == "__main__":
    main()
