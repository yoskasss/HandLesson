from flask import Flask, render_template, request, redirect, Response, jsonify
from camera import VideoCamera

app = Flask(__name__)

# Kullanıcı bilgilerini saklamak için basit bir liste
users = []

# VideoCamera sınıfını bir kez başlatıyoruz
camera = VideoCamera()

@app.route('/')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    users.append({"name": name})
    return redirect('/game')

@app.route('/game')
def game_page():
    return render_template('game.html')

@app.route('/stats')
def stats_page():
    return render_template('stats.html', users=users)

# Kamera görüntüsünü yayınlayan route
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fingers_count')
def fingers_count():
    # Toplam parmak sayısını almak için kamera objesini kullanıyoruz
    total_fingers = camera.totalFingers
    return jsonify(totalFingers=total_fingers)

if __name__ == '__main__':
    app.run(debug=True)
