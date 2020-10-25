import requests
from bs4 import BeautifulSoup


class Abcnews_scrapper:
  def __init__(self):
    self.url = 'https://abcnews.go.com/'
    self.top_stories = []
    self.query_dic = {
                      'I' : 'International',
                      'U' : 'US',
                      'P' : 'Politics',
                      'B' : 'Business'
                     }

  def determine_search_url(self, query):
    if query != 'G':
      self.url = self.url + self.query_dic[query.upper()]

  def get_response_page(self):
    return requests.get(self.url)

  def check_response(self):
    return self.get_response_page().raise_for_status()
  
  def get_soup_object(self):
    web_page_soup = BeautifulSoup(self.get_response_page().text, 'html.parser')
    return web_page_soup

  def set_top_stories(self, query):
    soup = self.get_soup_object()
    if query != 'G':
      for i in range(1,6):
        self.top_stories.append(soup.select('#fitt-analytics > div > main > div.band__lead.band > div.block__single-column.block.HeadlineStackBlock__headlines_ad > div > div:nth-child({0}) > a'.format(i))[0])
    else:
      for i in range(1,6):
        self.top_stories.append(soup.select('#trio-headline-view > ul > li:nth-child({0}) > div > h1 > a'.format(i))[0])    
          #fitt-analytics > div > main > div.band__lead.band > div.block__single-column.block.HeadlineStackBlock__headlines_ad > div > div:nth-child(1) > a

  def get_story_titles(self):
    return [titles.getText() for titles in self.top_stories]

  def get_story_title(self, num):
    headlines = self.get_story_titles()
    num -= 1
    return headlines[num]

  def display_top_stories(self):
    headlines = self.get_story_titles()
    i = 1
    for headline in headlines:
      print("(" + str(i) + ") "+ headline + "\n")
      i = i + 1

  def access_headline(self, link):
    link -= 1
    return self.top_stories[link].get('href')




  






