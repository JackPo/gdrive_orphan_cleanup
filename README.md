# Google Drive Orphaned Files Cleanup Script

This script is designed to identify and remove orphaned files in your Google Drive. An orphaned file or folder is one that isn't located in "My Drive" or any other folder. You can manually find these orphaned files by searching "is:unorganized owner:me" in the Google Drive search bar.

The script was co-written with the help of OpenAI's ChatGPT-4 and underwent significant manual tweaking and debugging.

## Prerequisites

Before running the script, you need to create a `credentials.json` file that allows the script to authenticate your Google Drive account. You also need to install the necessary Python libraries for Google APIs. Here are the detailed steps to do this:

### Creating a credentials.json file

1. Go to the Google API Console: [https://console.developers.google.com/](https://console.developers.google.com/)
2. From the project drop-down, select a project, or create a new one if you don't already have one.
3. In the sidebar on the left, select Library.
4. In the displayed library, search for "Google Drive" and select "Google Drive API".
5. On the Google Drive API page, click "ENABLE".
6. Once enabled, click "CREATE CREDENTIALS" at the top of the page.
7. It will prompt you with several questions. Here's how you should answer:
   - "Which API are you using?": Select "Google Drive API".
   - "Where will you be calling the API from?": Select "Other UI (e.g., Windows, CLI tool)".
   - "What data will you be accessing?": Select "User data".
8. Click "What credentials do I need?".
9. It will ask for a name and a "Product name shown to users". You can enter any name in both fields.
10. Click "Done".
11. You should now see a new OAuth 2.0 Client ID credential. To the right, there will be a download button. Click this button to download your credentials.
12. Rename the downloaded file to `credentials.json` and place it in the same directory as the script.

> **Note:** Ensure the `credentials.json` file's path matches the path specified in your Python script. Always keep your `credentials.json` file secure. Anyone who has access to this file can access your Google Drive.

### Installing necessary Python libraries

Ensure you have the necessary Python libraries for Google APIs installed. If not, you can install them using pip:

```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

# Running the script
With the credentials.json file in place and the necessary Python libraries installed, you're ready to run the script. It will authenticate with your Google Drive, search for any orphaned files, and proceed to remove them.

Please make sure to monitor the script's progress as it runs, especially if you have a large number of files in your Google Drive. The script outputs logging information that can help you track its progress and troubleshoot any potential issues.  
