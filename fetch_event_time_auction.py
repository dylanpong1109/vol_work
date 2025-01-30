import requests
import time
import json
from bs4 import BeautifulSoup

def fetch_time_auction():
    # URL of the page to scrape
    page = 1
    projects = []
    while True:
        print(f'current page: {page}')
        url = f"https://timeauction.org/en/projects?page={page}"

        # Perform an HTTP GET request to fetch the page content
        response = requests.get(url)
        html_content = response.content

        # Parse the fetched HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract project details
        project_cards = soup.select("div.projects-catalog_filter-projects-grid a")

        last_item_no = soup.select("#showing-number")[0].get_text(strip=True)
        if int(last_item_no) == 0:
            break

        for card in project_cards:
            
            title = card.select_one(".project-card_help-us-title").get_text(strip=True)
            organization = card.select_one(".project-card_content-org-name").get_text(strip=True)
            time_details = card.select_one(".project-card_content-time-count").get_text(strip=True)
            image_url = card.select_one(".project-card_banner")["src"]

            link = card.get('href')
        
            # Since the extracted link is a relative URL, we need to make it absolute
            absolute_link = f"https://timeauction.org{link}"

            project_detail = None
            start_date = None
            end_date = None

            if absolute_link:
                response = requests.get(absolute_link)
                html_content = response.content
                soup = BeautifulSoup(html_content, "html.parser")

                project_period = soup.select_one('#projectPeriod').get_text(strip=True)
                start_end = project_period.split('-')
                if len(start_end) == 2:
                    start_date = project_period.split('-')[0]
                    end_date = project_period.split('-')[1]
                else:
                    start_date = project_period.split('-')[0]
                    end_date = project_period.split('-')[0]

                project_details = soup.select('#projectDetailsList li')
                detail_list = []
                for detail in project_details:
                    detail_list.append(detail.get_text(strip=True))
                project_detail = '\n'.join(detail_list)

            projects.append({
                "title": title,
                "organization": organization,
                "start_date": start_date,
                "end_date": end_date,
                "time_details": time_details,
                "project_details": project_detail,
                "image_url": image_url,
                "link": absolute_link
            })

        page += 1
        time.sleep(0.5)

    ## Print out the extracted details
    # for project in projects:
    #     print(f"Title: {project['title']}")
    #     print(f"Organization: {project['organization']}")
    #     print(f"Start date: {project['start_date']}")
    #     print(f"End date: {project['end_date']}")
    #     print(f"Time Details: {project['time_details']}")
    #     print(f"Project Details: {project['project_details']}")
    #     print(f"Image URL: {project['image_url']}")
    #     print(f"Event Link: {project['link']}")
    #     print("-" * 50)

    with open("response_time_auction.json", "w", encoding="utf-8") as f:
        json.dump(projects, f, ensure_ascii=False, indent=4)
    print("Response saved as response_time_auction.json")

if __name__=="__main__":
    fetch_time_auction()