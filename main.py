from program import *
from Style import *
from util import *

def main():
    print_welcome_message()
    while True:
        search_term = input(Style.BOLD + "Enter a search term: " + Style.ENDC)
        if search_term.lower() == 'exit':
            print(Style.RED + "Exiting the application. Thank you for using the Stack Overflow Search Tool!" + Style.ENDC)
            break
        pattern = generate_regex_patterns(search_term)
        questions = fetch_questions(search_term, 50)
        matched_questions = match_questions_using_greedy(questions, pattern)

        if not matched_questions or len(matched_questions) <= 1:
            print(Style.YELLOW + "No exact matches found. Trying broader search..." + Style.ENDC)
            broad_term = search_term.split()[0]
            questions = fetch_questions(broad_term, 100)
            matched_questions = match_questions_using_greedy(questions, pattern)

        if matched_questions:
            display_questions(matched_questions)
        else:
            print(Style.RED + "No relevant questions found. Please try a different search term." + Style.ENDC)

if __name__ == "__main__":
    main()
