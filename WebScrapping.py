import requests
from bs4 import BeautifulSoup
import pandas as pd
'''
returns date committed and message
'''
def commit_info(url ,name):
    print(url,'---->',name)
    commit = BeautifulSoup(requests.get(url).content,'html.parser')
    links = commit.find_all('pre') # will return commit message
    commit_date = commit.find_all('div',class_="u-monospace Metadata")[0].find_all('td')
    #check the page format and modify as per need.
    submit_date_idx = -3
    if len(commit_date) == 9:
        submit_date_idx = -4
    commit_date = commit_date[submit_date_idx].getText()
    #print('len of commit',len(commit_date),'len of links', len(links))
    return commit_date ,links[0].getText()

home = "https://android.googlesource.com"
start = "/platform/frameworks/av/+log/pie-dev/services/audiopolicy"
head = home+start
page = requests.get(head)

#make a Beautiful Soup
soup = BeautifulSoup(page.content,'html.parser')
links = soup.find_all(class_="CommitLog-item CommitLog-item--default") #check in your case ?
final_list = []
for link in links :
    tmp_link = link.find_all('a')[-1]
    #get the link and name
    name = tmp_link.getText()
    route_link = tmp_link.get('href')
    info = commit_info(home+route_link ,name)
    #make list as data, title, message, link
    lst =[]
    lst.append(info[0])
    lst.append(name)
    lst.append(info[1])
    lst.append(home+route_link)
    final_list.append(lst)

#print(final_list)
df = pd.DataFrame(final_list,columns=['Date Submitted','title','message','link'])
df.to_csv('test.csv')
