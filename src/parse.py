import csv
import re
import pandas as pd


def parse_transcription_csv(input_path, output_path):
    pattern = re.compile(r'\[(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})]  (.*)')

    parsed_data = []

    with open(input_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            line = ''.join(row) 
            match = pattern.match(line)
            if match:
                start_time = match.group(1)
                end_time = match.group(2)
                text = match.group(3)

                parsed_data.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'text': text
                })

    df = pd.DataFrame(parsed_data)
    df.to_csv(output_path, index=False)
    print("done")
    return df

