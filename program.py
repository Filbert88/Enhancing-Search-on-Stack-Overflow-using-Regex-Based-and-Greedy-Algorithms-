import requests
import regex
from functools import lru_cache
from itertools import product

def fetch_questions(topic, max_items=100):
    questions = []
    page = 1
    custom_filter = "!9_bDDxJY5"
    api_key = '93KS9ghSKNGXkc7kadtKjQ(('  
    while len(questions) < max_items:
        params = {
            'page': page,
            'pagesize': 100,
            'order': 'desc',
            'sort': 'activity',
            'intitle': topic,
            'site': 'stackoverflow',
            'filter': custom_filter,
            'key': api_key 
        }
        url = "https://api.stackexchange.com/2.3/search"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get('items', [])
            if not data:
                break
            questions.extend(data)
            page += 1
        else:
            print(f"Error: Received status code {response.status_code} for topic '{topic}'")
            print(f"Response content: {response.text}")
            break
    return questions[:max_items]

def generate_variations_from_pattern(search_term):
    substitutions = {
        '0': 'o',
        '1': 'i',
        '3': 'e',
        '4': 'a',
        '5': 's',
        '6': 'g',
        '7': 't',
        '8': 'b',
        '9': 'g',
        '@': 'a',
        '!': 'i',
        '$': 's'
    }
    
    words = search_term.split()
    variations = [search_term]
    
    for word in words:
        if any(char in substitutions for char in word):
            chars = [[char] if char not in substitutions else [char, substitutions[char]] for char in word]
            word_variations = [''.join(candidate) for candidate in product(*chars)]
            for variation in word_variations:
                new_variation = search_term.replace(word, variation, 1)
                if new_variation not in variations:
                    variations.append(new_variation)
    
    return variations

def generate_regex_patterns(search_term):
    leet_speak_substitutions = {
        'a': '[a4@]',  
        'e': '[e3]',    
        'i': '[i1!]',   
        'o': '[o0]',    
        's': '[s5$]',  
        't': '[t7+]',   
        'g': '[g69]',    
        'b': '[b8]',
        '0': '[o]',
        '5': '[5s$]',
        '4': '[4a@]',
        '3': '[3e]',
        '1': '[1i!]',
        '6': '[69g]',
        '9': '[9g]', 
        '8': '[8b]', 
        '7': '[7t+]'
    }

    pattern_parts = []
    for word in search_term.split():
        patterned_word = ''.join(leet_speak_substitutions.get(char, char) for char in word.lower())
        pattern_parts.append(patterned_word)

    pattern_string = r'\b' + r'\b|\b'.join(pattern_parts) + r'\b'
    pattern = regex.compile(pattern_string, regex.IGNORECASE)
    return pattern

def match_questions_using_greedy(questions, pattern):
    matched_questions = []
    for question in questions:
        title = question['title']
        matches = list(pattern.finditer(title))
        title_score = len(matches)
        engagement_score = ((question.get('answer_count', 0) * 2) 
                            + (question.get('comment_count', 1)))
        score = title_score * 2 + engagement_score
        matched_questions.append((question, score))
    matched_questions.sort(key=lambda x: x[1], reverse=True)
    return matched_questions[:20]

@lru_cache(maxsize=10000)
def cached_levenshtein_distance(s1, s2):
    return levenshtein_distance(s1, s2)

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]