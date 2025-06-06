# MailDeleter-Bulk-Gmail-Email-Cleaner
MailDeleter is a Python command-line tool that allows you to quickly and safely clean up your Gmail inbox. It uses the official Gmail API and OAuth2 authentication to provide several powerful deletion options through a simple interactive menu.

Requirements:

    Python 3.7+

    A Google Cloud project with Gmail API enabled

    credentials.json file from your Google Cloud Console : https://console.cloud.google.com/



USAGES:

    -Clone the repository and place your credentials.json in the project folder.
    
    -Install dependencies:
        pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    
    -Run the script:
    
        python3 script.py
    
    -Follow the interactive menu to select the desired deletion operation.

!!WARNING!!:

This tool performs real deletions on your Gmail account. Always test on a small set of emails first and use with caution.
