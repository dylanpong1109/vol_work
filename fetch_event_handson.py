import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

url = "https://volunteer.handsonhongkong.org/search/getOpportunitiesCalendar"

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "__stripe_mid=e6390de8-a5a4-4ac4-a32b-9ebfb0ad9ea7765712; __stripe_sid=2b8fa0bc-8d26-459a-be84-35d3ee3f5b2ae31dbf; ASP.NET_SessionId=zlhkydvjfbasb0af0xv4rhd3; current-data-selected=eyJpc0dsb2JhbCI6IjAiLCJpc0NNU0FkbWluIjoiMCIsImlzTG9nZ2VkIjoiMCJ9; Languages=W3siSUQiOjYsIk5hbWUiOiJDaGluZXNlIiwiVXJsIjoiemgiLCJpc0RlZmF1bHQiOmZhbHNlLCJJc28iOiJ6aC1DSFQiLCJTaXRlSWQiOjIyNSwiQ3JlYXRlZERhdGUiOiJcL0RhdGUoMTcyNzk0Njg0NjI5MilcLyJ9LHsiSUQiOjksIk5hbWUiOiJFbmdsaXNoIiwiVXJsIjoiZW4iLCJpc0RlZmF1bHQiOnRydWUsIklzbyI6ImVuLVpXIiwiU2l0ZUlkIjoyMjUsIkNyZWF0ZWREYXRlIjoiXC9EYXRlKDE3Mjc5NDY4NDYyOTIpXC8ifV0=; CurrentLanguage=W3siSUQiOjksIk5hbWUiOiJFbmdsaXNoIiwiVXJsIjoiZW4iLCJpc0RlZmF1bHQiOnRydWUsIklzbyI6ImVuLVpXIiwiU2l0ZUlkIjoyMjUsIkNyZWF0ZWREYXRlIjoiXC9EYXRlKDE3Mjc5NDY4NDYyOTIpXC8ifV0=; __RequestVerificationToken=VPc2hUx8Qpp8dFkpGIZasjeL4BTimK-VZId7ZUTsHAQnFrrhR_NYx9gB1BCuKEKAAM3KxlNCnb91VE2MWc6kRstqrGU1; _gid=GA1.2.1910109432.1727946850; _ga_TZHF49THX7=GS1.1.1727946828.1.1.1727946850.0.0.0; fpestid=5dpUKNDdlEl6BlgWqPCblddTzmfs9zDRNWtK0wFT71zWq3egPklctyCu9EtNe84wI6uEeA; _cc_id=c8dd87c68bc267355625d82c95cdf9e9; panoramaId_expiry=1728033250834; _gcl_au=1.1.361868553.1727946851; ARRAffinity=6ff1e39c46353b36490f8387ecbcaf4cbeab85bbaaf088ab79879167c08c408d; ARRAffinitySameSite=6ff1e39c46353b36490f8387ecbcaf4cbeab85bbaaf088ab79879167c08c408d; _gat_gtag_UA_3334112_3=1; _gat_gtag_UA_23258225_5=1; _gat_gtag_UA_37930115_1=1; _ga_EV2FPCRP1Y=GS1.1.1727946849.1.1.1727947014.0.0.0; _ga=GA1.1.75766060.1727946828; _ga_YY6X29P83E=GS1.1.1727946849.1.1.1727947014.60.0.0",
    "Origin": "https://volunteer.handsonhongkong.org",
    "Referer": "https://volunteer.handsonhongkong.org/calendar?",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

start_date = datetime.strftime(datetime.today(), '%Y-%m-%d')
end_date = datetime.strftime(datetime.today() + relativedelta(months=1), '%Y-%m-%d')
print('start_date', start_date, 'end_date', end_date)
data = {
    "searchResultBlockId": "483",
    "isRecreateAction": "false",
    "IsFromShareUrl": "false",
    "searchvo_location_type": "",
    "searchvo_zip": "",
    "searchvo_issue_area": "",
    "searchvo_keyword": "",
    "searchvo_distance": "",
    "searchvo_age_volunteer": "",
    "searchvo_age_volunteer_specific_values": "",
    "searchvo_serve_this_organization": "",
    "searchvo_managed_by": "",
    "searchvo_population_served": "",
    "searchvo_duration": "",
    "searchvo_appropiate_groups_yes": "",
    "searchvo_appropiate_seniors_yes": "",
    "searchvo_appropiate_court_ordered_yes": "",
    "searchvo_opportunity_type": "",
    "searchvo_invitation_code": "",
    "searchvo_startfrom": start_date, #"2024-09-28",
    "searchvo_endfrom": end_date, #"2024-11-09",
    "searchvo_location_names": "",
    "searchvo_causes": "",
    "searchvo_availability": "",
    "searchvo_skills": "",
    "searchvo_activity_type": "",
    "searchvo_events": "",
    "searchvo_age_group": "",
    "searchvo_gender": "",
    "searchvo_view_by": "",
    "searchvo_searchresultblockid": ""
}

response = requests.post(url, headers=headers, data=data, verify='Zscalar.cer')
# print(response.text)

# Parse the JSON string
events = response.json()

all_data = []

for date_event in events['items']:
    for occurrence in date_event['occurrences']:
        # Extract the required fields
        event_url = occurrence.get('opportunityLink')
        event_title = occurrence.get('opportunityName')
        event_description = occurrence.get('description')
        start_date = occurrence.get('startDateTimeISO').split('T')[0]
        end_date = occurrence.get('endDateTimeISO').split('T')[0]
        start_time = occurrence.get('startTime')
        end_time = occurrence.get('endTime')
        all_data.append(occurrence)

        # print("Event URL:", event_url)
        # print("Event Title:", event_title)
        # print("Event Description:", event_description)
        # print("Start Date:", start_date)
        # print("End Date:", end_date)
        # print("Start Time:", start_time)
        # print("End Time:", end_time)

# Save the response as JSON
if response.status_code == 200:
    save_json = all_data
    
    with open("response_handson.json", "w", encoding="utf-8") as f:
        json.dump(save_json, f, ensure_ascii=False, indent=4)
    print("Response saved as response_handson.json")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(f"Response: {response.text}")