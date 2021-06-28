import os
import json
import objectpath
from pathlib import Path 
import string
from collections import Counter

def extract_logs(filepath):

    """ This function takes a json file of Google Dialogflow logs and extracts the user inputs with their frequencies.

    Input: filepath for a json file in string format

    Returns:
        .txt file: user inputs with their frequencies
    """

    # Extract the main user input info which is under the 'textPayload' field and return as a list
    with open(filepath, encoding ='utf-8') as f:
        data = json.load(f)
        json_tree = objectpath.Tree(data)
        result_list = list(json_tree.execute('$..textPayload'))

    # Example element in the result_list: 'Dialogflow Request : {"session":"0.p80scpt1cn",
    # "query_input":"{\\n  \\"text\\": {\\n    \\"textInputs\\": [{\\n      \\"text\\": \\"Hi\\"\\n    }]\\n  }\\n}",
    # "timezone":"America/Los_Angeles"}'

    # Create empty list
    results = []

    # Get user input from the second 'text' field under 'query_input' field
    for result in result_list:
        start_length = len('Dialogflow Request : ')
        if result.startswith('Dialogflow Request'):     
            text_first = result[start_length:]                  # Get the string within the first curly bracket after 'Dialogflow Request'
            dictionary_first = json.loads(text_first)           # Create a dictionary format from the first text
            text_second = dictionary_first['query_input']       # Get the string within the first curly bracket after 'query_input'
            dictionary_second = json.loads(text_second)         # Create a dictionary format from the second text
            json_tree = objectpath.Tree(dictionary_second)      # Extract user input text
            result_second = list(json_tree.execute('$..text'))

            if result_second:
                result_second[1] = result_second[1].lower()     # Bring it to the lower case
                result_second[1] = ''.join([char for char in result_second[1] if char not in string.punctuation]) # Remove punctuation
                results.append(result_second[1])  

    value_counts = Counter(results)       # Counts of user inputs
    temp_output = value_counts.most_common()
    temp_output = '\n'.join([str(item) for item in temp_output])

    # Save the output as a .txt file
    with open('user_input_frequencies.txt', mode='wt', encoding = 'utf-8') as output:
        output.write(str(temp_output))

    return