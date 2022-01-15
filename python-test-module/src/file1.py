import cv2
import mediapipe as mp
print("Hello world")
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
# help(mp_hands.Hands)

# path3 = r'C:\Users\Genevieve\Downloads\l3.jpg'
# path2 = r'C:\Users\Genevieve\Downloads\l2.jpg'
# path1 = r'C:\Users\Genevieve\Downloads\l1.jpg'
# IMAGE_FILES = [path1, path2, path3]
resultsList = []

# for path in IMAGE_FILES:
#     image = cv2.flip(cv2.imread(path), 1)
#     cv2.imshow(path, image)
#     with mp_hands.Hands(
#         static_image_mode=True,
#         max_num_hands=1,
#         min_detection_confidence=0.5) as hands:
#         # Read an image, flip it around y-axis for correct handedness output (see
#         # above).
#         # Convert the BGR image to RGB before processing.
#         rgbimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = hands.process(rgbimage)
#
#
#         # Print handedness and draw hand landmarks on the image.
#         print('Handedness:', results.multi_handedness)
#         image_height, image_width, _ = image.shape
#         annotated_image = image.copy()
#         hand_landmarks = results.multi_hand_landmarks[0]
#         # mp_drawing.draw_landmarks(
#         #     rgbimage,
#         #     hand_landmarks,
#         #     mp_hands.HAND_CONNECTIONS,
#         #     mp_drawing_styles.get_default_hand_landmarks_style(),
#         #     mp_drawing_styles.get_default_hand_connections_style())
#         for hand_world_landmarks in results.multi_hand_world_landmarks:
#             mp_drawing.plot_landmarks(
#                 hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
#         for hand_landmarks in results.multi_hand_landmarks:
#             print('hand_landmarks:', hand_landmarks)
#             print(
#                 f'Index finger tip coordinates: (',
#                 f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#                 f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
#             )
#             mp_drawing.draw_landmarks(
#                 annotated_image,
#                 hand_landmarks,
#                 mp_hands.HAND_CONNECTIONS,
#                 mp_drawing_styles.get_default_hand_landmarks_style(),
#                 mp_drawing_styles.get_default_hand_connections_style())
#         # Draw hand world landmarks.
#         for hand_world_landmarks in results.multi_hand_world_landmarks:
#             mp_drawing.plot_landmarks(
#                 hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
#
# for results in resultsList:
#     mp_drawing.draw_landmarks(
#         annotated_image,
#         hand_landmarks,
#         mp_hands.HAND_CONNECTIONS,
#         mp_drawing_styles.get_default_hand_landmarks_style(),
#         mp_drawing_styles.get_default_hand_connections_style())
#     for hand_world_landmarks in results.multi_hand_world_landmarks:
#         mp_drawing.plot_landmarks(
#             hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
#


# add wait key. window waits until user presses a key
cv2.waitKey(0)
# and finally destroy/close all open windows
cv2.destroyAllWindows()


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

        key_pressed =  cv2.waitKey(5)

        if key_pressed % 256 == 27:
            break
        elif key_pressed % 256 == 32:
            cv2.imshow('Capture', cv2.flip(image, 1))
            resultsList.append(results)
            if len(resultsList) == 2:
                break
    difTotal = 0
    # for hand_landmarks in resultsList[0].multi_hand_landmarks:
    #     print('hand_landmarks:', hand_landmarks)

    for result in resultsList:
        print("---- Result -----")
        hand = result.multi_hand_landmarks[0]
        landmarks = hand.landmark
        for landmark in landmarks:
            print(f"landmark: {landmark.x} {landmark.y} {landmark.z}")

    print(f"resultsList: {resultsList}")
    print(f"thing {resultsList[0].multi_hand_landmarks[0].landmark[0].x}")
    for i in range(0,21):
        currentX =resultsList[0].multi_hand_landmarks[0].landmark[i].x - resultsList[1].multi_hand_landmarks[0].landmark[i].x
        currentX = currentX * currentX
        currentY =resultsList[0].multi_hand_landmarks[0].landmark[i].y - resultsList[1].multi_hand_landmarks[0].landmark[i].y
        currentY = currentY * currentY
        currentZ =resultsList[0].multi_hand_landmarks[0].landmark[i].z - resultsList[1].multi_hand_landmarks[0].landmark[i].z
        currentZ = currentZ * currentZ
        curPointDif = currentX + currentY + currentZ
        difTotal = difTotal + curPointDif
    print(f"difTotal {difTotal}")



cap.release()

# 0.25868996621453844                    - similar-ish
# difTotal 0.0045767651950870784         - basically the same
# difTotal 3.447838967408188              same shape different spot
#difTotal 0.523087603573555               palm vs fist
