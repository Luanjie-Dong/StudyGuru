import requests
import time


#module_id
def get_topics(module_id):
    
    notes_endpoint = f"http://notes:5000/notes?module_id={module_id}"

    # notes_endpoint = f"http://127.0.0.1:5005/notes"
    notes_param = {
        "module_id": module_id
    }

    retries = 3  
    delay = 2    

    while retries > 0:
        try:
            response = requests.get(notes_endpoint,params=notes_param)
            response.raise_for_status()  
            notes_data = response.json()

            topics = []
            for note in notes_data:
                sub_topics = note.get("topics", [])
                if sub_topics:
                    topics.extend(sub_topics)

            if topics:
                return topics
            

        except requests.exceptions.RequestException as e:
            print(f"Error fetching content for module {module_id}: {e}")
            

        retries -= 1

        if retries > 0:
            print(f"Retrying... ({retries} attempts left)")
            time.sleep(delay)

    return []



def get_quizzes(challenge_id):

    questions_endpoint = f"http://questions:5000/questions_attempt?challenge_id={challenge_id}"
    # questions_endpoint = f"http://127.0.0.1:5006/questions_attempt?challenge_id={challenge_id}"


    try:
        response = requests.get(questions_endpoint)
        response.raise_for_status()

        questions_data = response.json()

        return questions_data          


    except requests.exceptions.RequestException as e:
            print(f"Error fetching content for module: {challenge_id}: {e}")



def get_course(challenge_id):
    questions_endpoint = f"http://challenge:5000/challenge_info?challenge_id={challenge_id}"
    # questions_endpoint = f"http://127.0.0.1:5006/challenge_info?challenge_id={challenge_id}"


    try:
        response = requests.get(questions_endpoint)
        response.raise_for_status()

        questions_data = response.json()

        return questions_data['course_id']          


    except requests.exceptions.RequestException as e:
            print(f"Error fetching content for module: {challenge_id}: {e}")
