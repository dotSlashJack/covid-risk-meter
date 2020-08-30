# covid-alert
Code for tmrpa.org/covid-wc, developed for the City of Reno Public Health Emergency Advisory Board

### Using with AWS Lambda:

The lambda function and supporing code are located inside of the "zip" directory

1. Install pandas, numpy, matplotlib, datetime, and all of their dependencies in a local environment, we recommend inside of the "zip" folder.

2. Clean up files and zip the folder with your installations as well as lambda.py and threatMeter.py

3. Upload the zip to AWS Lambda (probably via an s3 bucket)

4. Configure an s3 bucket to store the relevant images and update code accordingly

5. Configure an s3 bucket that triggers an event in the lambda function upon upload (where you'll put the excel file)

6. Ensure this event updates the correct image (here, current.png) and public read access is granted

7. Access the URL of that updated image stored on the s3 bucket

### Other files

There are a few other files on here in the "misc" folder that we have used to grab some of the data and work towards a frontend website (e.g., dhss_covid_scraper.py). You are welcome to take a look at those, but they are probably not very useful to you. We also have an admin upload page that we use to upload the new excel file each day (and automatically update the metric from there); feel free to contact us if you would like information on how to set up your own admin page or would like a copy of our code for that portion of the project. These files will likely be removed from the main repository by September 4, 2020. We will likely maintain a copy on the active dev branch.

### Contact

colab[at]jackhester[dot]com or jsmith[at]tmrpa[dot]org

&#x1F534;
>#
>This code is still under development and is NOT intended for public use. We provide no warranty or guarantee that our code works or will be useful or accurate.
>#
&#x1F534;
