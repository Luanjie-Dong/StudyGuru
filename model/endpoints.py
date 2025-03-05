import requests


#module_id
def get_topics(module_id):
    
    # notes_endpoint = f"http://host.docker.internal:5005/notes?module_id={module_id}"

    notes_endpoint = f"http://127.0.0.1:5005/notes?module_id={module_id}"
    
    try:
        response = requests.get(notes_endpoint)
        response.raise_for_status()

        notes_data = response.json()

        
        topics = []
        for note in notes_data:
            sub_topics = note.get("topics",[])
            if sub_topics:
                topics.extend(sub_topics)

        return topics            


    except requests.exceptions.RequestException as e:
            print(f"Error fetching content for module: {module_id}: {e}")



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




