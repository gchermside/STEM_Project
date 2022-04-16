const queryString = window.location.search;
const params = new URLSearchParams(queryString);
const word= params.get("word");
const pictureOrVideo= params.get("pictureOrVideo");
document.getElementById("wordSpan").textContent=word;
const backButtonElem = document.getElementById("backButton");
backButtonElem.addEventListener("click", backToFind);

function backToFind() {
    console.log("closing window now");
    window.close();
}

console.log(word);
console.log(pictureOrVideo);

path = "uploads/2022-03-06T23_43_43.583Z-6802499/picture.jpeg";
findPicture(path);

function findPicture(path) {
    // --- Write the landmarks ---
    const dataAsAString = JSON.stringify(path)
    //fetch API here
    const url = "https://ywpaxgg1if.execute-api.us-east-1.amazonaws.com/prod/findfile";
    const fetchSettings = {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json"
        },
        body: dataAsAString
    };
    fetch(url, fetchSettings)
        .then(function (response) {
            response.json()
                .then(function (json) {
                    console.log(json);
                });
        })
        .catch(function (err) {
            console.log("Error fetching", err);
        });
}

// const s3 = new AWS.S3({
//     accessKeyId: passwords.AWSAccessKeyId,
// secretAccessKey: passwords.AWSSecretKey,
// Bucket: "asl-dictionary-uploads"
// });
//
// const parameters = {
//     Bucket: "asl-dictionary-uploads",
//     Key: "2022-03-06T23_43_43.583Z-6802499/picture.jpeg"
// };
//
// const output = s3download(parameters);
// console.log(output);
//
// const s3download = function (params) {
//     return new Promise((resolve, reject) => {
//         s3.createBucket({
//             Bucket: "asl-dictionary-uploads"        /* Put your bucket name */
//         }, function () {
//             s3.getObject(params, function (err, data) {
//                 if (err) {
//                     console.log("there was an error", err);
//                     reject(err);
//                 } else {
//                     console.log("Successfully downloaded data from  bucket");
//                     resolve(data);
//                 }
//             });
//         });
//     });
// }