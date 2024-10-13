from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

def load_events_data():
    # Load events data from JSON file
    with open("response.json", 'r', encoding='utf-8') as f:
        events_data = json.load(f)

    with open("response_avs.json", 'r', encoding='utf-8') as f:
        events_data_avs = json.load(f)

    with open("response_handson.json", 'r', encoding='utf-8') as f:
        events_data_handson = json.load(f)
    
    return events_data, events_data_avs, events_data_handson

@app.route("/")
def index():
    events_data, events_data_avs, events_data_handson = load_events_data()
    return render_template("index.html", events_data=events_data, 
                           events_data_avs=events_data_avs, 
                           events_data_handson=events_data_handson)


@app.route("/search", methods=["GET"])
def search():
    events_data, events_data_avs, events_data_handson = load_events_data()
    def standardize_time(timestamp):
        if timestamp:
            ## Use try-except to parse timstamp, avoid complicated regex expression
            try:
                time_obj = datetime.strptime(timestamp, "%H:%M")
                return time_obj.strftime('%H:%M:%S')
            except ValueError:
                pass

            try:
                time_obj = datetime.strptime(timestamp, "%H:%M:%S")
                return timestamp
            except ValueError:
                raise f"Invalid format: {timestamp}"
        else:
            return None
        
    start_date_str = request.args.get("startDate")
    
    if not start_date_str:
        return jsonify([])

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    results = []

    for job in events_data["data"]["jobs"]["data"]:
        for session in job["sessions"]:
            for timeslot in session["timeslots"]:
                if timeslot["startDate"]:
                    timeslot_start_date = datetime.strptime(timeslot["startDate"], "%Y-%m-%d")
                    if timeslot_start_date == start_date:
                        results.append({
                            "url": "https://app.socialcareer.org/volunteers/" + job["id"],
                            "web_host": "社職",
                            "job_title": job["title"],
                            "job_description": job["description"],
                            "session_title": session["title"],
                            "startDate": timeslot["startDate"],
                            "endDate": timeslot.get("endDate"),
                            "startTime": standardize_time(timeslot.get("startTime")),
                            "endTime": standardize_time(timeslot.get("endTime"))
                        })
    
    for event in events_data_avs:
        if event['Start Date']:
            timeslot_start_date = datetime.strptime(event['Start Date'], "%Y-%m-%d")
            if timeslot_start_date == start_date:
                results.append({
                    "url": event["URL"],
                    "web_host": "AVS",
                    "job_title": event["Title"],
                    "job_description": event["Description"],
                    "session_title": 'N/A',
                    "startDate": event["Start Date"],
                    "endDate": event.get("End Date"),
                    "startTime": standardize_time(event.get("Start Time")),
                    "endTime": standardize_time(event.get("End Time"))
                })

    for event in events_data_handson:
        if event['startDateTimeISO']:
            timeslot_start_date = datetime.strptime(event['startDateTimeISO'], "%Y-%m-%dT%H:%M")
            if timeslot_start_date.date() == start_date.date():
                results.append({
                    "url": event["opportunityLink"],
                    "web_host": "Hands-on",
                    "job_title": event["opportunityName"],
                    "job_description": event["description"],
                    "session_title": 'N/A',
                    "startDate": event["startDateTimeISO"].split('T')[0],
                    "endDate": event.get("endDateTimeISO").split('T')[0],
                    "startTime": standardize_time(event.get("startTime")),
                    "endTime": standardize_time(event.get("endTime"))
                })
    
    results = sorted(results, key=lambda event: event['startTime'])

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)