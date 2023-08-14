from flask import Flask, Response, render_template, request
import cv2
import os
import signal

import RPi.GPIO as GPIO
from PCA9685 import PCA9685

app = Flask(__name__)


# Video capturing using OpenCV
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            _, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/button_press/<direction>")
def button_press(direction):
    x = int(request.args.get("x"))  # Get the x value from the URL parameters
    y = int(request.args.get("y"))  # Get the y value from the URL parameters

    print(x)
    print(y)

    # print(f"Button pressed: {direction}")
    if direction == "up":
        print("moving up")
        pwm.setRotationAngle(1, y)

    elif direction == "down":
        print("moving down")
        pmw.setRotationAngle(1, y)

    elif direction == "right":
        print("moving right")
        pmw.setRotationAngle(0, x)

    elif direction == "left":
        print("moving left")
        pmw.setRotationAngle(0, x)

    # Process the direction, x_value, and y_value as needed
    # For example, you might print or log them
    # print(f"Direction: {direction}, X Value: {x_value}, Y Value: {y_value}")

    return "OK"


@app.route("/shutdown", methods=["POST"])
def shutdown():
    print("Shutting down the server...")
    pwm.exit_PCA9685()
    os.kill(os.getpid(), signal.SIGINT)

    return "Server shutting down..."


if __name__ == "__main__":
    pmw = PCA9685()
    pmw.setPWMFreq(50)
    pwm.setRotationAngle(0, x)
    pwm.setRotationAngle(1, y)
    app.run(host="0.0.0.0", debug=True)
