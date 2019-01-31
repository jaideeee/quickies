import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

def model_spec(url, writer):
    print('---for the url ---',url)
    url+='/specifications'
    print('---change to the url ---', url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    specs = soup.find(class_="phone-description-section")
    details = specs.find_all(class_='phone-description-child')
    keys = []
    values = []
    for idx, section in enumerate(details):
        if idx >= 1:  # dont need starting 1 index
            keys.extend(section.find_all(class_='prop-name'))
            values.extend(section.find_all(class_='prop-value'))

    k = []
    v = []
    for k1, v1 in zip(keys, values):
        k.append(k1.get_text())
        v.append(v1.get_text())

    data = {'feature': k, 'value': v}
    df = pd.DataFrame.from_dict(data)

    sheet_name = v[1][:12]
    sheet_name.replace(r'[]:*?/\'','')
    workbook = writer.book
    df.to_excel(writer, sheet_name=sheet_name)  # sheet name is model name

    worksheet = writer.sheets[sheet_name]
    format_cells = workbook.add_format({
        'text_wrap': True,
        'valign': 'center', })
    worksheet.set_column('B:B', 20, format_cells)
    worksheet.set_column('C:C', 100, format_cells)

driver = webdriver.Chrome()
driver.get('https://themrphone.com/phone-finder')
all_links = driver.find_elements_by_class_name('result-item')
writer = pd.ExcelWriter('phones.xlsx', engine='xlsxwriter')
for link in all_links :
    phone_link = link.find_element_by_tag_name('a').get_attribute('href')
    try:
        model_spec(phone_link , writer)
    except:
        print('continue')

print('--save')
writer.save()

