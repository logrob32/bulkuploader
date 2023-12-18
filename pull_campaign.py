from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
import os

def get_campaign_all(campaign_id):
    FacebookAdsApi.init(access_token=os.getenv('FACEBOOK_ACCESS_TOKEN'),
                        app_id=os.getenv('FACEBOOK_APP_ID'),
                        app_secret=os.getenv('FACEBOOK_APP_SECRET'))

    campaign = Campaign(campaign_id)
    campaign.remote_read(fields=[
        Campaign.Field.id,
        Campaign.Field.name,
        Campaign.Field.objective,
        Campaign.Field.status,
        Campaign.Field.special_ad_categories,
        # Add other fields as needed
    ])

    all_ad_sets = []
    all_ads = []
    ad_sets = campaign.get_ad_sets(fields=[
        'id',
        'name',
        'targeting',
        'daily_budget',
        'billing_event',
        'optimization_goal',
        # Add other fields as needed
    ])

    for ad_set in ad_sets:
        all_ad_sets.append(ad_set)
        ads = ad_set.get_ads(fields=[
            'id',
            'name',
            'creative',
            'status',
            # Add other fields as needed
        ])
        for ad in ads:
            all_ads.append(ad)

    return campaign, all_ad_sets, all_ads

# Example usage
#campaign_id = '23854378125310434'  # Replace with your actual campaign ID
#campaign, ad_sets, ads = get_campaign_all(campaign_id)
print(campaign)
for ad_set in ad_sets:
    print(ad_set)
for ad in ads:
    print(ad)
