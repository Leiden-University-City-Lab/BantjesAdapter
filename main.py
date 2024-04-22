from database.queries import query_person

# def ocr_persons_from_images():
# def extract_person_data_with_re(): >> generated dictionary
# def search_person_in_database():

# one of:
# def update_person_in_database():
# def create_person_in_database():


def get_person():
    person = query_person()
    return person


def main():
    data = get_person()
    print(data)


if __name__ == "__main__":
    main()
