import os
import numpy as np
from collections import defaultdict

def levenshtein_distance(ref, hyp):
    ref_len = len(ref)
    hyp_len = len(hyp)

    # Create a matrix to store the distances
    distance_matrix = np.zeros((ref_len + 1, hyp_len + 1), dtype=int)

    for i in range(ref_len + 1):
        distance_matrix[i][0] = i
    for j in range(hyp_len + 1):
        distance_matrix[0][j] = j

    for i in range(1, ref_len + 1):
        for j in range(1, hyp_len + 1):
            if ref[i - 1] == hyp[j - 1]:
                distance_matrix[i][j] = distance_matrix[i - 1][j - 1]
            else:
                distance_matrix[i][j] = min(distance_matrix[i - 1][j] + 1,  # Deletion
                                            distance_matrix[i][j - 1] + 1,  # Insertion
                                            distance_matrix[i - 1][j - 1] + 1)  # Substitution

    return distance_matrix[ref_len][hyp_len]

def cer(ref, hyp):
    # Calculate CER
    ref = list(ref)
    hyp = list(hyp)
    distance = levenshtein_distance(ref, hyp)
    return distance / len(ref)

def wer(ref, hyp):
    # Calculate WER
    ref = ref.split()
    hyp = hyp.split()
    distance = levenshtein_distance(ref, hyp)
    return distance / len(ref)

def process_directory(correct_dir, generated_dir):
    volume_data = defaultdict(lambda: {'cer_scores': [], 'wer_scores': []})

    for filename in os.listdir(correct_dir):
        if filename.endswith('.txt'):
            correct_filepath = os.path.join(correct_dir, filename)
            generated_filepath = os.path.join(generated_dir, filename)

            if os.path.exists(generated_filepath):
                with open(correct_filepath, 'r') as f:
                    reference_text = f.read().strip().lower()

                with open(generated_filepath, 'r') as f:
                    ocr_text = f.read().strip().lower()

                # Calculate CER and WER for the current file
                cer_score = cer(reference_text, ocr_text)
                wer_score = wer(reference_text, ocr_text)

                # Extract the volume from the filename
                volume = filename.split('vol')[1].split('txt')[0]

                volume_data[volume]['cer_scores'].append(cer_score)
                volume_data[volume]['wer_scores'].append(wer_score)

    # Calculate average CER and WER for each volume
    average_errors = {}
    for volume, scores in volume_data.items():
        average_cer = np.mean(scores['cer_scores'])
        average_wer = np.mean(scores['wer_scores'])
        average_errors[volume] = (average_cer, average_wer)

    return average_errors

# Example usage
correct_directory = 'sample_text_corrected'
generated_directory = 'sample_text_original'

average_errors_per_volume = process_directory(correct_directory, generated_directory)

for volume, (average_cer, average_wer) in average_errors_per_volume.items():
    print(f"Volume {volume} - Average Character Error Rate (CER): {average_cer:.2%}, Average Word Error Rate (WER): {average_wer:.2%}")
