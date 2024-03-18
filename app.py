from flask import Flask, render_template, Response
import cv2
import numpy as np
import pyscreenshot as ImageGrab

app = Flask(__name__)

def gen_frames():
    while True:
        screen = ImageGrab.grab()  # Capture the screen
        screen_np = np.array(screen)
        
        # Resize the captured screen to fit the viewport while maintaining aspect ratio
        aspect_ratio = 16 / 9
        height, width, _ = screen_np.shape
        target_width = int(height * aspect_ratio)
        resized_screen = cv2.resize(screen_np, (target_width, height))
        
        # Convert the resized screen to RGB color space
        resized_screen_rgb = cv2.cvtColor(resized_screen, cv2.COLOR_BGR2RGB)
        
        # Convert the resized screen to JPEG format
        ret, buffer = cv2.imencode('.jpg', resized_screen_rgb)
        frame = buffer.tobytes()
        
        # Yield the frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
