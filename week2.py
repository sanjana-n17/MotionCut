import re

def count_words(text):
    #Function to take a string input and return the number of words.
    
    #To remove punctuations
    punctuation = '.,!?;:"()[]{}<>'
    for char in punctuation:
        text = text.replace(char, '')
    
    # Split text into words
    words = text.split()
    
    # Filter words based on the new conditions
    filtered_words = []
    for word in words:
        # Check if the word contains any alphabetic characters
        if not re.search(r'[a-zA-Z]', word):
            continue  # Skip words without alphabetic characters
        # When the word ends or starts with a number
        if re.search(r'^\d|\d$', word):
            continue
        filtered_words.append(word)
    
    return len(filtered_words)

def main():
    # Main function handles user input and displays the word count.
 
    # Prompt the user to give input
    user_input = input("Please enter a sentence or paragraph: ").strip()
    
    # Check if input is empty
    if not user_input:
        print("Error! No input provided. Please enter some text.")
    else: 
        word_count = count_words(user_input)
        # Display the word count as output
        print(f"The number of words in the entered text is: {word_count}")

if __name__ == "__main__":
    main()
