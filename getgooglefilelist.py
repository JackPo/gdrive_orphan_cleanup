from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

import os
import pickle
import time

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    """Authenticates the user with Google Drive and returns the service."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def delete_folder_contents(service, folder_id):
    """Deletes the contents of a given folder."""
    attempt = 0
    while attempt <= 5:
        try:
            print("Listing files in folder with id: ", folder_id)
            results = service.files().list(
                q="'{}' in parents".format(folder_id),
                pageSize=1000, fields="files(id, mimeType)").execute()

            items = results.get('files', [])
            if not items:
                print("No items found in the folder with id: ", folder_id)
                break
            
            for item in items:
                print("Found item with id: ", item['id'])
                try:  
                    if item['mimeType'] == 'application/vnd.google-apps.folder':
                        print("Item is a folder. Recursively deleting contents.")
                        delete_folder_contents(service, item['id'])
                    print("Deleting item with id: ", item['id'])
                    service.files().delete(fileId=item['id']).execute()
                    print("Deleted item with id: ", item['id'])
                    attempt = 0
                except HttpError as e: 
                    print('An HTTP error occurred while deleting file/folder:', e)
                    attempt += 1
                    if attempt <= 5:
                        time.sleep(2**attempt)
                    else:
                        print('Too many errors occurred while deleting file/folder. Moving on to the next file.')
                        break

        except HttpError as e:
            print('An HTTP error occurred while listing folder contents:', e)
            attempt += 1
            if attempt <= 5:
                time.sleep(2**attempt)
                continue
            else:
                print('Too many errors occurred while listing folder contents. Moving on to the next folder.')
                break


def get_orphan_files(service):
    """Get and remove orphan files in Google Drive."""
    page_token = None
    orphan_files = []
    attempt = 0
    total_files_processed = 0

    while True:  # Keep looping until no more orphan files/folders are found
        try:
            results = service.files().list(
                q="'me' in owners",
                pageSize=1000, fields="nextPageToken, files(id, name, parents, shared, mimeType)",
                pageToken=page_token).execute()

            items = results.get('files', [])

            if not items:
                print('No files found.')
                break
            else:
                for item in items:
                    total_files_processed += 1
                    # If the file has no parents and it's not shared, it is an orphan.
                    if not 'parents' in item and not item.get('shared', False):
                        orphan_files.append(item)
                        print('Orphan File/Folder Found:', u'{0} ({1})'.format(item['name'], item['id']))
                        if item['mimeType'] == 'application/vnd.google-apps.folder':
                            delete_folder_contents(service, item['id'])
                            print('Removing orphan folder:', u'{0} ({1})'.format(item['name'], item['id']))
                        else:
                            print('Removing orphan file:', u'{0} ({1})'.format(item['name'], item['id']))
                        service.files().delete(fileId=item['id']).execute()

                page_token = results.get('nextPageToken', None)
                # If the request succeeded, reset the attempt count.
                attempt = 0

                print(f'Processed {total_files_processed} files so far. Found {len(orphan_files)} orphan files.')

        except HttpError as e:
            print('An HTTP error occurred:', e)
            attempt += 1
            if attempt <= 5:
                # Implementing exponential backoff.
                time.sleep(2**attempt)
                continue
            else:
                print('Too many errors occurred. Exiting.')
                break

    print('Finished processing files. Total files processed:', total_files_processed)

def main():
    """Main function."""
    service = authenticate_google_drive()
    get_orphan_files(service)

if __name__ == '__main__':
    main()
