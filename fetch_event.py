import requests
import json
from time import sleep

# Define the URL
url = "https://api.v2.socialcareer.org/graphql"

# Define the headers
headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Origin": "https://app.socialcareer.org",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "content-type": "application/json",
    "locale": "zhHant",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

    # Define the payload
payload = {
    "query": """
    query jobs($queryKey: String, $skip: Int, $pageSize: Int, $searchText: String, $filter: JobsFilter, $includePast: Boolean, $publicOnly: Boolean, $sort: String, $bookmarkSortByLast: Boolean) {
    jobs(
        params: {queryKey: $queryKey, skip: $skip, pageSize: $pageSize, searchText: $searchText, filter: $filter, includePast: $includePast, publicOnly: $publicOnly, sort: $sort, bookmarkSortByLast: $bookmarkSortByLast}
    ) {
        data {
        id
        ngoId
        ngo {
            name
            category
            logoUrl
        }
        title
        ownerCenter {
            name
        }
        sdgs
        causes
        recipients
        prerequisite {
            minAge
            maxAge
        }
        expectedCommitHours
        description
        remarks
        imageUrls
        volunteerFunctions
        skills
        languages
        languageOther
        parentalConsent
        pcAge
        quota
        remainingQuota
        acceptedQuota
        groupApply
        feeDetail
        applicationStart
        applicationEnd
        additionalQuestions {
            key
            desc
            type
            mandatory
            options {
            key
            desc
            }
        }
        contact
        contactEmail
        contactPhone
        pendingApplications
        acceptedApplications
        progress
        overallStart
        overallEnd
        sessions {
            id
            type
            title
            frequency
            position
            attendanceRule
            attendanceRuleAmount
            timeslots {
            id
            isSingleDay
            isDateTBC
            startDate
            endDate
            isAllDay
            isTimeTBC
            startTime
            endTime
            isVirtual
            address {
                en
                zhHans
                zhHant
            }
            addressLine
            mapLatLong
            recurrenceType
            recurrenceFrequency
            recurrenceWeekdays
            recurrenceMonthlyMode
            recurrenceRepeatDayOfMonth
            recurrenceRepeatWeek
            recurrenceRepeatDayOfWeek
            recurrenceExceptionDates
            regionCode
            districtCode
            subDistrictCode
            quota
            usedQuota
            pendingQuota
            remainingQuota
            }
        }
        isVirtual
        regionCode
        districtCode
        subDistrictCode
        location
        jobLink
        usedQuota
        createdAt
        updatedAt
        applicationRestrictions
        inviteMembers
        status
        }
        total
    }
    }
    """,
    "variables": {
        "filter": {
            "dayOfWeekOptions": None,
            "regionCodes": None,
            "districtCodes": None,
            "subDistrictCodes": None,
            "isVirtual": None,
            "isEditorChoice": None,
            "isNgoDetailsJobEventListFilter": None,
            "isBookmarkList": None,
            "restrictions": None,
            "causes": None,
            "recipients": None,
            "sdgoals": None,
            "volunteerFunctions": None,
            "ageOption": None,
            "ageRange": {"start": 0, "end": 100},
            "languages": None,
            "ngoId": None,
            "centerId": None,
            "expectedCommitHoursRange": {"start": 0, "end": 100}
        },
        # "skip": skip_tracker,
        "searchText": "",
        "pageSize": 12,
        "sort": "-publishDate",
        "includePast": False,
        "publicOnly": True,
        "bookmarkSortByLast": None
    },
    "operationName": "jobs"
}

skip_tracker = 0
all_data = []
while True:
    payload['variables']['skip'] = skip_tracker
    # Send the POST request
    response = requests.post(url, headers=headers, json=payload, verify='Zscalar.cer')

    event_list = response.json()['data']['jobs']['data']
    if event_list == []:
        break

    all_data += event_list
    skip_tracker += 12
    sleep(0.5)

# Save the response as JSON
if response.status_code == 200:
    save_json = {"data": {"jobs": {"data": all_data}}}
    
    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(save_json, f, ensure_ascii=False, indent=4)
    print("Response saved as response.json")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(f"Response: {response.text}")