"""this is a Python script for a dating profile matchmaker using a local LLM server.
It reads a JSON database of profiles, retrieves a specific profile based on user input,"""

# This code is designed to interact with a local LLM server to find dating profiles and suggest matches.
# It reads from a JSON database, retrieves a profile based on the username input, and uses an LLM to suggest an ideal match.
# Ensure the LLM server is running and the database file is correctly formatted.

import requests

import json


url = "http://localhost:12434/engines/llama.cpp/v1/chat/completions"

with open("data/db.json", "r") as f:
    database = f.read()

data_dict = json.loads(database)
print("Database loaded successfully.")
available_profiles = data_dict.keys()
print(f"Available profiles: {', '.join(available_profiles)}")

username = input("Enter a username to find the corresponding dating profile: ")


def find_profile(username):
    return data_dict.get(username, "Profile not found.")


def call_llm_matchmaker(username):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "ai/smollm2",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"what is the dating profile corresponding to this username? {username}. what would be an ideal good match for this profile?",
            },
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    json_data = response.json()

    message = json_data["choices"][0]["message"]["content"]
    return message


def main(username):
    profile = find_profile(username)

    if profile == "Profile not found.":
        print(profile)
    else:
        print(f"Profile for {username}: {profile}")
        match = call_llm_matchmaker(username)
        print(f"Ideal match for {username}: {match}")


if __name__ == "__main__":
    main(username)
