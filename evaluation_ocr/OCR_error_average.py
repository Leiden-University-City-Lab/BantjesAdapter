import os
import numpy as np

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
    cer_scores = []
    wer_scores = []

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

                cer_scores.append(cer_score)
                wer_scores.append(wer_score)

    # Calculate average CER and WER
    average_cer = np.mean(cer_scores)
    average_wer = np.mean(wer_scores)

    return average_cer, average_wer

# Example usage
correct_directory = 'sample_text_corrected'
generated_directory = 'sample_text_original'

average_cer, average_wer = process_directory(correct_directory, generated_directory)

print(f"Average Character Error Rate (CER): {average_cer:.2%}")
print(f"Average Word Error Rate (WER): {average_wer:.2%}")
