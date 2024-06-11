def get_questions():
    return [
        {
            "question": "1. Which of the following sorting algorithms has the best average-case time complexity?",
            "options": ["A. Bubble Sort", "B. Quick Sort", "C. Merge Sort", "D. Selection Sort"],
            "answer": "C"
        },
        {
            "question": "2. Which language is primarily used for web development?",
            "options": ["A. Python", "B. JavaScript", "C. C++", "D. Java"],
            "answer": "B"
        },
        {
            "question": "3. What is the full form of PDF?",
            "options": ["A. Portable Document Format", "B. Portable Data Format", "C. Personal Document Format", "D. Personal Data Format"],
            "answer": "A"
        },
        {
            "question": "4. Which of the following is an example of an operating system?",
            "options":["A. Microsoft Word", "B. Adobe Photoshop", "C. Windows 10", "D. Google Chrome"],
            "answer": "C"
        },
        {
            "question": "5. Which protocol is used for secure communication over the Internet?",
            "options":["A. SMTP", "B. FTP", "C. HTTPS", "D. HTTP"],
            "answer": "D"
        },
        {
            "question": "6. Who is considered the father of the modern computer?",
            "options":["A. Alan Turing", "B. Charles Babbage", "C. John von Neumann", "D. Bill Gates"],
            "answer": "B"
        },
        {
            "question": "7. Which company developed the first commercial microprocessor?",
            "options":["A. Intel", "B. IBM", "C. Microsoft", "D. AMD"],
            "answer": "A"
        },
        {
            "question": "8. In what year was the World Wide Web introduced to the public?",
            "options": ["A. 1985", "B. 1991", "C. 1995", "D. 2000"],
            "answer": "B"
        },
        {
            "question": "9. What is the purpose of the ACID properties in database management?",
            "options": ["A. To improve network performance", "B. To optimize memory usage", "C. To ensure the reliability of transactions", "D. To enhance data encryption"],
            "answer": "C"
        },
        {
            "question": "10. Which of the following algorithms is used for public-key cryptography?",
            "options": ["A. AES", "B. DES", "C. SHA-256", "D. RSA"],
            "answer": "D"
        }
    ]

def ask_question(question_data):
    print(question_data["question"])
    for option in question_data["options"]:
        print(option)
    user_answer = input("Please enter your answer: ").strip().upper()
    while user_answer not in ["A", "B", "C", "D"]:
        print("Invalid input. Please enter A, B, C, or D.")
        user_answer = input("Please enter your answer: ").strip().upper()
    return user_answer

def provide_feedback(user_answer, correct_answer):
    if user_answer == correct_answer:
        print("Correct!")
        return 5  # For correct answer
    else:
        print(f"Incorrect. The correct answer is {correct_answer}.")
        return -2  # For incorrect answer

def main():
    print("Welcome to the quiz!")
    start_quiz = input("Do you want to start the quiz? (yes/no): ").strip().lower()
    while start_quiz not in ["yes", "no"]:
        print("Invalid input. Please enter 'yes' or 'no'.")
        start_quiz = input("Do you want to start the quiz? (yes/no): ").strip().lower()

    if start_quiz == "yes":
        questions = get_questions()
        score = 0

        for question_data in questions:
            user_answer = ask_question(question_data)
            score_change = provide_feedback(user_answer, question_data["answer"])
            score += score_change
            print() 

        print(f"Quiz completed! Your final score is {score} out of {len(questions) * 5}.")
        
if __name__ == "__main__":
    main()



