// ==== Constants ====
const instructionsElem = document.getElementsByClassName('instructions')[0];
const videoElem = document.getElementsByClassName('input_video')[0];
const canvasElem = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElem.getContext('2d');

// ==== Global Variables ====
let s3; // gets set by initializeAWS()
let readyToCapture = false;
let captureMode = "snapshot"; // either "snapshot" or "video"
let isRightHanded = true;
let isOneHanded = true;
let mayCaptureData = false;
let saveNextFrame = false; // used in snapshot mode
let recordingVideo = false; // used in video mode
let landmarkList; // when recordingVideo is true, this is the list of landmarks for each frame
let recorder; // when recordingVideo is true, this is the recorder object
let doCapture = "notSet"; //either "notSet", "true" or "false"
let globalHandResults;
let globalImageAsBlob;
let globalLandmarkList;
let globalBlobEvent;
// ==== Functions ====




/*
 * This needs to be called before we begin. It initializes controls on the page.
 */
function initializeControls() {
    document.getElementById("snapshot").onclick = function(event) {
        captureMode = "snapshot";
    };
    document.getElementById("video").onclick = function() {
        captureMode = "video";
    }
    document.getElementById("right").onclick = function() {
        isRightHanded = true;
    };
    document.getElementById("left").onclick = function() {
        isRightHanded = false;
    }
    document.getElementById("one").onclick = function() {
        isOneHanded = true;
    };
    document.getElementById("two").onclick = function() {
        isOneHanded = false;
    }
}




/*
 * Call this function to make the UI temporarily something to the user
 * to indicate that a save was successful.
 */
// function showUserSaveHappened() {
//     savedElem.classList.add("showing");
//     setTimeout(function() {
//         savedElem.classList.remove("showing");
//     }, 1000)
// }


/*
 * Function called after a single frame has been taken.
 */
function saveSingleFrame(handResults, imageAsBlob) {
    // --- Write the landmarks ---
    const dataAsAString = JSON.stringify(handResults.multiHandLandmarks)
    //fetch API here
    const url = "https://ywpaxgg1if.execute-api.us-east-1.amazonaws.com/prod/find-picture";
    const fetchSettings = {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json"
        },
        body: dataAsAString
    };
    fetch(url, fetchSettings)
        .then(function(response){
            response.json()
                .then(function(json){
                    displayFindResult(json, "picture");
                });
        })
        .catch(function(err) {
            console.log("Error fetching", err);
        });


    // const uploadInstructionsForLandmark = {
    //     Bucket: 'asl-dictionary-uploads',
    //     Key: `uploads/${randomId}/landmarks.json`,
    //     ContentType: "application/json", //subtly important
    //     Body: dataAsAString
    // };
    // s3.upload(uploadInstructionsForLandmark, function(err) {
    //     if (err) {
    //         throw err;
    //     }
    //     console.log("finished saving landmark");
    // });
}




/*
 * Function called after a single frame has been taken.
 */
function saveVideo(landmarkList, videoAsBlob) {
    // --- Write the landmarks ---
    const dataAsAString = JSON.stringify(landmarkList);
    //fetch API here
    let url;
    if (isOneHanded) {
        url = "https://ywpaxgg1if.execute-api.us-east-1.amazonaws.com/prod/find-video1";
    } else {
        url = "https://ywpaxgg1if.execute-api.us-east-1.amazonaws.com/prod/find-video2";
    }
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
                    if (json.errorMessage === null || json.errorMessage === undefined){
                        displayFindResult(json, "video");
                    } else {
                        console.log("error message is ");
                        console.log(json.errorMessage);
                        const errorElem = document.getElementById("error");
                        errorElem.classList.remove("hidden");
                        console.log("error, not enough data");
                    };
                });
        })
        .catch(function (err) {
            console.log("Error fetching", err);
        });
}

function saveFrameForFindOrCollect(handResults, imageAsBlob) {
        saveSingleFrame(handResults, imageAsBlob);
}


function saveVideoForFindOrCollect(landmarkList, blobEventData) {
    saveVideo(landmarkList, blobEventData);
}


function displayFindResult(json, pictureOrVideo) {
    console.log("I think the answer is: ", json.bestGuess);
    const guessElem = document.getElementById("guess");
    guessElem.innerText = json.bestGuess;
    const guessBlockElem = document.getElementById("guessBlock");
    guessBlockElem.classList.remove("hidden");
    console.log("removed hidden");
    // const url = 'word.html?word='+encodeURIComponent(json.bestGuess)+'&pictureOrVideo=' + pictureOrVideo;
    // // window.location.href = url;
    // window.open(url);
}



// ==== MAIN FUNCTION ====
initializeAWS()
initializeControls()
startRunningCamera()
