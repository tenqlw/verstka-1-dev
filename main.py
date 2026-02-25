import datetime
import pandas as pd

from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)             

df = pd.read_excel('wine3.xlsx', na_values='', keep_default_na=False)

categories = defaultdict(list)

for _, row in df.iterrows():
    category = row['Категория']
    wine = {
        'Категория': category,
        'Название': row['Название'],
        'Сорт': row['Сорт'] if pd.notna(row['Сорт']) else '',
        'Цена': row['Цена'],
        'Картинка': row['Картинка'],
        'Акция': row['Акция']
    }
    categories[category].append(wine)

pprint(dict(categories)) 

def get_year_form(year: int) -> str:
    if 11 <= year % 100 <= 14:
        return "лет"
    last_digit = year % 10
    if last_digit == 1:
        return "год"
    if last_digit in (2, 3, 4):
        return "года"
    return "лет"

template = env.get_template('template.html')

now = datetime.datetime.now()
age=now.year - 1920
year_form=get_year_form(age)

context = {
    'categories': dict(categories),
    'year': age,
    'name_years': year_form
}

rendered = template.render(context)
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()