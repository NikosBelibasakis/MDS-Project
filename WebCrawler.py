#version4s
import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
# import requests  not needed now , because we have aiohttp and asyncio


# Function which returns last word
def lastWord(string):
    # split by space and converting
    # string to list and
    lis = list(string.split(" "))

    # length of list
    length = len(lis)

    # returning last element in list
    return lis[length - 1]

#function for extracting surname of a scientist
def extract_surname(soup):
    
    temp_html = soup.find('div', class_='mw-content-ltr mw-parser-output') #get each scientist's name
    name = temp_html.find('p', class_='').b

    z = 1

    if name is None:
        while name is None:
            name = temp_html.find_all('p', class_='')
            name = name[z].b
            z = z + 1

    name = name.text
    name = lastWord(name)
    return name

#extract what education every scientist has had from their wikipedia page
def extract_education(soup):
    education = ""
    education_found = False
    headlines = soup.find_all('h2', class_='')  # Get all the headlines of the page
    for headline in headlines:
        span_tag = headline.find('span', class_='mw-headline')
        if span_tag and "education" in span_tag.get_text().lower():
            # If "education" is found in the headline
            next_tag = headline.find_next('h2')  # Find the next h2 tag after the headline
            if next_tag:
                # Collect text from <p> and <ul> elements until the next <h2> tag
                elements = headline.find_next_siblings(['p', 'ul'])
                for element in elements:
                    # Concatenate the text of <p> and <ul> elements until the next <h2> tag
                    if element.name == 'p':
                        education += element.get_text() + "\n"
                    elif element.name == 'ul':
                        education += element.get_text(separator='\n') + "\n"
                    if element.find_next('h2') == next_tag:
                        break  # Exit loop when the next h2 tag is encountered
                break  # Exit the loop after processing the education section
            
    if not education_found:
        # If "Education" section doesn't exist, try to get education from the "Biography" section
        biography_headline = soup.find('span', {'id': 'Biography'})
        if biography_headline:
            # Find the <h2> tag with "Biography" section and get the first <p> tag as education
            biography_next_tag = biography_headline.parent.find_next('h2')
            if biography_next_tag:
                education_paragraph = biography_headline.parent.find_next('p')
                if education_paragraph:
                    education += education_paragraph.get_text() + "\n"

    return education

       
#asynchronous function for fetching information about scientists
async def fetch_info(session, link):
    async with session.get(link) as response:
        if response.status == 200:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'lxml')
            
            awards = ''  # Extract awards from the page
            dblp_record = ''  # Extract DBLP record
            
            # Return a dictionary with extracted information
            return {
                'surname': extract_surname(soup),
                'awards': awards,
                'education': extract_education(soup),
                'dblp_record': dblp_record
            }
        else:
            return None

async def main():
    href_obj = []  #a list where the hrefs will be stored
    scientist_info_list = []  #a list where the surnames of the computer scientists' pages will be stored
    links = []  #a list where the links of the computer scientists' pages will be stored

    async with aiohttp.ClientSession() as session:
        html_text = await session.get('https://en.wikipedia.org/wiki/List_of_computer_scientists')
        soup = BeautifulSoup(await html_text.text(), 'lxml')
        list_items = soup.find_all('li', class_='') #get the <li>s that have no class

        for l in list_items:        #for each <li> tag
            a_tag = l.find('a')     #find the first <a> tag
            if a_tag is not None:           #if <a> tag exists
                a_tag_href = a_tag['href']  #get the href (link) of the <a> tag
                href_obj.append(a_tag_href) #add the href in the list
            else:
                a_tag_text = None

        del href_obj[685:]   #delete the hrefs that don't refer to computer scientists

        #we store the links of the computer scientists' pages in the "links" list
        links = ["https://en.wikipedia.org" + str(h) for h in href_obj]

        tasks = []
        for link in links:      #visiting each scientist's page
            tasks.append(fetch_info(session, link))

        scientist_info_list = await asyncio.gather(*tasks)

        #Changing some elements in the surname list, because some surnames have peculiarities
        scientist_info_list[24]['surname'] = 'Bachman'
        scientist_info_list[26]['surname'] = 'Backus'
        scientist_info_list[33]['surname'] = 'Bauer'
        scientist_info_list[43]['surname'] = 'Blaauw'
        scientist_info_list[61]['surname'] = 'Bourne'
        scientist_info_list[62]['surname'] = 'Bouwman'
        scientist_info_list[70]['surname'] = 'Brinch Hansen'
        scientist_info_list[72]['surname'] = 'Brooks'
        scientist_info_list[76]['surname'] = 'Caballero Gil'
        scientist_info_list[83]['surname'] = 'Carmack'
        scientist_info_list[95]['surname'] = 'Clarke'
        scientist_info_list[97]['surname'] = 'Codd'
        scientist_info_list[109]['surname'] = 'Corbató'
        scientist_info_list[141]['surname'] = 'Dix'
        scientist_info_list[145]['surname'] = 'Draper'
        scientist_info_list[153]['surname'] = 'Eckert'
        scientist_info_list[157]['surname'] = 'Emerson'
        scientist_info_list[180]['surname'] = 'Ford' #Ford Jr. 
        scientist_info_list[179]['surname'] = 'Forbus'
        scientist_info_list[200]['surname'] = 'Gates'
        scientist_info_list[203]['surname'] = 'Geschke'
        scientist_info_list[256]['surname'] = 'Hehner'
        scientist_info_list[287]['surname'] = 'Ingalls'
        scientist_info_list[334]['surname'] = 'Kruskal'
        scientist_info_list[403]['surname'] = 'Moore'
        scientist_info_list[473]['surname'] = 'Pieraccini'
        scientist_info_list[509]['surname'] = 'Royce'
        scientist_info_list[566]['surname'] = 'Steele'

        # Saving scientist info to JSON file
        with open("scientist_info.json", "w") as outfile:
            json.dump(scientist_info_list, outfile, indent=4,ensure_ascii=False)
            #with ensure_ascii=False, non-ASCII characters are represented directly in the JSON file without escaping them as Unicode escape sequences.
        

        i = 0

        for scientist_info in scientist_info_list:
            surname = scientist_info.get('surname')
            ed = scientist_info.get('education')
            if surname:
                if ed=='' :
                    print(f'Scientist: {surname}, and index number: {i} with no education')
                i = i + 1


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
