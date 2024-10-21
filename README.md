# GdriveReport

##### Retrieve Google OAuth API credential file
- Visit the [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Navigate to the OAuth Consent Screen tab, complete the necessary fields, save.
- In the Credentials tab, click on Create Credentials and select OAuth Client ID.
- Choose Desktop App as the application type and click Create.
- Use the download button to download your client secret.
- Visit [Google API page](https://console.developers.google.com/apis/library)
- Search for "Google Drive API" and enable it if it is disabled

#### Clone Repo and Run Reports
- Clone the repo:
```git clone https://github.com/jordanbk/GdriveReport.git```
- Change directory to the root of the project:
```cd GdriveReport```
- Move the client_secret_*.json file (Downloaded from the Google Cloud Console) to the current directory and rename it credentials.json:
```mv /path/to/client_secret_*.json credentials.json```
- Install dependencies and set up the project:
```
pip3 install -U pip
pip3 install .
```
- Run the program:
```python3 main.py```

- Follow the prompts displayed by the program.