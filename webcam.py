# save project as file

from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    resized_image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Resized Webcam Image", resized_image)

    # Make the image a numpy array and reshape it to the models input shape.
    resized_image = np.asarray(resized_image, dtype=np.float32).reshape(1, 224, 224, 3) # 224

    # Normalize the image array
    resized_image = (resized_image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(resized_image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    cv2.putText(image, "Class: " + class_name[2:-1], (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,100,0), 2)
    cv2.putText(image, str(float("{:.2f}".format(confidence_score*100))) + "%", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,100,0), 2)
    
    # str(float("{:.2f}".format(confidence_score*100))) + "%"
    
    cv2.imshow("Webcam Image", image)
    
    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()