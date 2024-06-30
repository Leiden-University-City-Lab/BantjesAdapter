from AI.openai_tools_pydantic import process_person_data


def main(path, volume):
    process_person_data(path, volume)


if __name__ == "__main__":
    main(f'evaluation_json/generated_jsons/correct_text/', 'vol1')
