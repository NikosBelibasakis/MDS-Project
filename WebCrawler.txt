import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup


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
    try:  
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
    except Exception as e:
        print(f"Error extracting surname: {e}")
        return "Unknown"

#extract what education every scientist has had from their wikipedia page
def extract_education(soup):
    education = ""
    education_found = False
    headlines = soup.find_all('h2', class_='')  # Get all the headlines of the page
    for headline in headlines:
        span_tag = headline.find('span', class_='mw-headline')
        title=span_tag.get_text().lower()
        if "education" in title:
            # If "education" is found in the headline
            next_tag = headline.find_next('h2')  # Find the next h2 tag after the headline
            # Collect text from <p> and <ul> elements until the next <h2> tag
            elements = headline.find_next_siblings(['p', 'ul'])
            for element in elements:
                # Concatenate the text of <p> and <ul> elements until the next <h2> tag
                if element.name == 'p':
                    education += element.get_text() + "\n"
                elif element.name == 'ul':
                    education += element.get_text(separator='\n') + "\n"
                if element.find_next('h2') == next_tag:
                    education_found=True #we found education so we set it true!
                    break  # Exit loop when the next h2 tag is encountered
            break  # Exit the loop after processing the education section

    if not education_found:
            label_element = soup.find('th',class_='infobox-label', string=lambda text: text and "Alma" in text and "mater" in text)
            if label_element:
                # Get the corresponding <td> tag containing educational information
                data = label_element.find_next('td', class_='infobox-data')
                if data:
                    # Extract text from <a> tags inside the <td> element
                    education_list = [a.text for a in data.find_all('a')]

                    # Extract text separated by <br> tags inside the <td> element
                    br_text = data.get_text(separator='\n')
                    if br_text:
                        education_list.extend(br_text.split('\n'))

                    education = ', '.join(education_list)  # Convert list to text
                    education_found=True

    if not education_found:
        # Check "Biography", "Life", or "Career" sections
        for headline in soup.find_all('span', class_='mw-headline'):
            title = headline.get_text().lower()
            if "biography" in title or "life" in title or "career" in title:
                paragraph = headline.parent.find_next('p')
                if paragraph:
                    education += paragraph.get_text() + "\n"
                    education_found = True
                    break

    if not education_found:
        # Get the first and second <p> tags on the page
        paragraphs = soup.find_all('p')
        for p in paragraphs[:2]:
            next_tag = p.find_next('h2')
            education += p.get_text() + "\n"
            if p.find_next('h2') == next_tag:
                education_found = True
                break

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

        del href_obj[687:]   #delete the hrefs that don't refer to computer scientists

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
        scientist_info_list[44]['surname'] = 'Blaauw'
        scientist_info_list[62]['surname'] = 'Bourne'
        scientist_info_list[63]['surname'] = 'Bouwman'
        scientist_info_list[71]['surname'] = 'Brinch Hansen'
        scientist_info_list[73]['surname'] = 'Brooks'
        scientist_info_list[77]['surname'] = 'Caballero Gil'
        scientist_info_list[84]['surname'] = 'Carmack'
        scientist_info_list[96]['surname'] = 'Clarke'
        scientist_info_list[98]['surname'] = 'Codd'
        scientist_info_list[110]['surname'] = 'Corbató'
        scientist_info_list[142]['surname'] = 'Dix'
        scientist_info_list[146]['surname'] = 'Draper'
        scientist_info_list[154]['surname'] = 'Eckert'
        scientist_info_list[158]['surname'] = 'Emerson'
        scientist_info_list[181]['surname'] = 'Ford' #Ford Jr. 
        scientist_info_list[180]['surname'] = 'Forbus'
        scientist_info_list[201]['surname'] = 'Gates'
        scientist_info_list[204]['surname'] = 'Geschke'
        scientist_info_list[257]['surname'] = 'Hehner'
        scientist_info_list[288]['surname'] = 'Ingalls'
        scientist_info_list[335]['surname'] = 'Kruskal'
        scientist_info_list[404]['surname'] = 'Moore'
        scientist_info_list[474]['surname'] = 'Pieraccini'
        scientist_info_list[510]['surname'] = 'Royce'
        scientist_info_list[566]['surname'] = 'Steele'

        # Saving scientist info to JSON file
        with open("scientist_info.json", "w") as outfile:
            json.dump(scientist_info_list, outfile, indent=4,ensure_ascii=False)
            #with ensure_ascii=False, non-ASCII characters are represented directly in the JSON file without escaping them as Unicode escape sequences.
        

        i = 0

        for scientist_info in scientist_info_list:
            surname = scientist_info.get('surname')
            if scientist_info.get('education')=='':
                print(f'Scientist: {surname}, and index number: {i} \n')
                i=i+1


asyncio.run(main())
