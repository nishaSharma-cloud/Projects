# Gmail API: 
  * This project send a mail using gmail api and search for mail based on the search query.
  * Send mail to the specified recipient based on following argument:
    * subject
    * body 
    * to
    * creds
  * Mail searchs all messages based on the query phrase with the help of following argument:
    * queryMessage
    * creds

# Technology Stack:
  * base64
  * MIMEText from email.mime.text
  * build from googleapiclient.discovery
  * InstalledAppFlow from google_auth_oauthlib.flow

# Dependencies:
  * <a name="section-1"></a> Google console account [https://cloud.google.com/](#section-1) 
  * GMAIL API enabled for that account
  * OAuth credentials available for desktop app
