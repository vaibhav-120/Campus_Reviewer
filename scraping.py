import requests
from bs4 import BeautifulSoup

def Scraping(id,page):
    url = f"https://www.careers360.com/colleges/reviews?page={page}&college_id={id}"
    proxy={
            "http": "http://pehgjxwr:j7u0qyb1xux8@198.23.239.134:6540",
            "https": "http://pehgjxwr:j7u0qyb1xux8@198.23.239.134:6540",
            "http": "http://pehgjxwr:j7u0qyb1xux8@207.244.217.165:6712",
            "https": "http://pehgjxwr:j7u0qyb1xux8@207.244.217.165:6712"
        }

    response = requests.get(url,proxies=proxy)    
    College_Infrastructure = []
    Academics = []
    Placements = []
    Campus_Life = []
    Anything_Else = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        divs = soup.find_all('div', class_='detail_content_review')
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    for div in divs:
        # Access <h> tags (assuming it could be any heading tag like <h1>, <h2>, etc.)
        heading = div.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        paragraph = div.find('p')
        if heading and paragraph:
            if heading.get_text() == "College Infrastructure":
                College_Infrastructure.append(paragraph.get_text())
            elif heading.get_text() == "Academics":
                Academics.append(paragraph.get_text())
            elif heading.get_text() == "Placements":
                Placements.append(paragraph.get_text())
            elif heading.get_text() == "Campus Life":
                Campus_Life.append(paragraph.get_text())
            elif  heading.get_text() == "Anything Else":
                Anything_Else.append(paragraph.get_text())

    return College_Infrastructure,Academics,Placements,Campus_Life,Anything_Else


def scrap(id):
    try:
        College_Infrastructure = []
        Academics = []
        Placements = []
        Campus_Life = []
        Anything_Else = []
        for i in range(1,10):
            College_infra,Academic, Placement,Campus_Lyf,Any_Else = Scraping(id,i)
            College_Infrastructure += College_infra
            Academics += Academic
            Placements += Placement
            Campus_Life += Campus_Lyf
            Anything_Else += Any_Else
    except:
        pass
    data = {}
    data["College_Infrastructure"] = College_Infrastructure
    data["Academics"] = Academics
    data["Placements"] = Placements
    data["Campus_Life"] = Campus_Life
    data["Anything_Else"] = Anything_Else
    return data