from abcnews_scrapper import Abcnews_scrapper
import requests
from bs4 import BeautifulSoup
from queue_ll import Queue, Node
import webbrowser
  
"""
abcnews Web Scrapper App Main Program

"""

# Dict used to avoid if/else branches
explore = { 'y' : True, 'n' : False }

# Boolean to check if user wishes to continue with app
start = True
  
"""
Start of App

"""

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