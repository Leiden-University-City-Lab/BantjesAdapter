from AI.openai_tools_pydantic import process_person_data


def main(path, volume):
    # Run the data processing
    process_person_data(path, volume)


if __name__ == "__main__":
    path = f'evaluation_json/generated_json/try1/ocr_text/'
    volume = 'vol1'
    main(path, volume)
