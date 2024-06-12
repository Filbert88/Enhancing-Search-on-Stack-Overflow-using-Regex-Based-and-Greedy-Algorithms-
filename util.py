from Style import *
from program import *

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        dictionary = set(word.strip().lower() for word in file.readlines())
    return dictionary

def find_closest_word(input_word, dictionary):
    closest_word = None
    min_distance = float('inf')
    for word in dictionary:
        dist = cached_levenshtein_distance(input_word, word)
        
        if word.startswith(input_word[0]):
            dist -= 0.5 

        if abs(len(word) - len(input_word)) <= 1:
            dist -= 0.5

        if dist < min_distance:
            min_distance = dist
            closest_word = word
        
        if dist == 0:  
            break

    if min_distance > 2 or closest_word is None: 
        return input_word
    return closest_word

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