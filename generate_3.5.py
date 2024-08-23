import json
import g4f


# Define the prompt for the request
prompt = """
Write 100 test questions to prepare for CIA exam part one. Each question should have 4 answers. create text for .json file with table of that questions containing the following fields: 
Question ID
Exam: CIA
Part: 1
Question Number: A unique identifier for each question.
Question Text: The content of the question itself.
Option A: First possible answer.
Option B: Second possible answer.
Option C: Third possible answer.
Option D: Fourth possible answer.
Correct Answer: The correct option (e.g., A, B, C, or D).
Explanation
Tips
Category: The specific topic or area the question covers, aligned with the CIA exam syllabus.
Number of attempts: 0
Number of correct answers: 0
Percentage of correct answers: 0

Questions should strictly adhere to original exam by difficulty and knowledge areas. Some of questions should be long and based on scenarios. Other questions should refer to international auditing standards.

File must contain 100 questions
"""
# prompt = """
#     What is CIA?
# """

# Send the request to G4F using the appropriate model
response = g4f.ChatCompletion.create(
    model="gpt-3.5",
    messages=[{"role": "user", "content": prompt}],
    provider=g4f.Provider.Aichatos,
    cookies={"AEC": "AQTF6HwDOgQfJEAm-8C8KQGKxwMVkpEW0JnVuz4fb4F03Lpzx_1cSi_7UA", 
             "NID": "514=wGTh-5ihv-BjWAq_MmzzV_XrX_cRv5B0EhlidBeFSl_KdbXFoxUFUvJfmySCjM2UtWAfItlV4ICz_XGmYde2zY25Y6SwEaLgMeot5zDuMKrFJlPapPvt7Z8FRkQNfKDJJ6GhweqglEZZ8Nq7ufneY58wSaKP5DRcmHRA_JmwVCQ"},
    stream=True,
    auth=True,
)

for message in response:
    print(message, flush=True, end='')
# print(response)

# # Assuming the first choice in the response contains the text needed
# response_text = response.choices[0].message.content if response.choices else ""

# try:
#     # Convert the response text to JSON format (assuming the output is in proper JSON format as per the prompt)
#     questions = json.loads(response_text)

#     # Save the questions to a JSON file
#     # with open('cia_exam_part_one_questions.json', 'w') as json_file:
#     #     json.dump(questions, json_file, indent=4)
#     print(questions)

#     print("Questions saved to 'cia_exam_part_one_questions.json'")
# except json.JSONDecodeError:
#     print("Failed to decode response into JSON. Check the response format.")