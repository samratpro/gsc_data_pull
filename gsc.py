from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import date, timedelta

# Auth
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
KEY_FILE = 'credentials.json'
credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
service = build('searchconsole', 'v1', credentials=credentials)

# Site
site_list = service.sites().list().execute()
for site in site_list.get('siteEntry', []):
    print(site['siteUrl'], "-", site['permissionLevel'])  # check if site is listed and permission is allowed

# Date range
end_date = date.today()
start_date = end_date - timedelta(days=30)

# Query
request = {
    'startDate': start_date.isoformat(),
    'endDate': end_date.isoformat(),
    'dimensions': ['query'],
    'rowLimit': 1000,
}

response = service.searchanalytics().query(siteUrl='https://sajobsplug.co.za/', body=request).execute()

rows = response.get('rows', [])
print("Rows returned:", len(rows))
# print(rows[:3])  # quick peek

df = pd.DataFrame([{
    'query': row['keys'][0],
    'clicks': row.get('clicks', 0),
    'impressions': row.get('impressions', 0),
    'ctr': row.get('ctr', 0),
    'position': row.get('position', 0),
} for row in rows])

print(df.head())
