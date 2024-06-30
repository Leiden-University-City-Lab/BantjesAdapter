import json
import os
from collections import defaultdict


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def compare_values(correct, generated, path=''):
    correct_values = 0
    total_values = 0
    key_accuracies = defaultdict(
        lambda: [0, 0, 0])  # Dictionary to store correct, total, and empty match counts for each key path

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
    overall_key_accuracies = defaultdict(
        lambda: [0, 0, 0])  # Dictionary to store overall correct, total, and empty match counts for each key

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


def report_accuracy(correct_folder, generated_folder):
    accuracy, empty_match_score, key_accuracies = compare_json_files(correct_folder, generated_folder)
    print(f'Overall value accuracy: {accuracy:.2f}%')
    print(f'Average empty match score: {empty_match_score:.2f}%')

    category_accuracies = defaultdict(
        lambda: [0, 0, 0])  # To store correct, total, and empty match counts for each category

    print('\nAccuracy per key:')
    for key, (correct, total, empty_match) in key_accuracies.items():
        key_accuracy = (correct / total) * 100 if total > 0 else 0
        empty_match_percentage = (empty_match / total) * 100 if total > 0 else 0
        print(
            f'{key}: {key_accuracy:.2f}% ({correct}/{total}), Empty Match: {empty_match_percentage:.2f}% ({empty_match}/{total})')

        category = categorize_key(key)
        if category:
            category_accuracies[category][0] += correct
            category_accuracies[category][1] += total
            category_accuracies[category][2] += empty_match

    print('\nAverage accuracy and null score per category:')
    for category, (correct, total, empty_match) in category_accuracies.items():
        category_accuracy = (correct / total) * 100 if total > 0 else 0
        category_empty_match = (empty_match / total) * 100 if total > 0 else 0
        print(f'{category.capitalize()}: Accuracy: {category_accuracy:.2f}%, Empty Match: {category_empty_match:.2f}%')


correct_folder = 'correct_json/vol7'
# generated_folder = 'correct_text/vol7'
generated_folder = 'correct_text/vol7'
# correct_folder = 'test/correct'
# generated_folder = 'test/gen'
report_accuracy(correct_folder, generated_folder)
