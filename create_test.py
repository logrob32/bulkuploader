from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
import os

# Initialize the API with your access token, app ID, and app secret
FacebookAdsApi.init(access_token=os.getenv('FACEBOOK_ACCESS_TOKEN'),
                    app_id=os.getenv('FACEBOOK_APP_ID'),
                    app_secret=os.getenv('FACEBOOK_APP_SECRET'))

# Replace with your actual ad account ID
ad_account_id = 'act_421716725127524'

fields = []
params = {
    'name': 'My campaign',
    'objective': 'OUTCOME_TRAFFIC',
    'status': 'PAUSED',
    'special_ad_categories': [],
}

# Use the ad_account_id variable in the create_campaign call
campaign = AdAccount(ad_account_id).create_campaign(
    fields=fields,
    params=params,
)

# Print the campaign object
print(campaign)
