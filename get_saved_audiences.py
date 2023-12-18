from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env

def get_audiences(ad_account_id):
    FacebookAdsApi.init(access_token=os.getenv('FACEBOOK_ACCESS_TOKEN'),
                        app_id=os.getenv('FACEBOOK_APP_ID'),
                        app_secret=os.getenv('FACEBOOK_APP_SECRET'))

    ad_account = AdAccount(ad_account_id)

    try:
        saved_audiences = ad_account.get_saved_audiences(fields=[
            'id',
            'name',
            'time_updated',
            # Add other fields as needed
        ])
        # Convert Cursor to list of dictionaries
        audience_list = [audience.export_all_data() for audience in saved_audiences]
        return audience_list
    except Exception as e:
        print(f'An error occurred: {e}')


# Replace 'act_453485805236160' with your actual ad account ID
audiences = get_audiences('act_453485805236160')
for audience in audiences:
    print(audience)


def find_most_recent_audience(audiences, keywords):

    # Filter audiences based on keywords
    filtered_audiences = [aud for aud in audiences if any(keyword.lower() in aud.get('name', '').lower() for keyword in keywords)]

    if not filtered_audiences:
        return None, f"No audience found containing the keywords '{keywords}'."

    # Find the most recent audience
    most_recent_audience = max(filtered_audiences, key=lambda aud: datetime.strptime(aud.get('time_updated', '1900-01-01T00:00:00+0000'), '%Y-%m-%dT%H:%M:%S%z'))

    return most_recent_audience, None



# Simplified keyword lists
broad_keywords = ['broad']
wep_keywords = ['w/e/p/e', 'wep']
reach_keywords = ['reach', 'target area']

broad_audience, broad_error = find_most_recent_audience(audiences, broad_keywords)
wep_audience, wep_error = find_most_recent_audience(audiences, wep_keywords)
reach_audience, reach_error = find_most_recent_audience(audiences, reach_keywords)

# Output results or errors
for aud, error, category in zip([broad_audience, wep_audience, reach_audience], [broad_error, wep_error, reach_error], ['Broad', 'W/E/P/E', 'Reach or Target Area']):
    if error:
        print(error)
    else:
        print(f"Most recent '{category}' audience: ID - {aud['id']}, Name - {aud['name']}")
