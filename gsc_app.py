import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

def print_table(response, title):
    """Prints a response table with keys, clicks, impressions, CTR, and position."""
    print(f"\n--{title}:")
    if 'rows' not in response:
        print("Empty response")
        return
    rows = response['rows']
    row_format = "{:<20}" + "{:>20}" * 4
    print(row_format.format("Keys", "Clicks", "Impressions", "CTR", "Position"))
    for row in rows:
        keys = ",".join(row.get("keys", [""]))
        print(row_format.format(
            keys, row["clicks"], row["impressions"], row["ctr"], row["position"]))

def execute_request(service, property_uri, request):
    """Executes a searchAnalytics.query request."""
    try:
        return service.searchanalytics().query(
            siteUrl=property_uri, body=request).execute()
    except HttpError as e:
        print(f"Error executing request: {e}")
        return {}

def gsc_auth(scopes, credentials_file, token_file):
    """Authenticates with Google Search Console and returns the service."""
    creds = None
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, scopes)
        except Exception as e:
            print(f"Error loading token: {e}")
    if not creds or not creds.valid:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0, prompt="select_account")
            with open(token_file, "w") as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"Authentication error: {e}")
            exit(1)
    return build("searchconsole", "v1", credentials=creds)

# Configuration
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
CREDENTIALS_FILE = r"credentials2.json"
TOKEN_FILE = r"token.json"

# Authenticate and get service
try:
    webmasters_service = gsc_auth(SCOPES, CREDENTIALS_FILE, TOKEN_FILE)
except Exception as e:
    print(f"Failed to initialize service: {e}")
    exit(1)

# Retrieve list of all sites (for debugging)
try:
    site_list = webmasters_service.sites().list().execute()
    print("\nAll sites in Search Console:")
    if not site_list.get("siteEntry", []):
        print("No sites found in Search Console.")
        exit(1)
    for site in site_list.get("siteEntry", []):
        print(f"Site: {site['siteUrl']}, Permission: {site['permissionLevel']}")
except HttpError as e:
    print(f"Error retrieving site list: {e}")
    exit(1)

# Filter verified sites (URL prefix and Domain properties)
verified_sites_urls = [s["siteUrl"] for s in site_list.get("siteEntry", [])
                      if s["permissionLevel"] in ["siteOwner", "siteFullUser"]]

# Print verified sites and their sitemaps
if not verified_sites_urls:
    print("No verified sites found (Owner or Full permissions required).")
    exit(1)

for site_url in verified_sites_urls:
    print(f"\nVerified site: {site_url}")
    try:
        sitemaps = webmasters_service.sitemaps().list(siteUrl=site_url).execute()
        if "sitemap" in sitemaps:
            sitemap_urls = [s["path"] for s in sitemaps["sitemap"]]
            print(f"Sitemaps: {sitemap_urls}")
        else:
            print("No sitemaps found.")
    except HttpError as e:
        print(f"Error retrieving sitemaps: {e}")

    # Execute search analytics query
    request = {
        "startDate": "2025-05-18",  # 90 days ago from Aug 17, 2025
        "endDate": "2025-08-17",
        "dimensions": ["date"]
    }
    response = execute_request(webmasters_service, site_url, request)
    print_table(response, f"Search Analytics for {site_url}")