import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

""" 
This class is defined to send and search mails within a Gmail account.

Author: Nisha Sharma
Date: March 4, 2023

Public Methods:
* get_credentials(): Checks if the credentials are present and valid, if not credentials are fetched again.
* retrieve_credentials(): Retrieves the credentials based on scope and credentials' file path after successful authorization.
* send_email(subject, body, to, creds): Sends an email to the specified recipient.
* search_mail(queryMessage, creds): Searchs all messages based on the query phrase.

Instance variables:
* credentials: an instance of "google_auth_oauthlib.flow.InstalledAppFlow" class,
             that represent the credentials obtained after successful authorization.
* scope: a list of strings that specify the scope the authorization for the credentials.
* credentials_path: a string that contains the location of the file with authorization information

Dependencies:
* googleapiclient
* google_auth_oauthlib
* email

Limitations:
* send_mail() function is not defined to send any attachments.
* search_mail() function is not defined to search for phrases inside attachments.
"""


class gmailCredentials:
    # This is the default constructor of the class
    def __init__(self, cred_path, scope):
        self.credentials_path = cred_path
        self.scope = scope
        self.credentials = None

    # This function is defined to get the stored credentials or retrieve if not present.
    def get_credentials(self):
        if not self.credentials or not self.credentials.valid:
            self.retrieve_credentials()
        return self.credentials

    # This function is defined to retrieve the credentials after authorization
    def retrieve_credentials(self):
        try:
            creds = None
            # Set the desired OAuth scopes.
            SCOPES = self.scope

            # Create the OAuth flow for the installed application.
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, scopes=SCOPES)

            # Authorize the application and get the user's credentials.
            creds = flow.run_local_server(port=0)

        except Exception as error:
            print(F'An error occurred: {error}')
            creds = None
        self.credentials = creds

    # This function is defined to send an email to the desired recipient.
    def send_email(subject, body, to, creds):
        try:
            # Create the message
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            # Encode the message in base64
            message_bytes = message.as_bytes()
            message_b64 = base64.urlsafe_b64encode(message_bytes).decode('utf-8')

            # Call the Gmail API to send the message
            service = build('gmail', 'v1', credentials=creds)
            message = service.users().messages().send(userId='me', body={'raw': message_b64}).execute()
            print(F'Successfully sent message to {to}. Message Id: {message["id"]}')
        except Exception as error:
            print(F'An error occurred: {error}')
            message = None
        return message

    # This function searchs for the mails for a given query phrase.
    def search_mail(queryMessage, creds):

        # Create a Gmail API client.
        service = build('gmail', 'v1', credentials=creds)

        # Define the search query.
        query = queryMessage

        # Search for messages that match the query.
        results = service.users().messages().list(
            userId='me',
            q=query
        ).execute()

        # Print the message IDs of the matching messages.
        if 'messages' in results:
            for message in results['messages']:
                print(message['id'])
        else:
            print('No messages found.')


# Call the get_credentials() to initialise the credentials
creds = gmailCredentials('client_secret.json', ['https://www.googleapis.com/auth/gmail.readonly', \
                                                'https://www.googleapis.com/auth/gmail.send']).get_credentials()

# Call the send_email to send an email
gmailCredentials.send_email('Test Email', 'This is a test email sent via the Gmail API.', 'apitestapi59@gmail.com',
                            creds)

# Call the search_email to look for the email
gmailCredentials.search_mail('Gmail API', creds)
