import time
from generate_3_5_turbo_1_question import generate
# from openai_api import generate

if __name__ == "__main__":
    counter = 0
    while counter < 100:
        try:
            generate()
            counter += 1
            time.sleep(5)
            print("Сгенерировано вопросов: ", counter)
        except:
            pass