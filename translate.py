import requests
import os
import pprint
import chardet
from chardet.universaldetector import UniversalDetector
from pprint import pprint

API_KEY = 'trnsl.1.1.20180620T193545Z.3444149a9187659f.c0672693a0ce43a31d917b5bf5c57e0a05ecece0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate():
    detector = UniversalDetector()
    source = 'Source'
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), source)
    file_list = os.listdir(path)

    result_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Result')

    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    print("Для перевода доступны следующиее файлы:")
    for i in file_list:
        print(i)

    file_name = input('Укажите, какой файл из указанных выше Вы хотитк перевести:')
    file_path = os.path.join(path, file_name)

    with open(file_path, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        code_type = detector.result['encoding']
        print('Файл {} выполнен в кодировке {}' .format(file_name, code_type))

    to_lang = os.path.basename(file_path).lower()[0]+os.path.basename(file_path).lower()[1]

    with open(file_path, encoding=code_type) as translate_file:
        params = {
            'key': API_KEY,
            'text': translate_file,
            'lang': '{}-ru'.format(to_lang)
        }
        response = requests.get(URL, params=params)
        json_ = response.json()

        with open(os.path.join(result_folder, 'Translate_{}'.format(file_name)), 'w', encoding='utf-8') as new_file:
            new_file.write(''.join(json_['text']))
        print('Результат перевода:')
        with open(os.path.join(result_folder, 'Translate_{}'.format(file_name)), 'r', encoding='utf-8') as read_result:
            for line in read_result:
                pprint(line)


translate()
