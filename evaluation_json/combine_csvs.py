
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def combine_csv_files(csv_files, output_pdf):

    dfs = pd.DataFrame()

    for csv_file in csv_files:

        # Extract try name from file name
        try_name = os.path.splitext(os.path.basename(csv_file))[0]

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        df['run'] = try_name
        df['gpt'] = 35
        df['Correct_Text_Accuracy'] = df['Correct_Text_Accuracy'].str.rstrip('%').astype(float)
        df['OCR_Text_Accuracy'] = df['OCR_Text_Accuracy'].str.rstrip('%').astype(float)

        # Concat rows of the dataframe to the collection
        dfs = pd.concat([df, dfs], ignore_index=True, axis=0)

    # Concatenate all the DataFrames along the columns
    print(dfs)

    # Calculate min, max, range, and mean per category
    summary = dfs.groupby('Category').agg(
        Min_Correct_Text_Accuracy=('Correct_Text_Accuracy', 'min'),
        Max_Correct_Text_Accuracy=('Correct_Text_Accuracy', 'max'),
        Range_Correct_Text_Accuracy=('Correct_Text_Accuracy', lambda x: x.max() - x.min()),
        Mean_Correct_Text_Accuracy=('Correct_Text_Accuracy', 'mean'),
        Min_OCR_Text_Accuracy=('OCR_Text_Accuracy', 'min'),
        Max_OCR_Text_Accuracy=('OCR_Text_Accuracy', 'max'),
        Range_OCR_Text_Accuracy=('OCR_Text_Accuracy', lambda x: x.max() - x.min()),
        Mean_OCR_Text_Accuracy=('OCR_Text_Accuracy', 'mean')
    ).reset_index()

    # Print the summary DataFrame
    print(summary)

    # Extract categories, min values, and max values
    categories = summary['Category']
    min_correct_values = summary['Min_Correct_Text_Accuracy']
    max_correct_values = summary['Max_Correct_Text_Accuracy']
    mean_correct_values = summary['Mean_Correct_Text_Accuracy']

    min_ocr_values = summary['Min_OCR_Text_Accuracy']
    max_ocr_values = summary['Max_OCR_Text_Accuracy']
    mean_ocr_values = summary['Mean_OCR_Text_Accuracy']

    # Width of the bars
    x = np.arange(len(categories))

    # Create the plot
    fig, ax = plt.subplots()

    # Plot min-max area and the mean for Correct Text Accuracy
    ax.fill_between(x, min_correct_values, max_correct_values, color='blue', alpha=0.2, label='Range Correct Text Accuracy')
    ax.plot(x, mean_correct_values, color='purple', linestyle='-', linewidth=2, label='Mean Correct Text Accuracy')

    # Plot min-max area and the mean for OCR Text Accuracy
    ax.fill_between(x, min_ocr_values, max_ocr_values, color='green', alpha=0.2, label='Range OCR Text Accuracy')
    ax.plot(x, mean_ocr_values, color='brown', linestyle='-', linewidth=2, label='Mean OCR Text Accuracy')

    # Add labels and title
    ax.set_xlabel('Categories')
    ax.set_ylabel('Percentage')
    ax.set_title('Correct Interpretations per Category with chatGPT3.5')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend()

    # Write the plot to a new pdf file
    plt.plot()
    plt.savefig(output_pdf, dpi=600, format='pdf')

    # Show the plot
    plt.tight_layout()
    plt.show()


# List of CSV files to combine
csv_files = [
    'generated_json_gpt35/accuracy_try1.csv',
    'generated_json_gpt35/accuracy_try2.csv',
    'generated_json_gpt35/accuracy_try3.csv',
    'generated_json_gpt35/accuracy_try4.csv',
    'generated_json_gpt35/accuracy_try5.csv'
]

# Output pdf file
output_pdf = 'generated_json_gpt35/combined_accuracy_results_gtp35.pdf'
combine_csv_files(csv_files, output_pdf)


