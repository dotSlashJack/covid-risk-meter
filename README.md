# covid-alert
Code for covid-alert.org, developed for the City of Reno Public Health Emergency Advisory Board
>#
This code is not yet fully implemented and is NOT intended for public use.
>#

### Using with AWS Lambda:

The lambda function and supporing code are located inside of the "zip" directory

1. Install pandas, numpy, matplotlib, datetime, and all of their dependencies in a local environment, we recommend inside of the "zip" folder.

2. Clean up files and zip the folder with your installations as well as lambda.py and threatMeter.py

3. Upload the zip to AWS Lambda (probably onto an s3 bucket)

4. Configure an s3 bucket to store the relevant images and update code accordingly

5. Configure an s3 bucket that triggers an event in the lambda function upon upload (where you'll put the excel file)

6. Ensure this event updates the correct image (here, current.png) and public read access is granted

7. Access the URL of that updated image stored on the s3 bucket

### Other files

There are a few other files on here that we have used to grab some of the data and work towards a frontend website (e.g., dhss_covid_scraper.py). You are welcome to take a look at those, but they are probably not very useful to you. Some reorgainization and cleanup of this repo are in order in the near future.

### Contact
colab[at]jackhester[dot]com or jsmith[at]tmrpa[dot]org
