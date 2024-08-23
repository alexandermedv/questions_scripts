import json
import g4f
from config import model, questions_db
from datetime import datetime
from sqlalchemy import create_engine

engine = create_engine(questions_db)

# Define the prompt for the request
prompt = f"""
Write 5 test questions to prepare for CIA exam part one. Each question should have 4 answers. 
Create text for .json file with table of that questions with the following structure: 
{{"questions": [
 {{
"Question ID": "ID of question in the database",
"Certification_short" : "CIA",
"Certification": "Certified Internal Auditor (CIA)",
"Exam_part": 1,
"Question Number": "A unique identifier for each question",
"Question Text": "The content of the question itself",
"Option A": "First possible answer",
"Option B": "Second possible answer",
"Option C": "Third possible answer",
"Option D": "Fourth possible answer",
"Correct Answer": "The correct option (e.g., A, B, C, or D)",
"Explanation": "Detailed explanation why the answer is correct",
"Tips": "Tips how to best prepare for the topic",
"Category": "The specific topic or area the question covers, aligned with the CIA exam syllabus",
"Model": "{model}",
"Creator": "Alexander",
"Create_date": "{datetime.now()}",
"Number of attempts": 0,
"Number of correct answers": 0,
"Percentage of correct answers": 0
 }},
...
]
}}
Questions should strictly adhere to original exam by difficulty and knowledge areas. Some of questions should be long and based on scenarios. Other questions should refer to international auditing standards.

Make questions longer and more complicated.
Do not provide sample of questions, generate complete file immediately. File must contain 5 questions
"""
# prompt = """
#     What is CIA?
# """

# Send the request to G4F using the appropriate model
response = g4f.ChatCompletion.create(
	model=model,
	messages=[{"role": "user", "content": prompt}],
	# provider=g4f.Provider.Bing,
	cookies={"AEC": "AQTF6HwDOgQfJEAm-8C8KQGKxwMVkpEW0JnVuz4fb4F03Lpzx_1cSi_7UA", 
			 "NID": "514=wGTh-5ihv-BjWAq_MmzzV_XrX_cRv5B0EhlidBeFSl_KdbXFoxUFUvJfmySCjM2UtWAfItlV4ICz_XGmYde2zY25Y6SwEaLgMeot5zDuMKrFJlPapPvt7Z8FRkQNfKDJJ6GhweqglEZZ8Nq7ufneY58wSaKP5DRcmHRA_JmwVCQ"},
	stream=True,
	auth=True,
)


text = ''
for message in response:
	text += message
#     print(message, flush=True, end='')
# print(response)
print('text =', text)

def load_json_data(json_str):
	try:
		data = json.loads(json_str)
		return data
	except json.JSONDecodeError as e:
		print(f"Error decoding JSON: {e}")
		return None


# Function to insert data using raw SQL
def insert_questions(questions):
	insert_query = """
	INSERT INTO cia_questions (
		certification_short, certification, exam_part, question_number, question_text,
		option_a, option_b, option_c, option_d, correct_answer, explanation, tips,
		category, model, creator, create_date, number_of_attempts, number_of_correct_answers, 
		percentage_of_correct_answers)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
	"""

	with engine.connect() as connection:
		for q in questions:
			print('q =', q)
			# Format the create_date string into a datetime object
			create_date = datetime.strptime(q['Create_date'], '%Y-%m-%d %H:%M:%S.%f')
			# Execute the query with the provided data
			connection.execute(insert_query, (
				q['Certification_short'], q['Certification'], q['Exam_part'], q['Question Number'],
				q['Question Text'], q['Option A'], q['Option B'], q['Option C'], q['Option D'],
				q['Correct Answer'], q['Explanation'], q['Tips'], q['Category'], q['Model'],
				q['Creator'], create_date, q['Number of attempts'], q['Number of correct answers'],
				q['Percentage of correct answers']
			))
	

questions = load_json_data(text)
if questions:
	print('questions =', questions)
insert_questions(questions)