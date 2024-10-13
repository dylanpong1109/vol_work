from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
from time import sleep

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "avs_vhk_frontend=j0vkva7eh76lj2n1u9efof6vrt; _ga=GA1.1.1251223097.1727923325; avs_cookie_accept=Clicked; _ga_HW71D943EC=GS1.1.1727923325.1.1.1727923524.0.0.0",
    "Referer": "https://www.volunteering.org.hk/campaign_search?campaign-type=&TypeOfVolunteerWorkOthers=&District%5B%5D=958160000&start=&end=",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

def fetch_avs():
    print('Start fetching avs data')
    response = requests.get('https://www.volunteering.org.hk/campaign_search', headers=headers)

    print(response.status_code)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    activity_div = soup.find('div', id='activityitems')
    events = activity_div.find_all('div', class_='voluntary-item')
    all_data = []

    base_url = "https://www.volunteering.org.hk/"

    for event in events:
        title = event.find('div', class_='title').text.strip()
        start_date = event.find_all('span', class_='date')[0].text.strip()
        end_date = event.find_all('span', class_='date')[1].text.strip()
        
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        # Calculate duration
        if '服務時數' in event.text:
            duration = event.find('div', class_='service-time').text.strip().replace('\t', '')
        # elif '培訓時間' in event.text:
        #     duration = event.find('div', class_='service-time').text.strip()
        else:
            # Calculate duration if not directly provided
            duration = end_datetime - start_datetime

        a_tag = event.find('a', href=True)
        if a_tag:
            href = a_tag['href']
            full_url = base_url + href
        #     response = requests.get(full_url, headers=headers, verify='Go Daddy Root Certificate Authority - G2.crt')
        #     # Parse the HTML content using BeautifulSoup
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     # Extract the "職責" content
        #     description_tag = soup.find('td', string='職責')
        #     if description_tag:
        #         description = description_tag.find_next_sibling('td').get_text(strip=True)
        #     else:
        #         description = None

        #     # # Extract the "集合地點" content
        #     # meeting_location = soup.find('td', text='集合地點').find_next_sibling('td').get_text(strip=True)
        description = None

        event_dict = {"Title": title,
                    "Start Date": str(start_datetime.date()),
                    "End Date": str(end_datetime.date()),
                    "Start Time": str(start_datetime.time()),
                    "End Time": str(end_datetime.time()),
                    "Duration": str(duration), 
                    "Description": description,
                    "URL": full_url}

        all_data.append(event_dict)
        sleep(0.5)

    with open("response_avs.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    print("Response saved as response.json")

if __name__=='__main__':
    fetch_avs()