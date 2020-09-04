# covid-alert

Code for https://tmrpa.org/covid-wc, developed for the City of Reno Public Health Emergency Advisory Board

### File structure

##### The core code can be found under the ``zip'' folder.

ThreatCalculator: contains a class with methods to calculate useful summary statistics

Plotter: contains a class to create plots and charts of data list

plot: implementations of Plotter using COVID data list

calculate: implements ThreatCalculator to calculate results

lambda: communicate with AWS s3 buckets to update the threat meter, recommendations, and other supporting data

### Using with AWS Lambda:

The lambda function and supporting code are located inside of the "zip" directory

1. Install pandas, numpy, matplotlib, datetime, and all of their dependencies in a local environment, we recommend inside of the "zip" folder.

2. Clean up files and zip the folder with your installations as well as lambda.py, calculate.py, ThreatCalculator.py, and plot and Plotter.py if you wish to create plots (these two files are still under developed)

3. Upload the zip to AWS Lambda (probably via an s3 bucket)

4. Configure an s3 bucket to store the relevant images and update code accordingly

5. Configure an s3 bucket that triggers an event in the lambda function upon upload (where you'll put the excel file)

6. Ensure this event updates the correct image (here, current.png) and public read access is granted

7. Access the URL of that updated image stored on the s3 bucket

### Contact

There is a contact for at the bottom of the website, tmrpa.org/covid-wc, that you can use to ask questions or submit recommendations.

### Additional notes

We are making this code open source to help stakeholders and researchers understand our metrics and perform their own calculations. Please note that we do not provide any guarantees about the code or its performance. Please note that some of the code is only partially implemented at this time  (such as Plotter).
