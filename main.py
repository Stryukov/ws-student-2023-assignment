import requests
import json


URL = 'https://raw.githubusercontent.com/thewhitesoft/student-2023-assignment/main/data.json'
REPLACEMENT = 'replacement.json'


def get_messages(url: str) -> dict:
    """
    Get data from URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return {'status': True, 'data': response.json()}
    except requests.exceptions.RequestException as error:
        return {'status': False, 'data': error}


def clear_replacement(replacements: dict) -> dict:
    """
    Remove not unique item from replacement and repeated replacemaent.
    """
    new_replacement = []
    unique_replacement = set()

    for item in replacements[::-1]:
        if item['replacement'] not in unique_replacement:
            unique_replacement.add(item['replacement'])
            new_replacement.append(item)
    return new_replacement


def repair_messages(data: list, replacement: list) -> list:
    """
    Text message recovery.
    """
    count_messages = len(data) - 1
    index = 0
    while index <= count_messages:
        for item in replacement:
            if data[index].find(item['replacement']) != -1:
                if not item['source']:
                    source = ''
                else:
                    source = item['source']
                data[index] = data[index].replace(item['replacement'], source)

        # remove empty message
        if not len(data[index]):
            data.pop(index)
            count_messages -= 1
        else:
            index += 1
    return data


def main() -> None:
    # get data
    response = get_messages(URL)
    if not response['status']:
        print('Error: ', response['data'])
    data = response['data']

    # get replacement
    with open(REPLACEMENT, 'r') as file:
        replacement = json.load(file)
    replacement = clear_replacement(replacement)

    # recovery and save data
    recovery_message = repair_messages(data, replacement)
    with open('result.json', 'w') as file:
        json.dump(recovery_message, file)


if __name__ == '__main__':
    main()
