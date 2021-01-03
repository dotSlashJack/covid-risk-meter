# Covid Risk Meter Code

Support and backend code for covidriskmeter.org, developed for the City of Reno Public Health Emergency Advisory Board

&#x1F534;
>#
>**WARNING:** The most recent upload is an intermediate step as we prepare for the next generation of the tool. The GUI and predictive tool are NOT the finished versions! Please also note: the AWS supporting files will be REMOVED in the next version, as we are removing explicit support for this functionality in future versions. Plotting functions have been nearly universally disabled in this version, as the current GUI has not added support for the plotting functions yet. Our new version will be released no later than January 15th.
>#
&#x1F534;

### File structure

##### The core code can be found under the "zip" folder.

local_run: allows you to run the meter locally (if you don't want to run with AWS). Rcommended to delete this from "zip" if you upload to AWS. Usage: python local_run.py --x &lt;path/to/excel.xlsx> -m &lt;meter> or &lt;state> for state calculator.

ThreatCalculator: contains a class with methods to calculate useful summary statistics

Plotter: contains a class to create plots and charts of data list

plot: implementations of Plotter using COVID data list

calculate: implements ThreatCalculator to calculate results

lambda: communicate with AWS s3 buckets to update the threat meter, recommendations, and other supporting data

calc_utils: assorted utility functions for generating the overall score and color, any other misc. utility functions

### Expected data table structure

This code is designed to work when provided an excel file. You can, however, use a different format as long as it's brought into a pandas data frame (see lambda.py and calculate.py to see how we handle this). Each value or set of values we use in a calculation is in its own column.

You can also provide your own column names to perform calculations on (so long as you provide the name when instantiating the ThreatCalculator class), as we do in calculate.py. You can see the column names we use in that file, and each instantiation of the ThreatMeter class is commented so you can understand how we performed each calculation.

### Running locally:

Option 1, command line:

1. Navigate to the "zip" folder inside of the main folder

2. Run: python local_run.py --x &lt;path/to/excel.xlsx> -m &lt;meter> for the main meter, &lt;state> for state calculator, or &lt;predict> for the predictive tool. If you only run with the excel argument, the tool will run the main meter calculations ONLY by default

Option 2, GUI:

1. Navigate to the "zip" folder inside of the main folder

2. Run: python local_run.py

3. Choose your excel file with the button with the "Select Excel File"

4. Check the boxes method(s) you would like to run

5. Click RUN

6. Your results will be printed in the console/terminal where you ran the file from. Outputs will later be provided in file format as well.

### Using with AWS Lambda:

The lambda function and supporting code are located inside of the "zip" directory

1. Install pandas, numpy, matplotlib, datetime, and all of their dependencies in a local environment, we recommend inside of the "zip" folder.

2. Clean up files and zip the folder with your installations as well as lambda.py, calculate.py, ThreatCalculator.py, calc_utils.py, and plot and Plotter.py if you wish to create plots (these two files are still under developed)

3. Upload the zip to AWS Lambda (probably via an s3 bucket)

4. Configure an s3 bucket to store the relevant images and update code accordingly

5. Configure an s3 bucket that triggers an event in the lambda function upon upload (where you'll put the excel file)

6. Ensure this event updates the correct image (here, current.png) and public read access is granted

7. Access the URL of that updated image stored on the s3 bucket

### Changelog

v 1.2
- Added GUI support for users who do not want to use command line arguments
- Predictive tool framework added, but it is NOT the most recent version

v 1.1
- The calculation for the risk assessments was updated and uses a mean in stead of slopes and cutoffs were changed accordingly
- A new file was added to allow users to run the code locally

### Contact

There is a contact for at the bottom of the website, covidriskmeter.org, that you can use to ask questions or submit recommendations. You can also reach out to <a href="https://jackhester.com/contact.html">Jack Hester</a>, the main creator of this code.

### Additional notes

We are making this code open source to help stakeholders and researchers understand our metrics and perform their own calculations. Please note that we do not provide any guarantees about the code or its performance. Please note that some of the code is only partially implemented at this time (such as Plotter).
