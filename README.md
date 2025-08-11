


🔧 Step-by-step in Google Cloud Console:
- Go to Google Cloud Console
- Create or Select Project
- Search, Find then enable `Search Console API`
- In the left menu, go to: IAM & Admin → Service Accounts

- Click “+ CREATE SERVICE ACCOUNT”

Fill in:

- Name: search-console-access
- Description: (optional)
- Click Create and Continue
- Role assignment `Owner`
- Click Continue → Done

🎯 Now create and download the credentials:
- In the `Service Accounts` see existing email list example `search-console-access@...com`
- Click the 3-dot menu → Manage Keys
- -> search-console-access
- Under “Keys”, click “Add Key” → “Create new key”

Choose:
- Key type: JSON
- Click Create — it will download the correct credentials.json

🧠 Add this account to Google Search Console
- Open: https://search.google.com/search-console
- Choose your property
- Go to Settings → Users & permissions
- Click “Add User”
- Paste the client_email from your new JSON (e.g., search-console@your-project-id.iam.gserviceaccount.com)
- Set permission to Full User

Install Library
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas
```

