import re, json, time, os

def find_duplicates(input_list):
    # Count occurrences of each item
    count_dict = {}
    for item in input_list:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1

    # Filter items that appear more than once
    duplicates = [item for item, count in count_dict.items() if count > 1]

    return duplicates

def replace_multiple_whitespaces_with_single(text):
    # Replace one or more whitespace characters (\s+) with a single space
    return re.sub(r'\s+', ' ', text)

def date_to_str(today):
    return today.strftime("%m_%d_%Y").lower()

def dump(path, data, wait=False):
    with open(path, "w+", encoding="utf8") as file:
        if wait:
            time.sleep(3)
        file.write(json.dumps(data, ensure_ascii=False, indent=4))

def load(path):
    with open(path, "r") as file:
        return json.load(file)