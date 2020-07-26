/* script.js for covid-alert.org
@author Jack Hester
*/

function expandDiv(divID) {
    var x = document.getElementById(divID);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

AWS.config.region = 'us-west-2'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({ 
    IdentityPoolId: 'us-west-2:cafaba88-27e2-4c26-a632-a8a151dab798',
});
var s3 = new AWS.S3({
    apiVersion: "2006-03-01",
    params: { Bucket: 'covid-alert-table-upload' }
});


var bucketName = 'covid-alert-table-upload';
var bucketRegion = 'us-west-2';
var IdentityPoolId = 'us-west-2:cafaba88-27e2-4c26-a632-a8a151dab798';

    

function uploadFile(folderName) {
    var files = document.getElementById("tableUpload").files;
    if (!files.length) {
        return alert("Please choose a file to upload first.");
    }
    var file = files[0];
    var fileName = file.name;
    var folderKey = encodeURIComponent(folderName) + "/";

    var fileKey = folderKey + fileName;

    // Use S3 ManagedUpload class as it supports multipart uploads
    var upload = new AWS.S3.ManagedUpload({
        params: {
            Bucket: bucketName,
            Key: fileKey,
            Body: file,
            ACL: "public-read" //TODO: see if I can revoke this later
        }
    });

    var promise = upload.promise();

    promise.then(
        function (data) {
            console.log("Successfully uploaded file.");
            alert("Your new table finished uploading");
            //viewAlbum(folderName);
        },
        function (err) {
            return alert("There was an error uploading the file: ", err.message);
        }
    );
}

function deleteFile(folderName) {
    var files = document.getElementById("tableUpload").files;
    var file = files[0];
    var fileName = file.name;
    var folderKey = encodeURIComponent(folderName) + "/";
    var fileKey = folderKey + fileName;
    var bucketInstance = new AWS.S3();
    var params = {
        Bucket: bucketName,
        Key: fileKey
    };

    s3.deleteObject(params, function (err, data) {
        if (data) {
            console.log("File deleted successfully");
        }
        else {
            alert("Error deleting the old table: " + err);
        }
    });
}

/*
@param folderName the name of the folder inside the s3 bucket that contains the table
*/
function updateTable(folderName){
    deleteFile(folderName);
    uploadFile(folderName);
}
