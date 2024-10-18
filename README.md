# GdriveReport

##### Retrieve Google OAuth API credential file
- Visit the [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Navigate to the OAuth Consent Screen tab, complete the necessary fields, save.
- In the Credentials tab, click on Create Credentials and select OAuth Client ID.
- Choose Desktop App as the application type and click Create.
- Use the download button to download your credentials.
- Move the file to the root directory of this project.
- Visit [Google API page](https://console.developers.google.com/apis/library)
- Search for Drive and enable it if it is disabled
- Run the following commands:

```sh
$ pip3 install -U pip
$ pip3 install -U -r requirements.txt
$ python3 nf_gdrive/gdrive/src/assessment_1.py
$ python3 nf_gdrive/gdrive/src/assessment_2.py
$ python3 nf_gdrive/gdrive/src/assessment_3.py
```