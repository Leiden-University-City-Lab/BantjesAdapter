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


# Load the texts from the files
with open('sample_text_corrected/1.vol5txt.txt', 'r') as f:
    reference_text = f.read().strip().lower()

with open('sample_text_original/1.vol5txt.txt', 'r') as f:
    ocr_text = f.read().strip().lower()

# Calculate CER and WER
character_error_rate = cer(reference_text, ocr_text)
word_error_rate = wer(reference_text, ocr_text)

print(f"Character Error Rate (CER): {character_error_rate:.2%}")
print(f"Word Error Rate (WER): {word_error_rate:.2%}")
