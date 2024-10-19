# GdriveReport

##### Retrieve Google OAuth API credential file
- Visit the [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Navigate to the OAuth Consent Screen tab, complete the necessary fields, save.
- In the Credentials tab, click on Create Credentials and select OAuth Client ID.
- Choose Desktop App as the application type and click Create.
- Use the download button to download your credentials.
- Move the file to the root directory of this project.
- Visit [Google API page](https://console.developers.google.com/apis/library)
- Search for "Google Drive API" and enable it if it is disabled

### Clone repo and run reports
- Clone the repo:
```git clone https://github.com/jordanbk/GdriveReport.git```
- Change directory to the root of the project:
```cd GdriveReport```
- Move credentials.json to cwd:
```mv /path/to/credentials.json .```
- Install dependencies and set up the project:
```
$ pip3 install -U pip
$ pip3 install -e .
```
- Run the program:
```$ gdrive_report```
