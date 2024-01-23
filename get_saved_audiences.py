from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import os
from datetime import datetime
from dotenv import load_dotenv
import time
import pandas as pd
import re

load_dotenv()  # This loads the variables from .env

# Initialize the Facebook API
FacebookAdsApi.init(access_token=os.getenv('FACEBOOK_ACCESS_TOKEN'),
                    app_id=os.getenv('FACEBOOK_APP_ID'),
                    app_secret=os.getenv('FACEBOOK_APP_SECRET'))


def find_most_recent_audience(audiences, keywords):

    # Filter audiences based on keywords
    filtered_audiences = [aud for aud in audiences if any(keyword.lower() in aud.get('name', '').lower() for keyword in keywords)]

    if not filtered_audiences:
        return None, f"No audience found containing the keywords '{keywords}'."

    # Find the most recent audience
    most_recent_audience = max(filtered_audiences, key=lambda aud: datetime.strptime(aud.get('time_updated', '1900-01-01T00:00:00+0000'), '%Y-%m-%dT%H:%M:%S%z'))

    return most_recent_audience, None

def extract_version(audience_name):
    match = re.search(r'v(\d+)', audience_name)
    return int(match.group(1)) if match else None

def get_audiences(ad_account_ids, keywords_dict):
    all_audiences_filtered = {}

    for ad_account_id in ad_account_ids:
        try:
            ad_account = AdAccount(ad_account_id)
            saved_audiences = ad_account.get_saved_audiences(fields=['id', 'name', 'time_updated'])
            audience_list = [audience.export_all_data() for audience in saved_audiences]

            # Filtering for each audience type based on keywords
            filtered_audiences = {}
            for audience_type, keywords in keywords_dict.items():
                audience, error = find_most_recent_audience(audience_list, keywords)
                if audience:
                    filtered_audiences[audience_type] = audience
                else:
                    filtered_audiences[audience_type] = {'error': error}

            all_audiences_filtered[ad_account_id] = filtered_audiences

        except Exception as e:
            print(f'An error occurred with account {ad_account_id}: {e}')
            all_audiences_filtered[ad_account_id] = 'Error or No Audiences Found'

        # Sleep to manage rate limits
        time.sleep(1)

    return all_audiences_filtered

account_info = pd.read_csv("/Users/lroberts/Downloads/Bulk Uploader Reference - Sheet1.csv")
account_info.dropna(inplace=True)
account_info['Ad Account ID'] = account_info['Ad Account ID'].apply(lambda x: f'act_{int(x)}')
account_ids = list(account_info['Ad Account ID'][0:5])
# Example usage
keywords_dict = {
    'Broad': ['broad'],
    'W/E/P/E': ['w/e/p/e', 'wep'],
    'Reach/Target Area': ['reach', 'target area']
}

audiences_filtered = get_audiences(account_ids, keywords_dict)

# Initialize lists to store data and version consistency check
ad_account_ids = []
broad_ids = []
wepe_ids = []
reach_ids = []
version_consistency = []

# Extract data and perform version consistency check
for account_id, audience_data in audiences_filtered.items():
    if isinstance(audience_data, str):
        # Error occurred for this account, skip processing
        print(f"Error for account {account_id}: {audience_data}")
        ad_account_ids.append(account_id)
        broad_ids.append(None)
        wepe_ids.append(None)
        reach_ids.append(None)
        version_consistency.append("Error")
        continue
    ad_account_ids.append(account_id)
    broad_ids.append(audience_data['Broad'].get('id') if 'Broad' in audience_data and 'id' in audience_data['Broad'] else None)
    wepe_ids.append(audience_data['W/E/P/E'].get('id') if 'W/E/P/E' in audience_data and 'id' in audience_data['W/E/P/E'] else None)
    reach_ids.append(audience_data['Reach/Target Area'].get('id') if 'Reach/Target Area' in audience_data and 'id' in audience_data['Reach/Target Area'] else None)

    try:
        # Extract version numbers
        versions = [extract_version(audience_data.get(aud_type, {}).get('name', '')) for aud_type in ['Broad', 'W/E/P/E', 'Reach/Target Area']]
        
        # Check if all versions are the same or if there's no version
        if len(set(versions)) != 1 and not all(v is None for v in versions):
            version_consistency.append('Inconsistent')
        else:
            version_consistency.append('Consistent')
    except Exception as e:
        print(f"An unexpected error occurred for account {account_id}: {e}")
        version_consistency.append("Error")
# Create DataFrame for audience data
audience_df = pd.DataFrame({
    'broad_id': broad_ids,
    'wepe_id': wepe_ids,
    'reach_id': reach_ids,
    'version_consistency': version_consistency
}, index=ad_account_ids)

# Merge with existing DataFrame
updated_df = pd.merge(account_info, audience_df, how='left', left_on='Ad Account ID', right_index=True)

# Save to CSV
downloads_path = "/Users/lroberts/Downloads/"
current_date = datetime.now().strftime("%Y%m%d")
filename = f"audience_ids_{current_date}.csv"
full_path = os.path.join(downloads_path, filename)

updated_df.to_csv(full_path, index=False)
print(f"DataFrame exported to {full_path}")