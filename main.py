from lxml import html

'''
import requests

headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://www.florist.ch/florist-in-der-naehe-finden/'
response = requests.get(url, headers=headers)

with open('page.html', 'w', encoding='utf-8') as file:
     file.write(response.text)
'''
page = ''
with open('page.html', 'r', encoding='utf-8') as file:
      page = file.read()

tree = html.fromstring(page)

names = tree.xpath('//*[@class="new-username"]/h2/a')
addrs = tree.xpath('//*[@class="address"]/div/a')
info = tree.xpath('//span[@class="zusatzinfo"]')

## use text_content() instead of text
pnames = []
phone = []

for elem in info:
    text = elem.text_content()
    before, sep, after = text.partition('0')
    if sep:
        name = before.strip()
        phone_number = '0' + after.strip()
        pnames.append(name)
        phone.append(phone_number)

gmap = []
for elem in addrs:
     lnk = ''
     for part in elem.xpath('./@href'):
          lnk += part
     gmap.append(lnk)

'''
for n, a, l, pn, ph in zip(names, addrs, gmap, pnames, phone):
     print("Company: ", n.text)
     print("Address: ", a.text)
     print("Google Map: ", l)
     print("Owner: ", pn)
     print("Contact no.: ", ph)
     print()
'''

Data = []
for n, a, l, pn, ph in zip(names, addrs, gmap, pnames, phone):

     d_list = []
     d_list.append(n.text)
     d_list.append(a.text)
     d_list.append(l)
     d_list.append(pn)
     d_list.append(ph)

     Data.append(d_list)


from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.title = 'Sheet1'

ws.append(['Company name', 'Address', ' Adress Link', 'Owner', 'Contact no'])

# insert_rows is used for inserting blank rows not the data !!
# use .append() to insert a list at a time

for d in Data:
     ws.append(d)

wb.save('scrap_data.xlsx')