# -*- coding: utf8 -*-

# Импортируем библиотеки
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import pandas as pd
from pytz import timezone

# Списки для обработки запросов
tasklist = []
tasklist2 = []
tasklist3_1 = []
tasklist3_2 = []
tasklist3_3 = []
tasklist3_4 = []


class helloHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path.endswith('/tasklist'): # Страница с методами

            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Task List</h1>'
            output += '<h3><a href="/tasklist/task_1">Task_1</a></h3>'
            output += '<h3><a href="/tasklist/task_2">Task_2</a></h3>' 
            output += '<h3><a href="/tasklist/task_3">Task_3</a></h3>' 
            output += '</body></html>'

            self.wfile.write(output.encode())


        if self.path.endswith('/task_1'):     # Вывод для 1 задания

            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Task 1</h1>'
            output += '<meta charset="utf-8">'

            output += '<form method="POST" enctype="multipart/form-data" action="/task_1">'
            output += '<input name="task" type="text" placeholder="geonameid">'
            output += '<input type="submit" value="Go">'
            output += '</form>'

            if len(tasklist) > 0:
                output += '<table border="1">'
                output += '<caption>Information about town</caption>'
                output += '<tr>'
                for column in columns:
                    output += '<th>'
                    output += column
                    output += '</th>'
                output += '</tr>'
                output += '<tr>'
                for cell in tasklist:
                    output += '<th>'
                    output += '<meta charset="utf-8">'
                    output += cell
                    output += '</th>'
                output += '</tr>'
                output += '</table>'

            output += '<h5><a href="/tasklist">Вернуться к списку методов</a></h5>'

            self.wfile.write(output.encode())


        if self.path.endswith('/task_2'):     # Вывод для второго задания

            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<meta charset="utf-8">'
            output += '<h1>Task 2</h1>'

            output += '<form method="POST" enctype="multipart/form-data" action="/task_2">'
            output += '<input name="task2_1" type="text" placeholder="page number">'
            output += '<input name="task2_2" type="text" placeholder="towns on page">'
            output += '<input type="submit" value="Go">'
            output += '</form>'

            if len(tasklist2) > 0:
                output += '<table border="1">'
                output += '<caption>Information about towns</caption>'
                output += '<tr>'
                for column in columns:
                    output += '<th>'
                    output += column
                    output += '</th>'
                output += '</tr>'
                output += '<tr>'
                for row in tasklist2:
                    for cell in row:
                        output += '<th>'
                        output += '<meta charset="utf-8">'
                        output += str(cell)
                        output += '</th>'
                    output += '</tr>'
                output += '</table>'

            output += '<h5><a href="/tasklist">Вернуться к списку методов</a></h5>'
            output += '</body></html>'

            self.wfile.write(output.encode())


        if self.path.endswith('/task_3'):  # Вывод для третьего задания

            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<meta charset="utf-8">' 
            output += '<h2>Выберите город:</h2>' 

            output += '<form method="POST" enctype="multipart/form-data" action="/task_3" accept-charset="utf-8">'
            # Первое поле ввода
            output += '<input name="task3_town1" type="text" input list="towns" placeholder="town1">'
            # второе поле
            output += '<input name="task3_town2" type="text" input list="towns" placeholder="town2">'
            
            output += '<input type="submit" value="Go">'

            # Выпадающий список городов

            output += '<datalist id="towns">'
            output += str(''.join(['<option value="'+str(x)+'"></option>' for x in unique_russian_names]))
            output += '</datalist>'

            output += '</form>'

            # Вывод таблицы с информацией

            if len(tasklist3_1) > 0:
                output += '<table border="1">'
                output += '<caption>Information about towns</caption>'
                output += '<tr>'
                for column in columns:
                    output += '<th>'
                    output += column
                    output += '</th>'
                output += '</tr>'
                output += '<tr>'
                for cell in tasklist3_1:
                    output += '<th>'
                    output += '<meta charset="utf-8">'
                    output += cell
                    output += '</th>'
                output += '</tr>'

                if len(tasklist3_2) > 0:
                    output += '<tr>'
                    for cell in tasklist3_2:
                        output += '<th>'
                        output += '<meta charset="utf-8">'
                        output += cell
                        output += '</th>'

            output += '</tr>'
            output += '</table>'

            if len(tasklist3_3)>0:
                output += '<h3>'
                output += tasklist3_3[0] + tasklist3_3[1] + tasklist3_3[2]
                output += '</h3>'

            if len(tasklist3_4)>0:
                output += '<h3>'
                output += " ".join(tasklist3_4)
                output += '</h3>'

            output += '<h5><a href="/tasklist">Вернуться к списку методов</a></h5>'
            output += '</body></html>'

            self.wfile.write(output.encode())


    def do_POST(self): # Обработка post запросов

        # Метод 1
        if self.path.endswith('/task_1'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task = fields.get('task')
                geonameid = new_task[0]
                try:
                    geonameid = int(geonameid)
                except:
                    pass
                if geonameid in df['geonameid'].values:
                    tasklist.clear()
                    df_town_index = df[df['geonameid'] == geonameid].index[0]

                    for cell in df.loc[df_town_index,:].values.tolist():
                        tasklist.append(str(cell))

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/task_1')
            self.end_headers()

        # Метод 2
        if self.path.endswith('/task_2'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task = fields.get('task2_1')
                new_task2 = fields.get('task2_2')
                page_num = new_task[0]
                towns_on_page = new_task2[0]
                tasklist2.clear()
                try:
                    page_num = int(page_num)
                    towns_on_page = int(towns_on_page)
                    start = (page_num-1)*towns_on_page
                    end = start + towns_on_page
                    list_of_lists_with_info = df[start:end].values.tolist()
                    for row in list_of_lists_with_info:
                        tasklist2.append(row)
                except:
                    pass


            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/task_2')
            self.end_headers()

        # Метод 3
        if self.path.endswith('/task_3'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task1 = fields.get('task3_town1')
                new_task2 = fields.get('task3_town2')
                new_town1 = new_task1[0]
                new_town2 = new_task2[0]

                # Вывод информации о первом городе
                try:
                    new_town1 = str(new_town1)
                    if new_town1 in unique_russian_names:
                        tasklist3_1.clear()
                        town_max_pop1 = df[df['russian_name'] == new_town1]["population"].max() 
                        max_town_index1 = df[(df['russian_name']==new_town1) & (df['population'] == town_max_pop1)].sample(1).index.values[0]
                        for cell in df.loc[max_town_index1, :]:
                            tasklist3_1.append(str(cell))
                except:
                    pass

                # Вывод информации о втором городе
                try:
                    new_town2 = str(new_town2)
                    if new_town2 in unique_russian_names:
                        tasklist3_2.clear()
                        town_max_pop2  = df[df['russian_name'] == new_town2]["population"].max() 
                        max_town_index2 = df[(df['russian_name'] == new_town2) & (df['population'] == town_max_pop2)].sample(1).index.values[0]
                        for cell in df.loc[max_town_index2, :]:
                            tasklist3_2.append(str(cell))
                        

                        # Определяем какой город севернее
                        tasklist3_3.clear()
                        if df.loc[max_town_index1, 'latitude'] > df.loc[max_town_index2, 'latitude']:
                            tasklist3_3.append(str(new_town1))
                            tasklist3_3.append(' севернее, чем ')
                            tasklist3_3.append(str(new_town2))
                        else:
                            tasklist3_3.append(str(new_town2))
                            tasklist3_3.append(' севернее, чем ')
                            tasklist3_3.append(str(new_town1))

                        # Временные зоны
                        tasklist3_4.clear()
                        if df.loc[max_town_index1, 'timezone'] == df.loc[max_town_index2, 'timezone']:
                            tasklist3_4.append("Временные зоны ")
                            tasklist3_4.append("совпадают")
                        else:
                            tz_town1 = timezone(df.loc[max_town_index1, 'timezone'])
                            tz_town2 = timezone(df.loc[max_town_index2, 'timezone'])
                            difference = tz_diff('2020-09-15', tz_town1, tz_town2)
                            tasklist3_4.append('Временные зоны')
                            tasklist3_4.append('отличаются на')
                            tasklist3_4.append(str(int(difference)))
                            tasklist3_4.append("ч.")
                except:
                    pass

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/task_3')
            self.end_headers()


# Словарь с заменами
slovar_for_composites_more_2 = ({'scz': 'щ', 'shch' : 'щ', 'ja': 'я', 'Scz': 'щ', 'Shch' : 'Щ', 'Ja': 'я'})
slovar_for_composites = ({'zh': 'ж', 'sh': 'ш', 'ch': 'ч', 'ye': 'е','yu': 'ю', 'ya': 'я', 'kh' : 'х', 'ts' : 'ц', 'Ch': 'Ч', 'Zh': 'Ж', 'Sh': 'Ш','Yu': 'Ю', 'Ya': 'Я', 'Ye': 'Е', 'Ts': 'Ц', 'Kh' : 'Х'})
slovar = {'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'ž': 'ж', 'z': 'з', 'i': 'и', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х', 'c': 'ц', 's': 'с', 'y': 'ы', '’': 'ь', "'": 'ь', "’’": 'ъ', '”': 'ъ', 'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е', 'Z': 'З', 'I': 'Й', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'R': 'Р', 'T': 'Т', 'U': 'У', 'Y':'Ы', 'F': 'Ф', 'H': 'Х', 'C': 'Ц', 'S': 'С'}
# алфавиты
list_of_consonant = set(['б', 'в', 'г', 'д', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'т', 'ф', 'х', 'с'])
list_of_consonant_eng = set(['a', 'b', 'v', 'g', 'd', 'z', 'k', 'l', 'm', 'n', 'p', 'r', 't', 'f', 'h', 'c', 's'])
russian_alphabet = set(['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', '-', ' ']) 
russian_alphabet_vowel = set(['а', 'е', 'ё', 'и', 'о', 'у', 'э', 'ю', 'я', 'А', 'Е', 'Ё', 'И', 'О', 'У', 'Э', 'Ю', 'Я'])

# Переводит с английского транслита на русский язык
def translite_row(row):
    try:
        name = row['name']
        list_of_words = name.split(" ")
        translated_list = []
        for word in list_of_words:
            if word[-1] == "y":
                if word[-2] == "ц":
                    word = word[:-1] + "и"
                elif word[-2] in list_of_consonant_eng:
                    word = word[:-1] + "ы"
                else:
                    word = word[:-1] + "й"
            if word[0] == "I" or word[0] == "i":
                word = "И" + word[1:]
            for key in slovar_for_composites_more_2:
                word = word.replace(key, slovar_for_composites_more_2[key])
            for key in slovar_for_composites:
                word = word.replace(key, slovar_for_composites[key])
            for key in slovar:
                word = word.replace(key, slovar[key])
            if "ы" in list(word):
                list_with_y = list(word)
                y_index = list_with_y.index("ы")
                if list_with_y[y_index-1] in russian_alphabet_vowel:
                    list_with_y[y_index] = "й"
                    word = "".join(list_with_y)
            if word[-1] == "ы":
                word = word[:-1] + "й"
            translated_list.append(word)
        return " ".join(translated_list)
    except:
        pass


# Достает значение (если оно есть) на русском языке из столбца "alternatenames" и присваивает его russian_name
def check_for_russian(row):
    if row['alternatenames'] != "нет данных":
        maybe_russian_word = row['alternatenames'].split(",")[-1]
        russian_letters = set(maybe_russian_word)
        if russian_letters.issubset(russian_alphabet):
            return maybe_russian_word
    return row['russian_name']


def tz_diff(date, tz1, tz2):
    '''
    Возвращает разницу во времени между timezone1 and timezone2
    для данной даты
    пример:
    date = '2020-09-18'
    '''
    date = pd.to_datetime(date)
    return (tz1.localize(date) - tz2.localize(date).astimezone(tz1)).seconds/3600

# Загрузим данные
df = pd.read_csv('RU.txt', delimiter= '\t', low_memory=False, header=None)
df.insert(4, "russian_name", value="Город")

# Дадим названия нашим столбцам
columns = ['geonameid', 'name', 'asciiname', 'alternatenames','russian_name', 'latitude', 'longitude', 
           'feature_class', 'feature_code', 'country_code', 'cc2', 'admin1_code', 'admin2_code',
           'admin3_code', 'admin4_code', 'population', 'elevation', 'dem', 'timezone', 'modification_date']
df.columns = columns
df.fillna('нет данных', inplace=True) # заполним пропущенные значения на "нет данных"
# Теперь данные имеют вид таблицы

# Примением написанные функции для получения столбца с русскими названиями
df['russian_name'] = df.apply(translite_row, axis=1)
df['russian_name'] = df.apply(check_for_russian, axis=1)

# Лист с уникальными названиями на русском
unique_russian_names = df.russian_name.unique().tolist()


def main():
    PORT = 8000
    server = HTTPServer(('',PORT),helloHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()
