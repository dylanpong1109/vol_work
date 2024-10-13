import json


# Parse the JSON data
with open('./response.json', 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)


# Access specific fields
jobs_data = parsed_data["data"]["jobs"]["data"]
for job in jobs_data:
    job_title = job.get("title", "N/A")
    job_description = job.get("description", "N/A")
    sessions = job["sessions"]
    
    for session in sessions:
        session_title = session.get("title", "N/A")
        for timeslot in session["timeslots"]:
            start_date = timeslot.get("startDate", "N/A")
            end_date = timeslot.get("endDate", "N/A")
            start_time = timeslot.get("startTime", "N/A")
            end_time = timeslot.get("endTime", "N/A")
            
            # Print the results
            print(f"Job Title: {job_title}")
            print(f"Job Description: {job_description}")
            print(f"Session Title: {session_title}")
            print(f"Start Date: {start_date}")
            print(f"End Date: {end_date}")
            print(f"Start Time: {start_time}")
            print(f"End Time: {end_time}")
            print()  # Newline for better readability