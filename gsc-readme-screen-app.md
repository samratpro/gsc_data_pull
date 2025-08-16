# Google Search Console API Connection Setup

This guide explains how to set up and connect to the Google Search Console (GSC) API using a Python script that opens a browser popup for authentication, allowing users to select a Gmail account and auto-connect without manual code entry. The script retrieves verified sites, sitemaps, and search analytics data (clicks, impressions, CTR, position).

## Prerequisites
- A Google account with access to Google Search Console (e.g., `name@gmail.com`).
- A verified site in GSC.
- Python 3.x and a virtual environment (e.g., `\venv`).
- The `credentials2.json` file from Google Cloud Console.

## Setup Steps

### Step 1: Enable Google Search Console API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Select or create a project (e.g., "GSC Data Pull").
3. Navigate to **APIs & Services** > **Library**.
4. Search for **Google Search Console API** and click **Enable**.

### Step 2: Create OAuth 2.0 Client ID for Desktop App
1. In Google Cloud Console, go to **APIs & Services** > **Credentials**.
2. Click **Create Credentials** > **OAuth 2.0 Client IDs**.
3. Select **Desktop app** as the application type.
4. Enter a name (e.g., "GSC Desktop Client") and click **Create**.
5. Download the JSON file (e.g., `client_secret_*.json`).
6. Rename the file to `credentials2.json` and save it to `\gsc\`.

### Step 3: Configure OAuth Consent Screen and Add Test User
1. In Google Cloud Console, go to **APIs & Services** > **OAuth consent screen**.
2. If not already configured, set up the consent screen:
   - Choose **External** user type.
   - Enter an **App name** (e.g., "GSC Data Pull"), a user support email, and developer contact email (e.g., `nichescl@gmail.com`).
   - Add the scope: `https://www.googleapis.com/auth/webmasters.readonly`.
   - Save and continue through the steps.
3. Under **Test users**, click **+ Add users**.
4. Add your Google account (e.g., `name@gmail.com`) as a test user and save.
   - This allows authentication while the app is in testing mode.
5. **Optional for Production**: To allow non-test users, set the app to **Production** and submit for verification (requires a privacy policy URL and domain). For personal use, testing mode is sufficient.

### Step 4: Verify Site Access in Google Search Console
1. Go to [Google Search Console](https://search.google.com/search-console).
2. Sign in with your Google account (e.g., `name@gmail.com`).
3. Ensure your site (e.g., `https://your-site.com/`) is added as a property:
   - Add a **URL Prefix** property (e.g., `https://your-site.com/`) or **Domain** property (e.g., `your-site.com`).
   - Complete verification (e.g., via DNS TXT record or HTML meta tag).
4. Go to **Settings** > **Users and permissions**.
5. Ensure your account has **Full** or **Owner** permissions for the site. If not, add `name@gmail.com` with appropriate permissions.

### Step 5: Install Python Dependencies
1. Activate your virtual environment:
   ```bash
   \venv\Scripts\activate
   ```
2. Install required libraries:
   ```bash
   pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
   ```

### Step 6: Run the Python Script
1. Save the provided Python script (e.g., `gsc_auto_connect_debug.py`) to `E:\ML Practice\gsc\`.
2. Ensure `credentials2.json` is in `E:\ML Practice\gsc\`.
3. Run the script:
   ```bash
   "\venv\Scripts\python.exe" "\gsc\gsc_auto_connect_debug.py"
   ```
4. A browser popup will open:
   - Select your Gmail account (e.g., `name@gmail.com`).
   - Authorize the app. The script will auto-capture the token and save it to `token.json`.
5. The script will:
   - List all GSC sites and their permission levels (for debugging).
   - Show verified sites (with **Owner** or **Full** permissions).
   - Retrieve sitemaps and search analytics data (clicks, impressions, CTR, position) for a recent date range.

## Troubleshooting
- **No Verified Sites Found**:
  - Check the script’s output under “All sites in Search Console” to see your site’s `siteUrl` and `permissionLevel`.
  - If the site has `siteRestrictedUser` or `siteUnverifiedUser`, upgrade to **Full** or **Owner** permissions in GSC.
  - If the site is a Domain property (e.g., `sc-domain:your-site.com`), ensure it’s verified.
  - Add a URL Prefix property (e.g., `https://your-site.com/`) if needed.
- **Authentication Error (403: access_denied)**:
  - Verify `name@gmail.com` is a test user in **OAuth consent screen** > **Test users**.
  - Ensure `credentials2.json` matches the Client ID (`xxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com`).
  - Delete `token.json` and rerun to force re-authentication.
- **Empty Search Analytics**:
  - Adjust the date range in the script (e.g., 90 days ago to today) to match your site’s data availability:
    ```python
    request = {
        "startDate": "2025-03-18",
        "endDate": "2025-08-17",
        "dimensions": ["date"]
    }
    ```
  - Check the **Performance** report in GSC to confirm data exists.
- **Browser Issues**:
  - Ensure `http://localhost` isn’t blocked by your firewall.
  - Try a different browser or clear cache.

## Notes
- The script uses `google-auth-oauthlib` for a modern, automated OAuth flow.
- Tokens are saved to `token.json` for reuse, skipping the browser popup on subsequent runs.
- To query specific metrics (e.g., by query or page), modify the `dimensions` in the script:
  ```python
  request = {
      "startDate": "2025-03-18",
      "endDate": "2025-08-17",
      "dimensions": ["query", "page"]
  }
  ```

For further assistance, contact the developer or check the [Google Search Console API documentation](https://developers.google.com/search/apis).