import requests
import regex

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

def match_questions_using_greedy(questions, pattern):
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