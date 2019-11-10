from selenium import webdriver
import sqlite3

url = "https://fastfoodnutrition.org/"
conn = sqlite3.connect("menu.db")
cursor = conn.cursor()
driver = webdriver.Chrome()
driver.implicitly_wait(2)

driver.get(url)

els = driver.find_elements_by_css_selector("ul.restaurant_list > li > a.c_t")
links = []
items = {}
for el in els:
    links.append(el.get_attribute("href"))
    s = el.text
    for old, new in [("-", ""), (" ", ""), ("_", ""), ("?", ""), ("%", ""), ("#", ""), ("/", ""), ("\"", ""), ("'", "")]:
        s = s.replace(old, new)
    items[s] = []

for link, item in zip(links, items):
    driver.get(link)
    data = driver.find_elements_by_class_name("item_link")
    for datum in data:
        try:
            datum_array = datum.text.split("\n")
            tmp = []
            tmp.append(datum_array[0])
            datum_array[2] = datum_array[2].split(" ")[0]
            if "-" in datum_array[2]:
                tmp.append((float(datum_array[2].split("-")[0]) + float(datum_array[2].split("-")[1])) / 2)
            else:
                tmp.append(float(datum_array[2]))
            items[item].append(tmp)
        except:
            pass

for item in items:
    cursor.execute("create table " + item + " (id INTEGER PRIMARY KEY NOT NULL, item TEXT NOT NULL, calories NUMERIC NOT NULL)")
    for menu_item in items[item]:
        cursor.execute("insert into " + item + " (item, calories) values (:item_name, :calories)", {"item_name": menu_item[0], "calories": menu_item[1]})

conn.commit()
conn.close()
