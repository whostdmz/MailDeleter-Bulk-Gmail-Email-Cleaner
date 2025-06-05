#!/usr/bin/env python3
# coding: utf-8

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# OAuth scopes for Gmail access
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
BATCH_SIZE = 500

def get_gmail_service():
    """Authenticate user and return Gmail service."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def delete_all(service):
    """Move all emails to trash."""
    try:
        response = service.users().messages().list(userId='me', maxResults=BATCH_SIZE).execute()
        messages = response.get('messages', [])
        if not messages:
            print("No emails to delete.")
            return
        print(f"{len(messages)} emails found. Deleting...")
        for msg in messages:
            service.users().messages().trash(userId='me', id=msg['id']).execute()
        print("All emails have been moved to trash.")
    except HttpError as error:
        print(f"API Error: {error}")

def delete_by_category(service):
    """Delete all emails in a specific Gmail category."""
    categories = {
        '1': 'primary',
        '2': 'social',
        '3': 'promotions',
        '4': 'updates',
        '5': 'forums'
    }
    print("Choose a category:")
    for key, value in categories.items():
        print(f"{key}: {value.capitalize()}")
    choice = input("Enter the number of the category: ").strip()
    category = categories.get(choice)
    if not category:
        print("Invalid choice.")
        return
    query = f"category:{category}"
    try:
        response = service.users().messages().list(userId='me', q=query, maxResults=BATCH_SIZE).execute()
        messages = response.get('messages', [])
        if not messages:
            print(f"No emails found in {category}.")
            return
        print(f"{len(messages)} emails found in {category}. Deleting...")
        for msg in messages:
            service.users().messages().trash(userId='me', id=msg['id']).execute()
        print(f"All emails in {category} have been moved to trash.")
    except HttpError as error:
        print(f"API Error: {error}")

def delete_by_sender(service):
    """Delete all emails from a specific sender."""
    sender = input("Enter the sender's email address to delete messages from: ").strip()
    if not sender:
        print("No email address entered.")
        return
    query = f"from:{sender}"
    try:
        response = service.users().messages().list(userId='me', q=query, maxResults=BATCH_SIZE).execute()
        messages = response.get('messages', [])
        if not messages:
            print("No emails found for this sender.")
            return
        print(f"{len(messages)} emails found. Deleting...")
        for msg in messages:
            service.users().messages().trash(userId='me', id=msg['id']).execute()
        print("Deletion complete.")
    except HttpError as error:
        print(f"API Error: {error}")

def empty_trash(service):
    """Permanently delete all emails in the trash."""
    try:
        print("Searching for emails in Trash...")
        response = service.users().messages().list(userId='me', labelIds=['TRASH'], maxResults=BATCH_SIZE).execute()
        messages = response.get('messages', [])
        if not messages:
            print("Trash is already empty.")
            return
        print(f"{len(messages)} emails found in Trash. Deleting permanently...")
        for msg in messages:
            service.users().messages().delete(userId='me', id=msg['id']).execute()
        print("Trash has been emptied.")
    except Exception as error:
        print(f"API Error: {error}")

def empty_spam(service):
    """Permanently delete all emails in the spam folder."""
    try:
        print("Searching for spam emails...")
        response = service.users().messages().list(userId='me', labelIds=['SPAM'], maxResults=BATCH_SIZE).execute()
        messages = response.get('messages', [])
        if not messages:
            print("No spam emails found.")
            return
        print(f"{len(messages)} spam emails found. Deleting permanently...")
        for msg in messages:
            service.users().messages().delete(userId='me', id=msg['id']).execute()
        print("All spam emails have been permanently deleted.")
    except HttpError as error:
        print(f"API Error: {error}")

def delete_by_filter(service):
    """Delete emails matching a custom Gmail search query."""
    filter_query = input("Enter your custom Gmail search query: ").strip()
    if not filter_query:
        print("No query entered.")
        return
    try:
        response = service.users().messages().list(userId='me', q=filter_query, maxResults=BATCH_SIZE).execute()
        messages = response.get('messages', [])
        if not messages:
            print("No emails found for this filter.")
            return
        print(f"{len(messages)} emails found. Deleting...")
        for msg in messages:
            service.users().messages().trash(userId='me', id=msg['id']).execute()
        print("All filtered emails have been moved to trash.")
    except HttpError as error:
        print(f"API Error: {error}")

def main_menu(service):
    """Display the main menu and handle user input."""
    while True:
        print("\nMailDeleter")
        print("1 - Delete All")
        print("2 - Delete Mail from Category")
        print("3 - Delete Mail from User")
        print("4 - Empty Trash")
        print("5 - Empty Spam")
        print("6 - Delete Mail from Filter")
        print("7 - Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            delete_all(service)
        elif choice == "2":
            delete_by_category(service)
        elif choice == "3":
            delete_by_sender(service)
        elif choice == "4":
            empty_trash(service)
        elif choice == "5":
            empty_spam(service)
        elif choice == "6":
            delete_by_filter(service)
        elif choice == "7":
            print("Exiting MailDeleter. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    service = get_gmail_service()
    main_menu(service)

