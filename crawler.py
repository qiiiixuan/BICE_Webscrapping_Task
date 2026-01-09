# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Data from giving.sg is injected dynamically by JavaScript, so we use API calls via POST requests to get the data directly.
# A POST request requires a URL, a JSON payload, and headers (to mimic a real browser request).
# These can be found by inspecting the network traffic in the browser's developer tools while navigating the website.

# One thing to note is the moduleVersion and apiVersion in the payloads.
# These versions may change over time as the website is updated, which may break the code, so we have to update them accordingly by checking the network traffic again.
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Import necessary libraries
import requests         # For making HTTP requests to scrape the website
import pandas as pd     # For creating dataframes to store scraped data into Excel files

from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

# Headers are constant for all requests
headers = {
    "Content-Type": "application/json",
    "Cookies": "osVisitor=ab568d35-ada5-4e33-8b24-409ea3b13fa2; nr1Users=lid%3dAnonymous%3btuu%3d0%3bexp%3d0%3brhs%3dXBC1ss1nOgYW1SmqUjSxLucVOAg%3d%3bhmc%3dODE1uhixQBFObTvV7Oa%2bAblvPQ8%3d; nr2Users=crf%3dT6C%2b9iB49TLra4jEsMeSckDMNhQ%3d%3buid%3d0%3bunm%3d; gsgCookieConsent=false; osVisit=11c3c1fb-e875-4b23-b012-114ad89c9c5c",
    "x-csrftoken": "T6C+9iB49TLra4jEsMeSckDMNhQ=",
}

# ----------------------------------------------------------------------------------------------------------------
# 1. Methods to obtain Trending and Donate Now lists from main page
# ----------------------------------------------------------------------------------------------------------------

def getTrendingSlugs():
    url = "https://www.giving.sg/screenservices/NVPC_ContentManagement_CW/ContentManagement/HomePage_Web/DataActionGetHomePageDetails"
    payload = {
        "screenData": {
            "variables": {},
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "V3ueqs5UHzgkmVWRu5AtWA",
        },
        "viewName": "a_Common.home",
    }
    data = requests.post(url, json=payload, headers=headers)

    slugs = []
    trendingList = data.json()['data']['VM_HomePage']['Content']['List'][1]['VMC_Highlight']['VMC_FeatureItemList']['List']
    for campaign in trendingList:
        slugs.append(campaign['UrlSlug'])
    
    return slugs


def getTrending():
    slugList = getTrendingSlugs()
    slugList = list(map(lambda x: {"UrlTypeId": "1", "UrlSlug": x}, slugList))

    url = "https://www.giving.sg/screenservices/NVPC_ContentManagement_CW/Home/HomePage_01b_Highlight/DataActionGetFeatureItems"
    payload = {
        "screenData": {
            "variables": {
                "VMC_Highlight": {
                    "BackgroundImageUrl_Desktop": "/res/GetMedia/image_3_38920f3846.png?103001&f=false",
                    "BackgroundImageUrl_Mobile": "/res/GetMedia/image_3_38920f3846.png?103001&f=false",
                    "BackgroundImageUrl_Tablet": "/res/GetMedia/image_3_38920f3846.png?103001&f=false",
                    "Header": "<h2><strong>Trending</strong></h2>",
                    "VMC_FeatureItemList": {
                        "List": slugList,
                    },
                }, 
                "_vMC_HighlightInDataFetchStatus": 1,
            }
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "JXW93X9ZRketw06uK40GXQ",
        },
        "viewName": "a_Common.home",
    }
    data = requests.post(url, json=payload, headers=headers)

    trendingList = data.json()['data']['VM_Highlight']['List']

    return list(map(lambda x: x['VM_CampaignCard']['Title'], trendingList))


def getDonateNow():
    url = "https://www.giving.sg/screenservices/NVPC_ContentManagement_CW/Home/HomePage_01c_Recommendation/DataActionGetRecommendedActivities"
    payload = {
        "screenData": {
            "variables": {
                "VMC_Recommendation": {
                    "BackgroundImageUrl_Desktop": "/res/GetMedia/Figma_Background_dark_blue_372677ffa2.png?023956&f=false",
                    "BackgroundImageUrl_Mobile": "/res/GetMedia/Figma_Background_dark_blue_372677ffa2.png?023956&f=false",
                    "BackgroundImageUrl_Tablet": "/res/GetMedia/Figma_Background_dark_blue_372677ffa2.png?023956&f=false",
                    "Header": "<h2><span style=\"color:hsl(0,0%,100%);\"><strong>Donate Now</strong></span></h2>",
                    "RecommendationTypeId": "1",
                }, 
                "_vMC_RecommendationInDataFetchStatus": 1,
            }
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "HLo05GLUH8jtube1K6HEyQ",
        },
        "viewName": "a_Common.home",
    }
    data = requests.post(url, json=payload, headers=headers)

    donateNowList = data.json()['data']['VM_Recommendation']['List']

    return list(map(lambda x: x['VM_CampaignCard']['Title'], donateNowList))

# ----------------------------------------------------------------------------------------------------------------
# 2. Methods to obtain total charity and campaign count
# ----------------------------------------------------------------------------------------------------------------

def getCharityCount():
    url = "https://www.giving.sg/screenservices/NVPC_Donating_CW/CampaignDetails/z_DonateList_01_Charities/DataActionGetCharityList"
    payload = {
        "screenData": {
            "variables": {
                "FilterBy_CharityVisibilityId": 0,
                "FilterBy_IsOnlyBookmarked": False,
                "FilterBy_IsOnlyTaxDeductible": False,
                "FilterBy_SelectedCauseList": {
                    "List": [],
                    "EmptyListItem": {
                        "Description": "",
                        "GroupName": "",
                        "ImageUrlOrIconClass": "",
                        "Label": "",
                        "Value": "",
                    },
                },
                "FilterBy_SortTypeId": 3,
                "FilterSide_CharityVisibilityId": 0,
                "FilerSide_IsOnlyBookmarked": False,
                "FilterSide_IsOnlyTaxDeductible": False,
                "FilterSide_SelectedCauseList": {
                    "List": [],
                    "EmptyListItem": {
                        "Description": "",
                        "GroupName": "",
                        "ImageUrlOrIconClass": "",
                        "Label": "",
                        "Value": "",
                    },
                },
                "FilterSide_SortTypeId": 3,
                "Filter_Count": 0,
                "Filter_IsActive": False,
                "IsExplore": False,
                "IsRefresh": True,
                "Result_IsFirstLoad": True,
                "Result_PageSize": 1,
                "Result_StartIndex": 0,
                "SearchKeyword": "",
                "_isExploreInDataFetchStatus": 1,
                "_isRefreshInDataFetchStatus": 1,
                "_searchKeywordInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "t28p3_D6zK7nE0WOG7gIsg",
        },
        "viewName": "d_Campaigns.Donate",
    }
    data = requests.post(url, json=payload, headers=headers)

    charityCount = data.json()['data']['CharityCount']

    return int(charityCount)


def getCampaignCount():
    url = "https://www.giving.sg/screenservices/NVPC_Donating_CW/CampaignDetails/z_DonateList_02_Campaigns/DataActionGetCampaignList"
    payload = {
        "screenData": {
            "variables": {
                "FilterBy_CampaignTypeSelected": 0,
                "FilterBy_CampaignVisibilityId": 0,
                "FilterBy_IsOnlyBookmarked": False,
                "FilterBy_IsOnlyTaxDeductible": False,
                "FilterBy_IsOnlyUnderserved": False,
                "FilterBy_IsSG60Featured": False,
                "FilterBy_SelectedCauseList": {
                    "List": [],
                    "EmptyListItem": {
                        "Description": "",
                        "GroupName": "",
                        "ImageUrlOrIconClass": "",
                        "Label": "",
                        "Value": "",
                    },
                },
                "FilterBy_SortTypeId": 7,
                "FilterSide_CampaignVisibilityId": 0,
                "FilerSide_IsOnlyBookmarked": False,
                "FilterSide_IsOnlyTaxDeductible": False,
                "FilterSide_IsOnlyUnderserved": False,
                "FilterSide_IsSG60Featured": False,
                "FilterSide_SelectedCauseList": {
                    "List": [],
                    "EmptyListItem": {
                        "Description": "",
                        "GroupName": "",
                        "ImageUrlOrIconClass": "",
                        "Label": "",
                        "Value": "",
                    },
                },
                "FilterSide_SortTypeId": 7,
                "Filter_Count": 0,
                "Filter_IsActive": False,
                "InitialCollectionTagIdList": {
                    "List": [],
                    "EmptyListItem": 0
                },
                "IsExplore": False,
                "IsRefresh": True,
                "Result_IsFirstLoad": True,
                "Result_PageSize": 1,
                "Result_StartIndex": 0,
                "SearchKeyword": "",
                "_initialCollectionTagIdListInDataFetchStatus": 1,
                "_isExploreInDataFetchStatus": 1,
                "_isRefreshInDataFetchStatus": 1,
                "_searchKeywordInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "8S64ql8R2cKB3o5wd+vJ7g",
        },
        "viewName": "d_Campaigns.Donate",
    }
    data = requests.post(url, json=payload, headers=headers)

    campaignCount = data.json()['data']['CampaignCount']

    return int(campaignCount)

# ----------------------------------------------------------------------------------------------------------------
# 3. Methods to get entire lists of charities and campaigns
# ----------------------------------------------------------------------------------------------------------------

def getCharityList():
    url = "https://www.giving.sg/screenservices/NVPC_Donating_CW/CampaignDetails/z_DonateList_01_Charities/DataActionGetCharityList"
    payload = {
        "screenData": {
            "variables": {
                "FilterBy_CharityVisibilityId": 0,
                "FilterBy_IsOnlyBookmarked": False,
                "FilterBy_IsOnlyTaxDeductible": False,
                "FilterBy_SelectedCauseList": {
                    "List": [],
                    "EmptyListItem": {
                        "Description": "",
                        "GroupName": "",
                        "ImageUrlOrIconClass": "",
                        "Label": "",
                        "Value": "",
                    },
                },
                "FilterBy_SortTypeId": 3,
                "FilterSide_CharityVisibilityId": 0,
                "FilerSide_IsOnlyBookmarked": False,
                "FilterSide_IsOnlyTaxDeductible": False,
                "FilterSide_SelectedCauseList": {
                    "List": [],
                    "EmptyListItem": {
                        "Description": "",
                        "GroupName": "",
                        "ImageUrlOrIconClass": "",
                        "Label": "",
                        "Value": "",
                    },
                },
                "FilterSide_SortTypeId": 3,
                "Filter_Count": 0,
                "Filter_IsActive": False,
                "IsExplore": False,
                "IsRefresh": True,
                "Result_IsFirstLoad": True,
                "Result_PageSize": getCharityCount(),
                "Result_StartIndex": 0,
                "SearchKeyword": "",
                "_isExploreInDataFetchStatus": 1,
                "_isRefreshInDataFetchStatus": 1,
                "_searchKeywordInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "t28p3_D6zK7nE0WOG7gIsg",
        },
        "viewName": "d_Campaigns.Donate",
    }
    data = requests.post(url, json=payload, headers=headers)

    charityList = data.json()['data']['VM_CharityCardItemList']['List']

    return charityList


def getCampaignList():
    url = "https://www.giving.sg/screenservices/NVPC_Donating_CW/CampaignDetails/z_DonateList_02_Campaigns/DataActionGetCampaignList"
    payload = {
        "screenData": {
            "variables": {
                "FilterBy_CampaignTypeSelected": 0,
                "FilterBy_CampaignVisibilityId": 0,
                "FilterBy_IsOnlyBookmarked": False,
                "FilterBy_IsOnlyTaxDeductible": False,
                "FilterBy_IsOnlyUnderserved": False,
                "FilterBy_IsSG60Featured": False,
                "FilterBy_SelectedCauseList": {
                    "List": [],
                    "EmptyListItem": {
                        "Description": "",
                        "GroupName": "",
                        "ImageUrlOrIconClass": "",
                        "Label": "",
                        "Value": "",
                    },
                },
                "FilterBy_SortTypeId": 7,
                "FilterSide_CampaignVisibilityId": 0,
                "FilerSide_IsOnlyBookmarked": False,
                "FilterSide_IsOnlyTaxDeductible": False,
                "FilterSide_IsOnlyUnderserved": False,
                "FilterSide_IsSG60Featured": False,
                "FilterSide_SelectedCauseList": {
                    "List": [],
                    "EmptyListItem": {
                        "Description": "",
                        "GroupName": "",
                        "ImageUrlOrIconClass": "",
                        "Label": "",
                        "Value": "",
                    },
                },
                "FilterSide_SortTypeId": 7,
                "Filter_Count": 0,
                "Filter_IsActive": False,
                "InitialCollectionTagIdList": {
                    "List": [],
                    "EmptyListItem": 0
                },
                "IsExplore": False,
                "IsRefresh": True,
                "Result_IsFirstLoad": True,
                "Result_PageSize": getCampaignCount(),
                "Result_StartIndex": 0,
                "SearchKeyword": "",
                "_initialCollectionTagIdListInDataFetchStatus": 1,
                "_isExploreInDataFetchStatus": 1,
                "_isRefreshInDataFetchStatus": 1,
                "_searchKeywordInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "8S64ql8R2cKB3o5wd+vJ7g",
        },
        "viewName": "d_Campaigns.Donate",
    }
    data = requests.post(url, json=payload, headers=headers)

    campaignList = data.json()['data']['CampaignCardItemList']['List']

    return campaignList

# ----------------------------------------------------------------------------------------------------------------
# 4. Methods to get basic info of campaigns (e.g. Guid, TypeCode)
# ----------------------------------------------------------------------------------------------------------------

def getCampaignBasic(slug: str):
    url = "https://www.giving.sg/screenservices/NVPC_Donating_CW/CampaignDetails/CampaignDetails_00/DataActionGetCampaignBasicInfo"
    payload = {
        "screenData": {
            "variables": {
                "CampaignUrlPath": slug,
                "IsAddDonationtoCart": False,
                "IsMobileApp": False,
                "IsShowPopup_OneTime": False,
                "IsShowPopup_Pledge": False,
                "IsUrlProcessed": False,
                "SelectedCartGuid": "",
                "TierDonation": {
                    "Amount": 0, 
                    "ImpactStatementText": "",
                },
                "UtmValue": "",
                "v": "",
                "_campaignUrlPathInDataFetchStatus": 1,
                "_isMobileAppInDataFetchStatus": 1,
                "_vInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "ncuzk4GEARQGTF2xFBzpBQ",
        },
        "viewName": "d_Campaigns.CampaignDetail",
    }
    data = requests.post(url, json=payload, headers=headers)

    campaignBasic = data.json()['data']

    return campaignBasic

# ----------------------------------------------------------------------------------------------------------------
# 5. Methods to get details of charities and campaigns
# ----------------------------------------------------------------------------------------------------------------

def getCharityProfile(uid: str):
    url = "https://www.giving.sg/screenservices/NVPC_CrossDomain_CW/c_EG_Profile/EGProfile_01_About/DataActionGetProfileAbout"
    payload = {
        "screenData": {
            "variables": {
                "CustomDonationAmount": 0,
                "EntityGroupGuid": uid,
                "IsDonateNow": False,
                "PortalID": 1,
                "SelectedCartGuid": "",
                "p_DonateAmount": 0,
                "p_IsShowDonationPopup": False,
                "p_IsShowPledgePopup": False,
                "_entityGroupGuidInDataFetchStatus": 1,
                "_portalIDInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "SETSMk_PuzcUoAZxsq67DA",
        },
        "viewName": "c_EntityGroup.EntityGroupProfile",
    }
    data = requests.post(url, json=payload, headers=headers)

    charityProfile = data.json()['data']['VM_GSG_EGProfileAbout']

    return charityProfile


def getCharitySummary(uid: str):
    url = "https://www.giving.sg/screenservices/NVPC_CrossDomain_CW/c_EG_Profile/EGProfile_00/DataActionGetProfileSummary"
    payload = {
        "screenData": {
            "variables": {
                "EntityGroupGuid": "",
                "PortalID": 1,
                "ShareUrl": "https://www.giving.sg/organisation/profile/" + uid,
                "UrlSlug": uid,
                "UtmRecValue": "",
                "_portalIDInDataFetchStatus": 1,
                "_urlSlugInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "BANifvWJLvlFX45kW2RHPw",
        },
        "viewName": "c_EntityGroup.EntityGroupProfile",
    }
    data = requests.post(url, json=payload, headers=headers)

    charitySummary = data.json()['data']['VM_GSG_EGProfile']

    return charitySummary


def getCampaignDetails(uid: str):
    url = "https://www.giving.sg/screenservices/NVPC_Donating_CW/CampaignDetails/CampaignDetails_01_View/DataActionGetCampaignDetails"
    payload = {
        "screenData": {
            "variables": {
                "ActiveTab": 0,
                "CampaignGuid": uid,
                "IsFirstTime": True,
                "IsMobileApp": False,
                "IsPreview": False,
                "_campaignGuidInDataFetchStatus": 1,
                "_isMobileAppInDataFetchStatus": 1,
                "_isPreviewInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "5qNlzH4K91mFetExEk0kPA",
        },
        "viewName": "d_Campaigns.CampaignDetail",
    }
    data = requests.post(url, json=payload, headers=headers)

    campaignDetails = data.json()['data']['CampaignDetails']

    return campaignDetails


def getCollectiveCampaignDetails(uid: str):
    url = "https://www.giving.sg/screenservices/NVPC_Donating_CW/CollectiveCampaign/CampaignDetails_02_CollectiveCampaignView/DataActionGetCollectiveCampaignDetails"
    payload = {
        "screenData": {
            "variables": {
                "ActiveTab": 0,
                "CampaignGuid": uid,
                "IsFillMiddleContent": True,
                "IsMobileApp": False,
                "IsPreview": False,
                "_campaignGuidInDataFetchStatus": 1,
                "_isMobileAppInDataFetchStatus": 1,
                "_isPreviewInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "03Hfe31l0NANvBkNNI6wxQ",
        },
        "viewName": "d_Campaigns.CampaignDetail",
    }
    data = requests.post(url, json=payload, headers=headers)

    campaignDetails = data.json()['data']['CampaignDetails']

    return campaignDetails


def getCampaignPartners(uid: str):
    url = "https://www.giving.sg/screenservices/NVPC_Donating_CW/CampaignDetails/CampaignPartners/DataActionGetCampaignPartnerList"
    payload = {
        "screenData": {
            "variables": {
                "CampaignGuid": uid,
                "CampaignPartnerDescription": "",
                "PageSize": 30,
                "ShowCardPopup": False,
                "ViewAllClicked": False,
                "_campaignGuidInDataFetchStatus": 1,
            },
        },
        "versionInfo": {
            "moduleVersion": "UIg6Cxr4hlTDlmZmxLS++w",
            "apiVersion": "vXv1+2_sASBhgTcc1pIZHg",
        },
        "viewName": "d_Campaigns.CampaignDetail",
    }
    data = requests.post(url, json=payload, headers=headers)

    partnerList = data.json()['data']['CampaignPartnerList']['List']

    return partnerList

# ----------------------------------------------------------------------------------------------------------------
# 6. Methods to get excel importable dataframe of charities and campaigns
# ----------------------------------------------------------------------------------------------------------------

def getCharityData(profile, summary, index: int, noc: int):
    root = "https://www.giving.sg"
    name = "\'" + summary['EntityGroupName'] if summary['EntityGroupName'][0] == '=' else summary['EntityGroupName']
    photos = list(map(lambda x: root + x['Url'], list(filter(lambda y: y['AssetTypeId'] == 1, profile['AssetList']['List']))))
    videos = list(map(lambda x: x['Url'], list(filter(lambda y: y['AssetTypeId'] == 2, profile['AssetList']['List']))))
    description = "\'" + profile['AboutStatement'] if profile['AboutStatement'][0] == '=' else profile['AboutStatement']
    description = ILLEGAL_CHARACTERS_RE.sub("", description)
    donationAmounts = list(map(lambda x: str(x['Value']), profile['DonationTierList']['List']))
    messages = list(map(lambda x: x['ImpactStatement'], profile['DonationTierList']['List']))
    hasContactInfo = profile['ContactPersonEmail'] != "" or profile['ContactPersonName'] != "" or profile['ContactPersonPhone'] != ""
    
    charityData = pd.DataFrame({
        "Page Number": [(index - index%30)/30 + 1],
        "Organisation": [name],
        "Webpage Link": [summary['WebsiteUrl']],
        "Photos": [" | ".join(photos)],
        "Videos": [" | ".join(videos)],
        "Organisation Description": [description],
        "Suggested Donation Amounts": [", ".join(donationAmounts)],
        "Donation Amount Messages": [" | ".join(messages)],
        "Contact Information Provided": ["Yes" if hasContactInfo else "No"],
        "Tax-deductible": ["Yes" if profile['IsTaxDeductible'] else "No"],
        "Number of Campaigns": [noc],
        "Date of Extraction": [pd.Timestamp.now().strftime("%Y-%m-%d")],
    })

    return charityData


def getCampaignData(details, index: int, daysLeft: int, repeatedCount: int, trending, donateNow):
    root = "https://www.giving.sg"
    title = "\'" + details['CampaignTitle'] if details['CampaignTitle'][0] == '=' else details['CampaignTitle']
    nameCharity = "\'" + details['CharityName'] if details['CharityName'][0] == '=' else details['CharityName']
    nameCreator = "\'" + details['CreatorName'] if details['CreatorName'][0] == '=' else details['CreatorName']
    photos = list(map(lambda x: root + x['AssetURL'], list(filter(lambda y: y['AssetURLType'] == "1", details['Assets']['List']))))
    videos = list(map(lambda x: x['AssetURL'], list(filter(lambda y: y['AssetURLType'] == "2", details['Assets']['List']))))
    category = list(map(lambda x: x['Name'], details['Causes']['List']))
    descriptionCampaign = "\'" + details['AboutCampaign'] if details['AboutCampaign'][0] == '=' else details['AboutCampaign']
    descriptionCampaign = ILLEGAL_CHARACTERS_RE.sub("", descriptionCampaign)
    donationAmounts = list(map(lambda x: str(x['Amount']), details['DonationTiers']['List']))
    messages = list(map(lambda x: x['ImpactStatementText'], details['DonationTiers']['List']))
    descriptionOrganisation = "\'" + details['AboutCharity'] if details['AboutCharity'] != "" and details['AboutCharity'][0] == '=' else details['AboutCharity']
    descriptionOrganisation = ILLEGAL_CHARACTERS_RE.sub("", descriptionOrganisation)
    hasContactInfo = details['ContactEmail'] != "" or details['ContactNumber'] != "" or details['ContactPersonName'] != ""
    totalDonors = details['TotalDonors']
    startDate = "-" if details['CampaignStartDate'] == "1900-01-01" else details['CampaignStartDate']
    endDate = "-" if details['CampaignEndDate'] == "1900-01-01" else details['CampaignEndDate']
    adv = "-"
    if details['CampaignStartDate'] != "1900-01-01":
        df = pd.DataFrame({
            'Date': [startDate, pd.Timestamp.now().strftime("%Y-%m-%d")],
        })
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.astype('int64').dtypes
        startWeek = df['Date'].dt.week[0]
        currentWeek = df['Date'].dt.week[1]
        weeks = currentWeek - startWeek
        if df['Date'].dt.year[0] == df['Date'].dt.year[1]:
            weeks += 52 * (df['Date'].dt.year[1] - df['Date'].dt.year[0])
        adv = totalDonors/weeks


    campaignData = pd.DataFrame({
        "Page Number": [(index - index%30)/30 + 1],
        "Campaign Title": [title],
        "Organisation": [nameCharity],
        "Individual": [nameCreator],
        "Photos": [" | ".join(photos)], 
        "Videos": [" | ".join(videos)], 
        "Category": [", ".join(category)],
        "Campaign Description": [descriptionCampaign],
        "Suggested Donation Amounts": [", ".join(donationAmounts)],
        "Donation Amount Messages": [" | ".join(messages)],
        "Organisation Description": [descriptionOrganisation],
        "Contact Information Provided": ["Yes" if hasContactInfo else "No"],
        "Tax-deductible": ["Yes" if details['IsTaxDeductible'] else "No"],
        "Donation Amount Raised": [details['CurrentAmount']],
        "Donation Goal": [details['TargetAmount']],
        "Number of Donors": [totalDonors],
        "Days To Go": [daysLeft],
        "Featured on Trending": ["Yes" if title in trending else "No"],
        "Featured on Donate Now": ["Yes" if title in donateNow else "No"],
        "Campaign Start Date": [startDate],
        "Campaign End Date": [endDate],
        "Average Donor Visits (per week)": [adv],
        "Repeated Count": [repeatedCount],
        "Date of Extraction": [pd.Timestamp.now().strftime("%Y-%m-%d")],
    })

    return campaignData


def getCollectiveCampaignData(details, partners, index: int, daysLeft: int, repeatedCount: int, trending, donateNow):
    root = "https://www.giving.sg"
    title = "\'" + details['CampaignTitle'] if details['CampaignTitle'][0] == '=' else details['CampaignTitle']
    nameCharities = list(map(lambda x: "\'" + x['Title'] if x['Title'][0] == '=' else x['Title'], partners))
    nameCreator = "\'" + details['CreatorName'] if details['CreatorName'][0] == '=' else details['CreatorName']
    photos = list(map(lambda x: root + x['AssetURL'], list(filter(lambda y: y['AssetURLType'] == "1", details['Assets']['List']))))
    videos = list(map(lambda x: x['AssetURL'], list(filter(lambda y: y['AssetURLType'] == "2", details['Assets']['List']))))
    category = list(map(lambda x: x['Name'], details['Causes']['List']))
    descriptionCampaign = "\'" + details['AboutCampaign'] if details['AboutCampaign'][0] == '=' else details['AboutCampaign']
    descriptionCampaign = ILLEGAL_CHARACTERS_RE.sub("", descriptionCampaign)
    donationAmounts = []
    messages = []
    descriptionOrganisation = "\'" + details['AboutCreator'] if details['AboutCreator'] != '' and details['AboutCreator'][0] == '=' else details['AboutCreator']
    descriptionOrganisation = ILLEGAL_CHARACTERS_RE.sub("", descriptionOrganisation)
    hasContactInfo = details['ContactEmail'] != "" or details['ContactNumber'] != "" or details['ContactPersonName'] != ""
    totalDonors = details['TotalUniqueDonors']
    startDate = "-" if details['CampaignStartDate'] == "1900-01-01" else details['CampaignStartDate']
    endDate = "-" if details['CampaignEndDate'] == "1900-01-01" else details['CampaignEndDate']
    adv = "-"
    # if details['CampaignStartDate'] != "1900-01-01":
    #     df = pd.DataFrame({
    #         'Date': [startDate, pd.Timestamp.now().strftime("%Y-%m-%d")],
    #     })
    #     df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    #     df.astype('int64').dtypes
    #     startWeek = df['Date'].dt.week[0]
    #     currentWeek = df['Date'].dt.week[1]
    #     weeks = currentWeek - startWeek
    #     if df['Date'].dt.year[0] == df['Date'].dt.year[1]:
    #         weeks += 52 * (df['Date'].dt.year[1] - df['Date'].dt.year[0])
    #     adv = totalDonors/weeks


    campaignData = pd.DataFrame({
        "Page Number": [(index - index%30)/30 + 1],
        "Campaign Title": [title],
        "Organisation": [" | ".join(nameCharities)],
        "Individual": [nameCreator],
        "Photos": [" | ".join(photos)], 
        "Videos": [" | ".join(videos)], 
        "Category": [", ".join(category)],
        "Campaign Description": [descriptionCampaign],
        "Suggested Donation Amounts": [", ".join(donationAmounts)],
        "Donation Amount Messages": [" | ".join(messages)],
        "Organisation Description": [descriptionOrganisation],
        "Contact Information Provided": ["Yes" if hasContactInfo else "No"],
        "Tax-deductible": ["No"],
        "Donation Amount Raised": [details['CurrentAmount']],
        "Donation Goal": [details['TargetAmount']],
        "Number of Donors": [totalDonors],
        "Days To Go": [daysLeft],
        "Featured on Trending": ["Yes" if title in trending else "No"],
        # "Featured on Donate Now": ["Yes" if title in donateNow else "No"],
        # "Campaign Start Date": [startDate],
        "Campaign End Date": [endDate],
        # "Average Donor Visits (per week)": [adv],
        "Repeated Count": [repeatedCount],
        "Date of Extraction": [pd.Timestamp.now().strftime("%Y-%m-%d")],
    })

    return campaignData

# ----------------------------------------------------------------------------------------------------------------
# 7. Methods to obtain excel importable data of charities and campaigns as one large dataframe
# ----------------------------------------------------------------------------------------------------------------

def scrapeCharityData():
    charityList = getCharityList()
    charityData = pd.DataFrame({
        "Page Number": [],
        "Organisation": [],
        "Webpage Link": [],
        "Photos": [], 
        "Videos": [], 
        "Organisation Description": [],
        "Suggested Donation Amounts": [],
        "Donation Amount Messages": [],
        "Contact Information Provided": [],
        "Tax-deductible": [],
        "Number of Campaigns": [],
        "Date of Extraction": [],
    })

    length = len(charityList)
    for index,charity in enumerate(charityList):
        if (index + 1) % 30 == 0:
            print("Scraped charity data: " + str(index + 1) + "/" + str(length))
        
        uid = charity['GUID']
        profile = getCharityProfile(uid)
        summary = getCharitySummary(uid)
        noc = charity['TotalCampaigns']

        charityData = pd.concat([charityData, getCharityData(profile, summary, index, noc)], ignore_index=True)

    return charityData


def scrapeCampaignData():
    campaignList = getCampaignList()
    trending = getTrending()
    donateNow = getDonateNow()
    campaignData = pd.DataFrame({
        "Page Number": [],
        "Campaign Title": [],
        "Organisation": [],
        "Individual": [],
        "Photos": [], 
        "Videos": [], 
        "Category": [],
        "Campaign Description": [],
        "Suggested Donation Amounts": [],
        "Donation Amount Messages": [],
        "Organisation Description": [],
        "Contact Information Provided": [],
        "Tax-deductible": [],
        "Donation Amount Raised": [],
        "Donation Goal": [],
        "Number of Donors": [],
        "Days To Go": [],
        "Featured on Trending": [],
        # "Featured on Donate Now": [],
        # "Campaign Start Date": [],
        "Campaign End Date": [],
        # "Average Donor Visits (per week)": [],
        "Repeated Count": [],
        "Date of Extraction": [],
    })

    length = len(campaignList)
    for index,campaign in enumerate(campaignList):
        if (index + 1) % 30 == 0:
            print("Scraped campaign data: " + str(index + 1) + "/" + str(length))
        
        repeatedCount = 1
        url = campaign['CampaignUrl']
        daysLeft = campaign['DaysLeft']
        title = "\'" + campaign['Title'] if campaign['Title'][0] == '=' else campaign['Title']
        titleList = campaignData["Campaign Title"].tolist()
        
        if title in titleList:
            id = titleList.index(title)
            repeatedCount = campaignData['Repeated Count'][id] + 1
            campaignData.loc[id, 'Repeated Count'] = repeatedCount
        
        campaignBasic = getCampaignBasic(url)
        uid = campaignBasic['CampaignGuid']
        typeCode = campaignBasic['TypeCode']
        
        if typeCode == 2:
            details = getCampaignDetails(uid)
            campaignData = pd.concat([campaignData, getCampaignData(details, index, daysLeft, repeatedCount, trending, donateNow)], ignore_index=True)
        elif typeCode == 3:
            details = getCollectiveCampaignDetails(uid)
            partners = getCampaignPartners(uid)
            campaignData = pd.concat([campaignData, getCollectiveCampaignData(details, partners, index, daysLeft, repeatedCount, trending, donateNow)], ignore_index=True)

    return campaignData

# Write data to Excel
def main():
    scrapeCharityData().to_excel("Data.xlsx", sheet_name="Charities")
    with pd.ExcelWriter(
        "Data.xlsx",
        engine="openpyxl",
        mode="a",
    ) as writer:
        scrapeCampaignData().to_excel(writer, sheet_name="Campaigns")


if __name__ == "__main__":
    main()
