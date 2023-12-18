from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import os

# Initialize the Facebook API with your credentials
FacebookAdsApi.init(access_token=os.getenv('FACEBOOK_ACCESS_TOKEN'),
                    app_id=os.getenv('FACEBOOK_APP_ID'),
                    app_secret=os.getenv('FACEBOOK_APP_SECRET'))

# Replace 'act_<AD_ACCOUNT_ID>' with your actual ad account ID
my_account = AdAccount('act_421716725127524')

# Attempt to fetch campaigns
try:
    campaigns = my_account.get_campaigns()
    print(campaigns)
except Exception as e:
    print(f'An error occurred: {e}')
