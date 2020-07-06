/* script.js for covid-alert.org
@author Jack Hester
*/

function expandDiv(divID){
    var x = document.getElementById(divID);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}