import requests
import regex

class Style:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'

def fetch_questions(topic, max_items=100):
    questions = []
    page = 1
    custom_filter = "!9_bDDxJY5"
    while len(questions) < max_items:
        params = {
            'page': page,
            'pagesize': 100,
            'order': 'desc',
            'sort': 'activity',
            'intitle': topic,
            'site': 'stackoverflow',
            'filter': custom_filter  
        }
        url = "https://api.stackexchange.com/2.3/search"
        response = requests.get(url, params=params)
        data = response.json().get('items', [])
        if not data:
            break
        questions.extend(data)
        page += 1
    return questions[:max_items]

def generate_regex_patterns(search_term):
    words = search_term.split()
    pattern_string = r'\b' + r'\b|\b'.join(regex.escape(word) for word in words) + r'\b'
    pattern = regex.compile(pattern_string, regex.IGNORECASE)
    return pattern

def match_questions(questions, pattern):
    matched_questions = []
    for question in questions:
        title = question['title']
        matches = list(pattern.finditer(title))
        title_score = len(matches)
        engagement_score = (question.get('answer_count', 0) * 2) + (question.get('comment_count', 1))
        score = title_score * 2 + engagement_score
        matched_questions.append((question, score))
    matched_questions.sort(key=lambda x: x[1], reverse=True)
    return matched_questions[:10]

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

def main():
    print_welcome_message()
    while True:
        search_term = input(Style.BOLD + "Enter a search term: " + Style.ENDC)
        if search_term.lower() == 'exit':
            print(Style.RED + "Exiting the application. Thank you for using the Stack Overflow Search Tool!" + Style.ENDC)
            break
        pattern = generate_regex_patterns(search_term)
        questions = fetch_questions(search_term, 50)
        matched_questions = match_questions(questions, pattern)

        if not matched_questions or len(matched_questions) <= 1:
            print(Style.YELLOW + "No exact matches found. Trying broader search..." + Style.ENDC)
            broad_term = search_term.split()[0]
            questions = fetch_questions(broad_term, 100)
            matched_questions = match_questions(questions, pattern)

        if matched_questions:
            display_questions(matched_questions)
        else:
            print(Style.RED + "No relevant questions found. Please try a different search term." + Style.ENDC)

if __name__ == "__main__":
    main()
