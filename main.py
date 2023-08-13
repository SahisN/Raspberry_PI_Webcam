from flask import Flask, Response, render_template
import cv2
import os
import signal

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
    # print(f"Button pressed: {direction}")
    if direction == "up":
        print("moving up")

    elif direction == "down":
        print("moving down")

    elif direction == "right":
        print("moving right")

    elif direction == "left":
        print("moving left")

    return "OK"


@app.route("/shutdown", methods=["POST"])
def shutdown():
    print("Shutting down the server...")
    os.kill(os.getpid(), signal.SIGINT)

    return "Server shutting down..."


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
