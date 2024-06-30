import json
import os
from collections import defaultdict

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def compare_values(correct, generated, path=''):
    correct_values = 0
    total_values = 0
    key_accuracies = defaultdict(lambda: [0, 0, 0])  # Dictionary to store correct, total, and empty match counts for each key path

    if isinstance(correct, dict) and isinstance(generated, dict):
        correct = {k.lower(): v for k, v in correct.items()}
        generated = {k.lower(): v for k, v in generated.items()}

        for key in correct:
            if key in generated:
                corr, total, key_acc = compare_values(correct[key], generated[key], path + key + '.')
                correct_values += corr
                total_values += total
                for k, v in key_acc.items():
                    key_accuracies[k][0] += v[0]
                    key_accuracies[k][1] += v[1]
                    key_accuracies[k][2] += v[2]
            else:
                key_accuracies[path + key][1] += 1  # Missing key
                total_values += 1
        for key in generated:
            if key not in correct:
                key_accuracies[path + key][1] += 1  # Extra key
                total_values += 1
    elif isinstance(correct, list) and isinstance(generated, list):
        for item1, item2 in zip(correct, generated):
            corr, total, key_acc = compare_values(item1, item2, path)
            correct_values += corr
            total_values += total
            for k, v in key_acc.items():
                key_accuracies[k][0] += v[0]
                key_accuracies[k][1] += v[1]
                key_accuracies[k][2] += v[2]
        for _ in range(len(correct), len(generated)):
            key_accuracies[path + '[]'][1] += 1  # Extra list items
            total_values += 1
        for _ in range(len(generated), len(correct)):
            key_accuracies[path + '[]'][1] += 1  # Missing list items
            total_values += 1
    else:
        if isinstance(correct, str) and isinstance(generated, str):
            correct = correct.lower()
            generated = generated.lower()

        if correct == generated:
            correct_values += 1
            key_accuracies[path][0] += 1
        key_accuracies[path][1] += 1
        total_values += 1

        # Check for empty values
        correct_is_empty = correct in [None, [], '']
        generated_is_empty = generated in [None, [], '']
        if correct_is_empty and generated_is_empty:
            key_accuracies[path][2] += 1

    return correct_values, total_values, key_accuracies

def compare_json_files(correct_folder, generated_folder):
    total_correct = 0
    total_count = 0
    total_empty_match = 0
    overall_key_accuracies = defaultdict(lambda: [0, 0, 0])  # Dictionary to store overall correct, total, and empty match counts for each key

    for file_name in os.listdir(correct_folder):
        if file_name.endswith('.json'):
            correct_file_path = os.path.join(correct_folder, file_name)
            generated_file_path = os.path.join(generated_folder, file_name)

            if os.path.exists(generated_file_path):
                correct_json = load_json(correct_file_path)
                generated_json = load_json(generated_file_path)

                correct_values, total_values, key_accuracies = compare_values(correct_json, generated_json)
                total_correct += correct_values
                total_count += total_values
                for key, value in key_accuracies.items():
                    overall_key_accuracies[key][0] += value[0]
                    overall_key_accuracies[key][1] += value[1]
                    overall_key_accuracies[key][2] += value[2]
                    total_empty_match += value[2]

    accuracy = (total_correct / total_count) * 100 if total_count > 0 else 0
    empty_match_score = (total_empty_match / total_count) * 100 if total_count > 0 else 0
    return accuracy, empty_match_score, overall_key_accuracies

def categorize_key(key):
    categories = {
        'grand_parents': 'grand_parents',
        'children': 'children',
        'education': 'education',
        'careers': 'careers',
        'particularities': 'particularities',
        'spouses': 'spouses',
        'parents': 'parents',
        'in_laws': 'in_laws',
        'far_family': 'far_family',
        '': 'main_person'  # Keys that do not start with any specific category
    }
    for category in categories:
        if key.startswith(category + '.'):
            return categories[category]
    return 'main_person'

def collect_accuracy_data(correct_folder, generated_folder):
    _, _, key_accuracies = compare_json_files(correct_folder, generated_folder)

    category_accuracies = defaultdict(lambda: [0, 0, 0])  # To store correct, total, and empty match counts for each category
    for key, (correct, total, empty_match) in key_accuracies.items():
        category = categorize_key(key)
        if category:
            category_accuracies[category][0] += correct
            category_accuracies[category][1] += total
            category_accuracies[category][2] += empty_match

    return category_accuracies

def report_accuracy_per_volume(correct_root_folder, generated_root_folder):
    volumes = os.listdir(correct_root_folder)
    all_results = defaultdict(lambda: {'correct_text': [0, 0, 0], 'ocr_text': [0, 0, 0]})

    for volume in volumes:
        correct_folder = os.path.join(correct_root_folder, volume)
        generated_folder_correct_text = os.path.join(generated_root_folder, 'correct_text', volume)
        generated_folder_ocr_text = os.path.join(generated_root_folder, 'ocr_text', volume)

        if os.path.isdir(correct_folder) and os.path.isdir(generated_folder_correct_text) and os.path.isdir(generated_folder_ocr_text):
            print(f'\nVolume: {volume}')

            category_accuracies_correct_text = collect_accuracy_data(correct_folder, generated_folder_correct_text)
            category_accuracies_ocr_text = collect_accuracy_data(correct_folder, generated_folder_ocr_text)

            print('\nResults for Correct Text Files:')
            for category, (correct, total, empty_match) in category_accuracies_correct_text.items():
                category_accuracy = (correct / total) * 100 if total > 0 else 0
                category_empty_match = (empty_match / total) * 100 if total > 0 else 0
                all_results[category]['correct_text'][0] += correct
                all_results[category]['correct_text'][1] += total
                all_results[category]['correct_text'][2] += empty_match
                print(f'{category.capitalize()}: Accuracy: {category_accuracy:.2f}%, Empty Match: {category_empty_match:.2f}%')

            print('\nResults for OCR Text Files:')
            for category, (correct, total, empty_match) in category_accuracies_ocr_text.items():
                category_accuracy = (correct / total) * 100 if total > 0 else 0
                category_empty_match = (empty_match / total) * 100 if total > 0 else 0
                all_results[category]['ocr_text'][0] += correct
                all_results[category]['ocr_text'][1] += total
                all_results[category]['ocr_text'][2] += empty_match
                print(f'{category.capitalize()}: Accuracy: {category_accuracy:.2f}%, Empty Match: {category_empty_match:.2f}%')

    print('\nOverall Results Per Category:')
    for category, results in all_results.items():
        correct_text_accuracy = (results['correct_text'][0] / results['correct_text'][1]) * 100 if results['correct_text'][1] > 0 else 0
        correct_text_empty_match = (results['correct_text'][2] / results['correct_text'][1]) * 100 if results['correct_text'][1] > 0 else 0
        ocr_text_accuracy = (results['ocr_text'][0] / results['ocr_text'][1]) * 100 if results['ocr_text'][1] > 0 else 0
        ocr_text_empty_match = (results['ocr_text'][2] / results['ocr_text'][1]) * 100 if results['ocr_text'][1] > 0 else 0

        print(f'\nCategory: {category.capitalize()}')
        print(f'Correct Text Files: Accuracy: {correct_text_accuracy:.2f}%, Empty Match: {correct_text_empty_match:.2f}%')
        print(f'OCR Text Files: Accuracy: {ocr_text_accuracy:.2f}%, Empty Match: {ocr_text_empty_match:.2f}%')


correct_root_folder = 'correct_json'
generated_root_folder = 'generated_jsons'
report_accuracy_per_volume(correct_root_folder, generated_root_folder)
