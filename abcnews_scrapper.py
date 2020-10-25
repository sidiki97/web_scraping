import requests
from bs4 import BeautifulSoup
from queue_c import Queue, Node
import webbrowser


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


    
if __name__ == "__main__":

  explore = { 'y' : True, 'n' : False }

  start = True
    

  print()
  print("\tWelcome to abcnews Web Scrapper App!\n")


  # Initialize Queues
  story_queue = Queue()
  old_queue = Queue()
  
  # Iteration counter
  i = 0 

  while start:

    selection = input('\tPlease select a category (Type Letter): \nGeneral (G)   U.S. (U)   International (I)   Business (B)   Politics (P)\n\nCategory: ').upper()
    print()

    # Create scrapper object
    section_headlines = Abcnews_scrapper()
    
    # Update self.url based on user selection
    section_headlines.determine_search_url(selection)

    # Check status of upload
    try:
      section_headlines.check_response()
    except Exception as ex:
      print('There was a %s' % (ex))

    # Collect headlines
    section_headlines.set_top_stories(selection)
    # Display headlines
    print('\tTop Stories:\n')
    section_headlines.display_top_stories()

    """

    Queue Management

    """
    

    # Add stories to queue
    story_selections = input("Choose stories to add to queue (input numbers with spaces)? ")
    print()

    number_list = story_selections.split(' ')

    for num in number_list:
      story_info = {}
      story_info['title'] = section_headlines.get_story_title(int(num))
      story_info['link'] = section_headlines.access_headline(int(num))
      story_queue.EnQueue(story_info)

    if i > 0:
      clear = input('Clear old stories from queue (y/n)? ')
      print()
      if explore[clear]:
        old_queue.EmptyQueue()
        
    print()
    # Add contents from old_queue

    for node in range(old_queue.size):
      story_queue.EnQueue(old_queue.DeQueue())

    # Display Queue Info and Contents
    print('Size of queue: {0}'.format(story_queue.size))
    print()

    # Display contents

    exit_queue = False

    while not (story_queue.isEmpty() or exit_queue):
      
      story = story_queue.Peek()
      print(story['title'])
      print(story['link'])
      print()
      done = input('(1) Open story (o)\n(2) Done reading (y)\n(3) Skip story (s)\n\n(4) Exit queue (e)\n\nChoose letter: ')
      if done.lower() == 'o':
        webbrowser.open(story['link'])
      elif done.lower() == 'y': 
        story_queue.DeQueue()
        print()
      elif done.lower() == 's':
        skipped_story = story_queue.DeQueue()
        story_queue.EnQueue(skipped_story)
        print()
      elif done.lower() == 'e': 
        exit_queue = True

    # Add contents of story_queue to old_queue
    for node in range(story_queue.size):
      old_queue.EnQueue(story_queue.DeQueue())
    
    print()
    explore_other = input('Do you wish to explore other categories (y/n)? ').lower()
    print()

    # Stay in app(while loop)
    start = explore[explore_other]

    # Iteration of while
    i += 1


  






