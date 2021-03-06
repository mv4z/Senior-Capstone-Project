import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen

#Currently NOT supporting multiple pages or creating master dictionary

def getTitles():
    pnames = []
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')

    for pos in soup.find_all('div', class_='title'):
        name = pos.a.get('title')
        #print (name)
        pnames.append(name)
    return (pnames)


def getCompanies():
    companies = []
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')
    
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        company = div.find_all(name='span', attrs={'class':'company'})
        if len(company) > 0:
          for b in company:
            companies.append(b.text.strip())
        else:
          sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
          for span in sec_try:
              companies.append(span.text.strip())
    return(companies)


def getLocations():
    locations = []
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')
    spans = soup.findAll('span', attrs={'class': 'location'})
    for span in spans:
        locations.append(span.text)

    return(locations)

def getDates():
    dates=[]
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')
    spans = soup.findAll('span', attrs={'class': 'date'})
    for span in spans:
        dates.append(span.text)
    return (dates)




def getPay():
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')  
    sal = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        try:
            sal.append(div.find(name='span', attrs={'class':'salaryText'}).text.replace('\n', ''))
        except:
            try:
                sal.append(div.find(name='span', attrs={'class':'sjcl'}).text.replace('\n', ''))
            except:
                continue
                
    return(sal)



#the short description provided
def getShortDesc():
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml') 
    summaries = []
    spans = soup.find_all('div', class_='summary')
    for span in spans:
        summaries.append(span.text.strip())
    return(summaries)


def getLinks():
    links = []
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')

    for pos in soup.find_all('div', class_='title'):
        link = pos.a.get('href')
        links.append("https://www.indeed.com" + link)
    return (links)




def getFullDesc(link):
    #descs = []
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    desc = soup.find('div', class_='jobsearch-jobDescriptionText')
    desc = desc.text
    return  (desc)


def getSkills(link):
    skillset = []
    skills = ['python', 'java', 'c++', 'sql', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end', 'html', 'css','json', 'xml','api', 'linux', 'nodejs', 'c#', 'spark', 'sas', 'matlab', 'excel', 'spark', 'hadoop', 'azure', 'spss', 'git']
    desc = getFullDesc(link).lower().split()
    for i in desc:
        if i in skills and i not in skillset:
            skillset.append(i)

    return (skillset)


#can change to return as a list
def getCategory(link):
    aiKeys = ['ai', 'a.i.', 'artificial intelligence', 'artificial']
    dlKeys= ['deep learning', 'neural networks', 'big data', 'deep', 'statistics']
    mlKeys = ['data mining', 'machine learning', 'cnn', 'rbm', 'machine', 'natural language', 'regression', 'fault diagnosis', 'intrusion detection']
    seKeys = ['software engineer', 'software development','code']

    sumList = getFullDesc(link).lower().split()

    for i in sumList:
        if i in aiKeys:
            return ('Artificial Intelligence')
    for i in sumList:
        if i in dlKeys:
            return ('Deep Learning')
    for i in sumList:
        if i in mlKeys:
            return ('Machine Learning')
    for i in sumList:
        if i in seKeys:
            return ('Software Engineer')

    return ('Other')




def getSome(job,city,genLinks,cnt):#creates links to job listings in indeed
    'if no location is given then make it into empty list plus this only covers cities only. There needs to be a job as a string to make this work'
    baseLink="https://www.indeed.com/"
    job=job.replace(" ","+")
    position=baseLink+"jobs?q="+job
    if city==[]:
        position=position+"&start=00"
        if genLinks==[]:
            genLinks.append(position)
        if cnt<10:
            cnt+=1
            link=position.replace(position[-2],str(cnt))
            link=link[:-1]+"0"                          #this only works if it is under 10 pages
            genLinks.append(link)
            cnt+=1
            getSome(job,city,genLinks,cnt)
    else:
        position=position+"&l="+str(city)+"&start=00"
        if genLinks==[]:
            genLinks.append(position)
        if cnt<10:
            cnt+=1
            link=position.replace(position[-2],str(cnt))
            link=link[:-1]+"0"                          #same for this one
            genLinks.append(link)
            cnt+=1
            getSome(job,city,genLinks,cnt)
    return genLinks

    




