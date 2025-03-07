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



# def challenge_answer(challenge_id):

#     notes_endpoint = f"http://host.docker.internal:5005/notes?module_id={module_id}"

#     try:
#         response = requests.get(notes_endpoint)
#         response.raise_for_status()

#         notes_data = response.json()

#         topics = []
#         for note in notes_data:
#             topics.extend(note.get("topics",""))

#         return topics            


#     except requests.exceptions.RequestException as e:
#             print(f"Error fetching content for module: {module_id}: {e}")




