
from AI.openai_tools_pydantic import process_person_data

path = f'evaluation_json/generated_json_gpt4o/try1/ocr_text/'
volume = 'vol1'
process_person_data(path, volume)

