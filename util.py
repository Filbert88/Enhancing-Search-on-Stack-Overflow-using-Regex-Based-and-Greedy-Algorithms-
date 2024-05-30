from Style import *

def display_questions(matched_questions):
    print(Style.HEADER + Style.BOLD + "Top Matched Questions:" + Style.ENDC)
    for question, score in matched_questions:
        print(Style.BOLD + "Title: " + Style.BLUE + question['title'] + Style.ENDC)
        print("Link: " + Style.UNDERLINE + Style.CYAN + question['link'] + Style.ENDC)
        print("Score: " + Style.YELLOW + str(question['score']) + Style.ENDC)
        print("Comments: " + str(question.get('comment_count', 0)))
        print("Answers: " + str(question.get('answer_count', 0)))
        print("Views: " + str(question.get('view_count', 0)) + "\n")

def print_welcome_message():
    print(Style.GREEN + Style.BOLD + "Welcome to the Stack Overflow Search Tool!" + Style.ENDC)
    print(Style.DIM + "This tool helps you find the most relevant questions based on your search terms.")
    print("Simply enter a search term, and we'll retrieve the top questions for you!" + Style.ENDC)
    print("Type 'exit' to quit the application.\n" + Style.ENDC)