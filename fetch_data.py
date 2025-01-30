from fetch_event_avs import fetch_avs
from fetch_event_handson import fetch_handson
from fetch_event_socialcareer import fetch_social_career
from fetch_event_time_auction import fetch_time_auction

def main():
    fetch_avs()
    fetch_handson()
    fetch_social_career()
    fetch_time_auction()

if __name__=="__main__":
    main()
