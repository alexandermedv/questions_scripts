from openai import OpenAI
import json
from config import gpt_model, questions_db, openai_api_key
from datetime import datetime
from sqlalchemy import create_engine, text as sqlalch_text

client = OpenAI(api_key=openai_api_key)
engine = create_engine(questions_db)

def load_json_data(json_str):
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    
# Function to insert data using raw SQL
def insert_questions(q):
 
    insert_query = sqlalch_text(
        "INSERT INTO questions.questions ("
        " certification_short, certification, exam_part, domain,"
        "question_text, option_a, option_b, option_c, option_d,"
        "correct_answer, explanation, tips, category, model, creator, create_date,"
        "number_of_attempts, number_of_correct_answers, percentage_of_correct_answers)"
    "VALUES ("
        ":certification_short, :certification, :exam_part, :domain,"
        ":question_text, :option_a, :option_b, :option_c, :option_d,"
        ":correct_answer, :explanation, :tips, :category, :model, :creator, :create_date,"
        ":number_of_attempts, :number_of_correct_answers, :percentage_of_correct_answers);"
    )

    with engine.connect() as connection:
        # print('q =', q)
        # Format the create_date string into a datetime object
          if q:
            create_date = datetime.strptime(q['create_date'], '%Y-%m-%d %H:%M:%S.%f')
            # Execute the query with the provided data
            connection.execute(insert_query, q)
            connection.commit()


def generate():

  response = client.chat.completions.create(
    model=gpt_model,
    messages=[
      {"role": "system", "content": "You are a tutor for exams on certification in risks and internal audit area."},
      {"role": "user", "content": f"""
      Write 1 test question to prepare for CIA exam part one. Question should have 4 answers. 
      Create text for .json file with question with the following structure: 
      {{
      "question_id": "ID of question in the database",
      "certification_short" : "CIA",
      "certification": "Certified Internal Auditor (CIA)",
      "exam_part": 1,
      "domain": "Knowledge area, aligned with the exam syllabus",
      "question_text": "The content of the question itself",
      "option_a": "First possible answer",
      "option_b": "Second possible answer",
      "option_c": "Third possible answer",
      "option_d": "Fourth possible answer",
      "correct_answer": "The correct option (e.g., A, B, C, or D)",
      "explanation": "Detailed explanation why the answer is correct",
      "tips": "Tips how to best prepare for the topic",
      "category": "The specific topic or area the question covers, aligned with the exam syllabus",
      "model": "{gpt_model}",
      "creator": "Alexander",
      "create_date": "{datetime.now()}" (current date as timestamp without timezone in format '%Y-%m-%d %H:%M:%S.%f'),
      "number_of_attempts": 0,
      "number_of_correct_answers": 0,
      "percentage_of_correct_answers": 0
      }}

      Question should strictly adhere to original exam by difficulty and knowledge areas. Some of questions should be long and based on scenarios. Other questions should refer to international auditing standards. Some questions may require calculations.

      Make questions longer and more complicated.
      Send only text of json file as a response, no comments required.
      """
      }
    ]
  )

  text_full = response.choices[0].message.content
  print('text_full[:7] =', text_full[:7])
  if text_full[:7] == "```json":
        start = 8
  else:
        start = 0

  print('text_full[-3:] =', text_full[-3:])
  if text_full[-3:] == "```":
        end = len(text_full) - 3
  else:
        end = len(text_full)

  text = text_full[start:end].strip()
  print('text =', text)

  questions = load_json_data(text)
  if questions:
      questions['create_time'] = datetime.now()
      print('questions =', questions)
      insert_questions(questions)
  

  return 


# print(response.choices[0].message.content)

if __name__ == "__main__":
    generate()