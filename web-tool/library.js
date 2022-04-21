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
    const guessBlockElem = document.getElementById("guessBlock");
    if(guessBlockElem !== null) {
        guessBlockElem.classList.add("hidden");
    }
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
    const guessBlockElem = document.getElementById("guessBlock");
    if(guessBlockElem !== null) {
        guessBlockElem.classList.add("hidden");
    }
    if (readyToCapture && captureMode === "video" && !recordingVideo && event.code === 'Space') {
        landmarkList = [];
        recorder = new MediaRecorder(canvasElem.captureStream());
        recorder.ondataavailable = onVideoDataAvailable;
        recorder.start();
        recordingVideo = true;
        console.log("about to not scroll down");
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
    saveVideoForFindOrCollect(landmarkList, blobEvent.data)
    globalLandmarkList = landmarkList;
    globalBlobEvent = blobEvent.data;
    landmarkList = null; // we saved it, so we don't need this data anymore
    recorder = null; // we saved it, so we don't need this data anymore
}



/*
 * This function returns a random number from 1 through 10 million.
 */
function getRandomId() {
    const d = new Date();
    const date = d.toISOString() //date is in UK time(hours will seem wrong but the rest is great)
    const date_ = date.replaceAll(":", "_");
    return date_ +"-"+Math.ceil(Math.random() * 10000000);
}


function onHandsResults(handResults, isFind) {
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
        saveFrameForFindOrCollect(handResults, imageAsBlob);
        console.log("going to waitForButtons")
    }
    if (recordingVideo) {
        landmarkList.push(handResults.multiHandLandmarks);
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
    document.addEventListener("keydown", onKeydown);
    document.addEventListener("keyup", onKeyup);
}
