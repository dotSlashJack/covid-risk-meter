# covid-alert
Code for frontend of covid-alert.org website
>#
This code is not yet fully functional and is NOT intended for public use.
>#

### Using with AWS Lambda:

1. Install pandas, numpy, matplotlib, and all of their dependencies in a local environment, we recommend inside of the "zip" folder.

2. Clean up files and zip the folder with your installations as well as lambda_function.py

3. Upload the zip to AWS Lambda (probably via an s3 bucket)

4. Configure an s3 bucket to store the relevant images

5. Configure an s3 bucket that triggers an event in the lambda function upon upload

6. Ensure this event updates the correct image (here, current.png) and public read access is granted

7. Access the URL of that updaged image stored on the s3 bucket

### Contact
colab[at]jackhester[dot]com or jsmith[at]tmrpa[dot]org
