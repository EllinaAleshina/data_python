import pandas as pd
import re
import pymorphy2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# загружаем датесет
data = pd.read_csv('/Users/ellinaalesina/Downloads/Данные для задания.csv', encoding='UTF-8', sep=';')
print('Алешина Эллина')

# Функция для очистки текста
def clean_text(text):
    # приводим текст к нижнему регистру
    text = text.lower()
    # создаем регулярное выражение для удаления лишних символов
    regular = r'[^\w\s]|[\d]|[a-z]|[A-Z]|[_]'
    text = re.sub(regular, ' ', text)
    # удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text)
    # возвращаем очищенные данные
    return text


# создаем список для хранения преобразованных данных
processed_text = []
# загружаем стоп-слова для английского языка
stop_words = stopwords.words('russian')
# РАБОТА СО СПИСКОМ СТОП-СЛОВ
# print(stop_words) # вывод списка стоп-слов на экран
print('Хотите ли Вы дополнить список стоп-слов? Ответьте Да или Нет:')
if input() == 'Да':
    print('Введите стоп-слово:')
    stop_words.append(input())# добавление слова в список стоп-слов
# stop_words.remove('и')# удаление слова из списка стоп-слов
# инициализируем лемматайзер
pymorph = pymorphy2.MorphAnalyzer()

# для каждого сообщения text из столбца data['Message']
for text in data['url,author,type,parent_post_url,tag,body']:
    # cleaning
    text = clean_text(text)
    # tokenization
    text = word_tokenize(text)
    # удаление стоп-слов
    text = [word for word in text if word not in stop_words]
    # лемматизация
    text = [pymorph.parse(w)[0].normal_form for w in text]

    # добавляем преобразованный текст в список processed_text
    processed_text.append(text)
top_words = {}
Counts = 0
data['url,author,type,parent_post_url,tag,body'] = processed_text
# print(data['url,author,type,parent_post_url,tag,body'])
k = 0

for w in data['url,author,type,parent_post_url,tag,body'][k]:
    if top_words.get(w) is None:
        for text in data['url,author,type,parent_post_url,tag,body']:
            Counts += text.count(w)
        top_words[w] = Counts
        Counts = 0
    k += 1

result = sorted(top_words.items(), key=lambda t: t[1], reverse=True)
print('Слова и частота их употребления:')
for k, v in result:
    print(k, ':', v)
print('\nТоп 100 слов, встреченных в базе данных:')
n = 1
for k, v in result:
    if n < 101:
        print(n, '.', k)
        n += 1
