import os
import json
import csv

# Paths to the directories containing the JSON files
correct_dir = "correct"
generated_dir = "generated_ocr_json"


# Function to compare JSON files and calculate accuracy
def compare_json_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    total_keys = len(data1)
    correct_new_person = 0
    correct_maybe_same_person = 0
    correct_person_id = 0
    should_new_person = 0
    generated_new_person = 0
    should_maybe_same_person = 0
    generated_maybe_same_person = 0

    for key in data1:
        if key not in data2:
            continue

        should_new_person += data1[key]['new_person']
        generated_new_person += data2[key]['new_person']

        should_maybe_same_person += data1[key]['maybe_same_person']
        generated_maybe_same_person += data2[key]['maybe_same_person']

        if data1[key]['new_person'] == data2[key]['new_person']:
            correct_new_person += 1
            if data1[key]['new_person'] or data1[key]['person_id'] == data2[key]['person_id']:
                correct_person_id += 1

        if data1[key]['maybe_same_person'] == data2[key]['maybe_same_person']:
            correct_maybe_same_person += 1

    accuracy_new_person = correct_new_person / total_keys
    accuracy_maybe_same_person = correct_maybe_same_person / total_keys
    accuracy_person_id = correct_person_id / total_keys

    return (accuracy_new_person, accuracy_maybe_same_person, accuracy_person_id,
            should_new_person, generated_new_person,
            should_maybe_same_person, generated_maybe_same_person)


# Prepare CSV output
csv_output = [["Volume", "Accuracy_Person_ID", "Accuracy_New_Person", "Accuracy_Maybe_Same_Person",
               "Correct_New_Person_Count", "Generated_New_Person_Count",
               "Correct_Maybe_Same_Person_Count", "Generated_Maybe_Same_Person_Count"]]

# Compare files
for i in range(1, 8):
    vol = f"vol{i}.json"
    correct_file = os.path.join(correct_dir, vol)
    generated_file = os.path.join(generated_dir, vol)

    (accuracy_new_person, accuracy_maybe_same_person, accuracy_person_id,
     correct_new_person_count, generated_new_person_count,
     correct_maybe_same_person_count, generated_maybe_same_person_count) = compare_json_files(correct_file,
                                                                                              generated_file)

    csv_output.append([f"vol{i}", accuracy_person_id, accuracy_new_person, accuracy_maybe_same_person,
                       correct_new_person_count, generated_new_person_count,
                       correct_maybe_same_person_count, generated_maybe_same_person_count])

# Write to CSV file
with open('accuracy_scores_ocr.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_output)

print("CSV file 'accuracy_scores.csv' has been generated.")
