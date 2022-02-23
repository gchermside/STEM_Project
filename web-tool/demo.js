// ==== Constants ====
const videoSize = {width: 1280, height: 720}; // must match the size in the HTML
const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');


// ==== Global Variables ====
let saveNextFrame = false;


// ==== Functions ====

/*
 * Function called when the user presses a key (while the browser is in the forefront).
 *
 * What it does is to use the space bar for recording.
 */
function onKeypress(event) {
    if (event.code === 'Space') {
        saveNextFrame = true;
    }
}


/*
 * Function called after a single frame has been taken.
 */
function saveSingleFrame(handResults) {
    console.log(handResults.multiHandLandmarks);
}


function onHandsResults(handResults) {
    if (handResults.multiHandLandmarks) {
        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        canvasCtx.drawImage(handResults.image, 0, 0, canvasElement.width, canvasElement.height);
        for (const landmarks of handResults.multiHandLandmarks) {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS,
                {color: '#00FF00', lineWidth: 5});
            drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2});
        }
        canvasCtx.restore();
    }
    if (saveNextFrame) {
        saveNextFrame = false;
        saveSingleFrame(handResults);
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
    const camera = new Camera(videoElement, {
        onFrame: async () => {
            await hands.send({image: videoElement});
        },
        width: videoSize.width,
        height: videoSize.height
    });
    camera.start();

    // --- Begin listening for space key ---
    document.addEventListener('keypress', onKeypress);
}


// ==== MAIN FUNCTION ====

startRunningCamera()
