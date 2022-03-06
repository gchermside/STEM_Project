// ==== Constants ====
const instructionsElem = document.getElementsByClassName('instructions')[0];
const savedElem = document.getElementsByClassName('saving')[0];
const videoElem = document.getElementsByClassName('input_video')[0];
const userNameElem = document.getElementById("name");
const signNameElem = document.getElementById("sign");
const canvasElem = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElem.getContext('2d');
let userName = ""
let signName = ""

// ==== Global Variables ====
let s3; // gets set by initializeAWS()
let readyToCapture = false;
let captureMode = "snapshot"; // either "snapshot" or "video"
let isRightHanded = true;
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
 * This needs to be called before we begin, it initializes access to AWS for
 * writing files and sets the "s3" global variable.
 */
function initializeAWS() {
    AWS.config.update({region: "us-east-1"});
    AWS.config.credentials = new AWS.CognitoIdentityCredentials(
        {IdentityPoolId: passwords.identityPoolId}
    );
    s3 = new AWS.S3();
}



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
    userNameElem.value = "";
    signNameElem.value = "";
}


/*
 * Function called when the user presses a key (while the browser is in the forefront).
 *
 * What it does is to use the space bar for recording.
 *
 * @param event the system event that was generated
 */
function onKeypress(event) {
    if (readyToCapture && captureMode === "snapshot" && event.code === 'Space') {
        saveNextFrame = true;
        event.preventDefault(); // don't actually type a space.
    }
    if (recordingVideo && event.code === 'Space') {
        // while recording video, don't let holding down the space cause problems
        event.preventDefault(); // don't react as if a space was typed.
    }
}


/*
 * Function that is called when a key goes down. Used to watch for the space
 * key going down to begin recording video.
 */
function onKeydown(event) {
    if (readyToCapture && captureMode === "video" && !recordingVideo && event.code === 'Space') {
        landmarkList = [];
        recorder = new MediaRecorder(canvasElem.captureStream());
        recorder.ondataavailable = onVideoDataAvailable;
        recorder.start();
        recordingVideo = true;
        event.preventDefault(); // don't actually process it as a space being typed.
    }
}


/*
 * Function that is called when a key goes down. Used to watch for the space
 * key going down to begin recording video.
 */
function onKeyup(event) {
    if (recordingVideo && event.code === 'Space') {
        recordingVideo = false;
        recorder.stop();
        event.preventDefault(); // don't actually process it as a space being typed.
    }
}


/*
 * Call this to indicate whether the video is ready to be captured.
 *
 * @param isReady a boolean; true if ready and false if not.
 */
function setReadyToCapture(isReady) {
    if (isReady !== readyToCapture) {
        readyToCapture = isReady;
        if (readyToCapture) {
            instructionsElem.classList.remove("notReady");
        } else {
            instructionsElem.classList.add("notReady");
        }
    }
}


/*
 * Call this function to make the UI temporarily something to the user
 * to indicate that a save was successful.
 */
function showUserSaveHappened() {
    savedElem.classList.add("showing");
    setTimeout(function() {
        savedElem.classList.remove("showing");
    }, 1000)
}


/*
 * Function called after a single frame has been taken.
 */
function saveSingleFrame(handResults, imageAsBlob) {
    // --- Select a random ID to use ---
    const randomId = getRandomId();
    console.log(`saving to id ${randomId}`);

    // --- Write the landmarks ---
    const dataAsAString = JSON.stringify(handResults.multiHandLandmarks)
    const uploadInstructionsForLandmark = {
        Bucket: 'asl-dictionary-uploads',
        Key: `uploads/${randomId}/landmarks.json`,
        ContentType: "application/json", //subtly important
        Body: dataAsAString
    };
    s3.upload(uploadInstructionsForLandmark, function(err) {
        if (err) {
            throw err;
        }
        console.log("finished saving landmark");
    });

    // --- Write the info ---
    userName = document.getElementById("name").value
    signName = document.getElementById("sign").value
    const jsonInfo = JSON.stringify({isRightHanded: isRightHanded, userName: userName, signName: signName})
    const uploadInstructionsForInfo = {
        Bucket: 'asl-dictionary-uploads',
        Key: `uploads/${randomId}/info.json`,
        ContentType: "application/json", //subtly important
        Body: jsonInfo
    };
    s3.upload(uploadInstructionsForInfo, function(err) {
        if (err) {
            throw err;
        }
        console.log("finished saving info");
    });

    // --- Write the image ---
    console.log("about to save image");
    const uploadInstructionsForImage = {
        Bucket: 'asl-dictionary-uploads',
        Key: `uploads/${randomId}/image.jpeg`,
        ContentType: "image/jpeg",
        Body: imageAsBlob
    };
    s3.upload(uploadInstructionsForImage, function(err) {
        if (err) {
            throw err;
        }
        console.log("finished saving image");
    });

    // --- Perform animation ---
    // NOTE: the save hasn't happened yet, it is still going on. So we're lying to the user.
    showUserSaveHappened();
}


/*
 * This function returns the canvas image as a blob. It's rather
 * complicated and it's not supposed to very obvious how it works.
 */
function canvasAsBlob(canvasElem) {
    const imageAsURL = canvasElem.toDataURL();
    const binary = atob(imageAsURL.split(',')[1]);
    const array = [];
    for(let i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
}


function onVideoDataAvailable(blobEvent) {
    const sureButtonsElem = document.getElementById("sureButtons")
    sureButtonsElem.classList.remove("hidden")
    globalLandmarkList = landmarkList;
    globalBlobEvent = blobEvent.data;
    landmarkList = null; // we saved it, so we don't need this data anymore
    recorder = null; // we saved it, so we don't need this data anymore
}


/*
 * Function called after a single frame has been taken.
 */
function saveVideo(landmarkList, videoAsBlob) {
    // --- Select a random ID to use ---
    const randomId = getRandomId();
    console.log(`saving to id ${randomId}`);

    // --- Write the landmarkList ---
    const dataAsAString = JSON.stringify(landmarkList);
    const uploadInstructionsForLandmarkList = {
        Bucket: 'asl-dictionary-uploads',
        Key: `uploads/${randomId}/landmarks.json`,
        ContentType: "application/json",
        Body: dataAsAString
    };
    s3.upload(uploadInstructionsForLandmarkList, function(err) {
        if (err) {
            throw err;
        }
        console.log("finished saving landmark");
    });

    // --- Write the info ---
    userName = document.getElementById("name").value
    signName = document.getElementById("sign").value
    const jsonInfo = JSON.stringify({isRightHanded: isRightHanded, userName: userName, signName: signName})
    const uploadInstructionsForInfo = {
        Bucket: 'asl-dictionary-uploads',
        Key: `uploads/${randomId}/info.json`,
        ContentType: "application/json", //subtly important
        Body: jsonInfo
    };
    s3.upload(uploadInstructionsForInfo, function(err) {
        if (err) {
            throw err;
        }
        console.log("finished saving info");
    });

    // --- Write the video ---
    console.log("about to save video");
    const uploadInstructionsForVideo = {
        Bucket: 'asl-dictionary-uploads',
        Key: `uploads/${randomId}/video.webm`,
        ContentType: "video/webm",
        Body: videoAsBlob
    };
    s3.upload(uploadInstructionsForVideo, function(err) {
        if (err) {
            throw err;
        }
        console.log("finished saving video");
    });

    // --- Perform animation ---
    // NOTE: the save hasn't happened yet, it is still going on. So we're lying to the user.
    showUserSaveHappened();
}


/*
 * This function returns a random number from 1 through 10 million.
 */
function getRandomId() {
    const d = new Date();
    const date = d.toISOString() //date is in UK time(hours will seem wrong but the rest is great)
    return date +"-"+Math.ceil(Math.random() * 10000000);
}


function onHandsResults(handResults) {
    // --- Draw the image onto the canvas ---
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElem.width, canvasElem.height);
    canvasCtx.drawImage(handResults.image, 0, 0, canvasElem.width, canvasElem.height);

    // --- If we plan to save it, capture the image before we draw landmarks ---
    let imageAsBlob;
    if (saveNextFrame) {
        // Since we're going to save it, we'd better grab a copy before drawing on it.
        imageAsBlob = canvasAsBlob(canvasElem);
    }

    // --- If we have landmarks, draw them on the canvas ---
    if (handResults.multiHandLandmarks && handResults.multiHandLandmarks.length > 0) {
        for (const landmarks of handResults.multiHandLandmarks) {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 5});
            drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2});
        }
        setReadyToCapture(true);
    } else {
        setReadyToCapture(false)
    }
    canvasCtx.restore();

    // --- If we need to, go ahead and save the data ---
    if (saveNextFrame) {
        saveNextFrame = false;
        const sureButtonsElem = document.getElementById("sureButtons")
        sureButtonsElem.classList.remove("hidden")
        console.log("going to waitFOrBottuns")
        globalHandResults = handResults;
        globalImageAsBlob = imageAsBlob;
    }
    if (recordingVideo) {
        landmarkList.push(handResults.multiHandLandmarks);
    }
}

function startCapture() {
    console.log("clicked yes")
    doCapture = "true";
    const sureButtonsElem = document.getElementById("sureButtons");
    sureButtonsElem.classList.add("hidden");
    // Want to do this:
    if(captureMode === "snapshot") {
        saveSingleFrame(globalHandResults, globalImageAsBlob);
    }
    if(captureMode === "video") {
        saveVideo(globalLandmarkList, globalBlobEvent);
    }
}

function noCapture() {
    console.log("clicked no")
    doCapture = "false";
    const sureButtonsElem = document.getElementById("sureButtons")
    sureButtonsElem.classList.add("hidden")
}


function startRunningCamera() {
    // --- Start Hands running ---
    const hands = new Hands({locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
    }});
    hands.setOptions({
        maxNumHands: 2,
        modelComplexity: 1,
        minDetectionConfidence: 0.7,
        minTrackingConfidence: 0.5
    });
    hands.onResults(onHandsResults);

    // --- Start the camera ---
    const camera = new Camera(videoElem, {
        onFrame: async () => {
            await hands.send({image: videoElem});
        },
        width: 1280,
        height: 720,
    });
    camera.start();

    // --- Begin listening for space key ---
    document.addEventListener('keypress', onKeypress);
    document.addEventListener("keydown", onKeydown);
    document.addEventListener("keyup", onKeyup);
}


// ==== MAIN FUNCTION ====
initializeAWS()
initializeControls()
startRunningCamera()
