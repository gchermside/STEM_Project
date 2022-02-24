// ==== Constants ====
const instructionsElem = document.getElementsByClassName('instructions')[0];
const savedElem = document.getElementsByClassName('saving')[0];
const videoElem = document.getElementsByClassName('input_video')[0];
const canvasElem = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElem.getContext('2d');


// ==== Global Variables ====
let s3; // gets set by initializeAWS()
let readyToCapture = false;
let saveNextFrame = false;


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
 * Function called when the user presses a key (while the browser is in the forefront).
 *
 * What it does is to use the space bar for recording.
 *
 * @param event the system event that was generated
 */
function onKeypress(event) {
    if (event.code === 'Space') {
        saveNextFrame = true;
        event.preventDefault(); // don't actually type a space.
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
    const dataAsAString = JSON.stringify(handResults.multiHandLandmarks);
    const uploadInstructionsForLandmark = {
        Bucket: 'test-bucket-for-file-upload',
        Key: `uploads/${randomId}/landmarks.json`,
        ContentType: "application/json",
        Body: dataAsAString
    };
    s3.upload(uploadInstructionsForLandmark, function(err) {
        if (err) {
            throw err;
        }
        console.log("finished saving landmark");
    });

    // --- Write the image ---
    console.log("about to save image");
    const uploadInstructionsForImage = {
        Bucket: 'test-bucket-for-file-upload',
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

/*
 * This function returns a random number from 1 through 10 million.
 */
function getRandomId() {
    return Math.ceil(Math.random() * 10000000);
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
        saveSingleFrame(handResults, imageAsBlob);
    }
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
}


// ==== MAIN FUNCTION ====
initializeAWS()
startRunningCamera()
