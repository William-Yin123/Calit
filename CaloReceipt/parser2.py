import sqlite3
import difflib

in_stream = open("keywords.csv")
key_words = in_stream.read()
in_stream.close()
key_words = key_words.split('\n')

for i in range(len(key_words)):
    key_words[i] = key_words[i].split(',')

def abbrev_to_word(word):
    word = word.lower()
    for x in key_words:
        if x[0] == "":
            break
        if x[0][0] == word[0]:
            for y in key_words[key_words.index(x)]:
                if y == word:
                    return x[0]
    return word

def parser(file):
    f = open(file, "r")
    f1 = f.readlines()
    item_list = {}
    for line in f1:
        quantity = 0
        line_array = line.split()
        try:
            tmp = int(line_array[0])
            quantity = tmp
        except:
            pass
        if quantity:
            words = line_array[1:len(line_array) if line_array[len(line_array)-1].isalpha() else len(line_array)-1]
            conv_words = []
            for x in words:
                conv_words.append(abbrev_to_word(x))
            item_list[" ".join(conv_words)] = quantity
    f.close()

    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()
    query = cursor.execute("select item, calories from McDonalds")
    results = query.fetchall()
    dict = {}
    possibilities = []
    for name, calorie in results:
        dict[name] = calorie
        possibilities.append(name)

    total_cals = 0
    data = {}
    for item in item_list:
        menu_item = difflib.get_close_matches(item, possibilities, 1, 0)
        data[menu_item[0]] = dict[menu_item[0]]
        total_cals += dict[menu_item[0]]
    data["total_cals"] = total_cals
    return data

