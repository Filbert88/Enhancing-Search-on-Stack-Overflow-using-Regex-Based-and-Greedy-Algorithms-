from program import *
from Style import *
from util import *
import time
import re

dictionary = load_dictionary('words.txt') 

def refine_search_query(query, dictionary):
    refined_query = []
    
    parts = re.split('(\W+)', query) 

    for part in parts:
        if part.isalpha(): 
            closest_word = find_closest_word(part, dictionary)
            refined_query.append(closest_word if closest_word else part)
        else:
            refined_query.append(part) 

    return ''.join(refined_query)

def main():
    print_welcome_message()
    while True:
        search_term = input(Style.BOLD + "Enter a search term: " + Style.ENDC)
        if search_term.lower() == 'exit':
            print(Style.RED + "Exiting the application. Thank you for using the Stack Overflow Search Tool!" + Style.ENDC)
            break
        
        pattern = generate_regex_patterns(search_term)
        variations = generate_variations_from_pattern(search_term)

        questions = []
        found = False 

        for term in variations:
            if not found: 
                print(f"Fetching questions for: {term}")
                fetched_questions = fetch_questions(term, 100)  
                if fetched_questions:
                    questions.extend(fetched_questions)
                    time.sleep(1)  
                    if len(fetched_questions) >= 1: 
                        print(f"Sufficient questions fetched for {term}.")
                        found = True  
                else:
                    print(f"No questions found for {term}.")
            else:
                break

        questions = {q['question_id']: q for q in questions}.values()

        matched_questions = match_questions_using_greedy(questions, pattern)

        if not matched_questions or len(matched_questions) <= 1:
            print(Style.YELLOW + "No exact matches found. Trying broader search..." + Style.ENDC)
            broad_term = search_term.split()[0]
            broad_variations = generate_variations_from_pattern(broad_term)

            questions = []
            found = False 

            for term in broad_variations:
                if not found: 
                    print(f"Fetching questions for: {term}")
                    fetched_questions = fetch_questions(term, 100)  
                    if fetched_questions:
                        questions.extend(fetched_questions)
                        time.sleep(1)  
                        if len(fetched_questions) >= 1: 
                            print(f"Sufficient questions fetched for {term}.")
                            found = True  
                    else:
                        print(f"No questions found for {term}.")
                else:
                    break
            
            if not found:
                refined_search_term = refine_search_query(broad_term, dictionary)
                print(Style.YELLOW + f"Refined search term used: {refined_search_term}" + Style.ENDC)
                refined_questions = fetch_questions(refined_search_term, 100)
                questions.extend(refined_questions)

            questions = {q['question_id']: q for q in questions}.values()
            
            matched_questions = match_questions_using_greedy(questions, pattern)

        if matched_questions:
            display_questions(matched_questions)
        else:
            print(Style.RED + "No relevant questions found. Please try a different search term." + Style.ENDC)

if __name__ == "__main__":
    main()