from bs4 import BeautifulSoup
import csv
import html2text
import requests

BASE_URL = 'https://1962ordo.today/day/octave-day-nativity-lord-2-2/'
MAX_DAYS = 5

class DayContents:
    def __init__(self, html):
        text_maker = html2text.HTML2Text()
        text_maker.emphasis_mark = ''
        text_maker.strong_mark = ''

        soup = BeautifulSoup(html, 'html5lib')
        self.date = soup.select_one('.entry-content .entry-title').string
        self.title = soup.select('.entry-content')[1].find('h2').string
        description_soup = soup.select('.entry-content')[1].findAll('p')
        self.feast_class = ''
        self.color = ''
        self.description = ''
        for element in description_soup:
            element_string = str(element)
            if 'lass<br/>' in element_string:
                parts = element_string.split('<br/>')
                self.feast_class = text_maker.handle(parts[0]).strip()
                self.color = text_maker.handle(parts[1]).strip()
            else:
                self.description += text_maker.handle(element_string).strip() + '\n'
        self.description = self.description.strip()

        #self.description = html2text(''.join(map(str, soup.select('.entry-content')[1].findAll('p')))).strip()
        self.notes = text_maker.handle(''.join(map(str, soup.select('.entry-content')[2].findAll('p')))).strip()

        self.next_url = soup.select_one('footer a[rel=next]')['href']

    def __str__(self):
        attrs = vars(self)
        return '---\n' + '\n'.join('%s: %s' % item for item in attrs.items()) + '\n'

def get_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text


page_url = BASE_URL
count = 0

with open('ordo.csv', mode='w') as out_file:
    csv_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Date', 'Title', 'Class', 'Color', 'Description', 'Notes', '1962ordo.today URL'])
    while page_url and count < MAX_DAYS:
        day = DayContents(get_page(page_url))
        print(day)
        csv_writer.writerow([day.date, day.title, day.feast_class, day.color, day.description, day.notes, page_url])
        page_url = day.next_url
        count += 1
