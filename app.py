# start import lib
import flask, base64, io, cv2, numpy as np
from PIL import Image
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from server.entity.person import Person
from server.face_processing.processing import get_face, get_emberding
from server.db.connectDB import connection

UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# config server
app = Flask(__name__)
CORS(app)


def time(s1, s2):
    s1, s2 = str(s1), str(s2)
    hour1 = int(s1[0:2])
    hour2 = int(s2[0:2])
    min1 = int(s1[3:5])
    min2 = int(s2[3:5])
    second1 = int(s1[6:8])
    second2 = int(s2[6:8])
    ms1 = int(s1[9:12])
    ms2 = int(s2[9:12])
    return (hour2 - hour1) * 3600 + (min2 - min1) * 60 + (second2 - second1) + (ms2-ms1)/1000

# handle http
@app.route("/huyen")
def index1():
    return "Hello REVA!"


@app.route("/sign_up", methods=['POST'])
def sign_up():
    time_start = str(datetime.now().time())
    request_json = request.get_json()
    face_base64 = request_json.get('imgBase64')
    username = request_json.get('username')
    name = request_json.get('name')
    phone = request_json.get('phone')
    email = request_json.get('email')
    sex = request_json.get('sex')
    ip_address = flask.request.remote_addr
    print("Yêu cầu: Đăng kí tài khoản.")
    print("Đã nhận từ: " + ip_address + " ,luc " + str(datetime.now()))
    print(
        "Dữ liệu nhận được: " + "username: " + username + ", name: " + name + ", phone: " + phone + ", email: " + email + ", sex: " + sex)
    print(
        "------------------------------------------------------------------------------------------------------------")
    if face_base64 is None:
        note = "Loi gui anh, vui long gui lai!"
        time_end = str(datetime.now().time())
        return jsonify({'status': 0, 'result': note, 'time_processing': time(time_start, time_end)})
    else:
        person = Person(username, name, phone, email, sex, None, face_base64)
        result = person.sign_up()
        time_end = str(datetime.now().time())
        time_processing = time(time_start, time_end)
        result['time_processing'] = time_processing
        return jsonify(result)
        # return person.sign_up()

@app.route("/login", methods=['POST'])
def login():
    time_start = str(datetime.now().time())
    request_json = request.get_json()
    face_base64 = request_json.get('imgBase64')
    username = request_json.get('username')
    ip_address = flask.request.remote_addr
    print("Yêu cầu: Đăng nhập.")
    print("Đã nhận từ: " + ip_address + " ,luc " + str(datetime.now()))
    print("Dữ liệu nhận được: " + "username: " + username)
    if face_base64 is None:
        note = "Loi gui anh, vui long gui lai!"
        time_end = str(datetime.now().time())
        return jsonify({'status': 0, 'result': note, 'time_processing': time(time_start, time_end)})
    else:
        person = Person(username, None, None, None, None, None, face_base64)
        result = person.login()
        time_end = str(datetime.now().time())
        time_processing = time(time_start, time_end)
        result['time_processing'] = time_processing
        return jsonify(result)
        # return person.login()


@app.route("/return_profile", methods=['POST'])
def return_profile():
    time_start = str(datetime.now().time())
    request_json = request.get_json()
    username = request_json.get('username')
    ip_address = flask.request.remote_addr
    print("Yêu cầu: Lấy thông tin cá nhân.")
    print("Đã nhận từ: " + ip_address + " ,luc " + str(datetime.now()))
    print("Dữ liệu nhận được: " + "username: " + username)
    print("-----------------------------------------------------------------------------------------------------------")
    person = Person(username, None, None, None, None, None, None)
    result = person.return_profile()
    time_end = str(datetime.now().time())
    time_processing = time(time_start, time_end)
    result['time_processing'] = time_processing
    return jsonify(result)
    # return person.return_profile()
    # return jsonify(result)


@app.route("/edit_profile", methods=['POST'])
def edit_profile():
    time_start = str(datetime.now().time())
    request_json = request.get_json()
    username = request_json.get('username')
    face_base64 = request_json.get('imgBase64')
    name = request_json.get('name')
    phone = request_json.get('phone')
    email = request_json.get('email')
    sex = request_json.get('sex')
    ip_address = flask.request.remote_addr
    print("Yêu cầu: Chỉnh sửa thông tin cá nhân.")
    print("Đã nhận từ: " + ip_address + " ,luc " + str(datetime.now()))
    print(
        "Dữ liệu nhận được: " + "username: " + username + ", name: " + name + ", phone: " + phone + ", email: " + email + ", sex: " + sex)
    print(
        "------------------------------------------------------------------------------------------------------------")
    person = Person(username, name, phone, email, sex, None, face_base64)
    result = person.change_profile()
    time_end = str(datetime.now().time())
    time_processing = time(time_start, time_end)
    result['time_processing'] = time_processing
    return jsonify(result)
    # return person.change_profile()

#
# @app.route("/change_face", methods=['POST'])
# def change_face():
#     request_json = request.get_json()
#     face_base64 = request_json.get('imgBase64')
#     username = request_json.get('username')
#     ip_address = flask.request.remote_addr
#     print("Yêu cầu: Thay đổi khuôn mặt đăng nhập.")
#     print("Đã nhận từ: " + ip_address + " ,luc " + str(datetime.now()))
#     print("Dữ liệu nhận được: " + "username: " + username)
#     print(
#         "------------------------------------------------------------------------------------------------------------")
#     if face_base64 is None:
#         note = "Loi gui anh, vui long gui lai!"
#         return jsonify({'status': 0, 'result': note})
#     else:
#         try:
#             img = base64.b64decode(str(face_base64))
#             img = Image.open(io.BytesIO(img))
#             img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
#             face = get_face(img)
#             note = ""
#             if face is None:
#                 note += "Ảnh cập nhật phải chứa duy nhất một khuôn mặt. Vui lòng kiểm tra lại!"
#             if note != "":
#                 return jsonify({'status': 0, 'result': note})
#             else:
#                 face_emberding = get_emberding(face)
#                 face_str = ""
#                 for i in range(len(face_emberding)):
#                     face_str += str(face_emberding[i]) + " "
#
#                 connect = connection()
#                 cur = connect.cursor()
#                 update = "UPDATE person SET face_emberding = '%s',face_base64 = '%s' WHERE  username = '%s' " % (
#                     face_str, str(face_base64), username)
#
#                 cur.execute(update)
#                 connect.commit()
#
#                 return jsonify({'status': 1})
#         except Exception as e:
#             print("Error: ", e)
#             note = "Lỗi xử lí!"
#             return jsonify({'status': 0, 'result': note})
#
#
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=80)
    # http_server = WSGIServer(('0.0.0.0', 80), app)
    # http_server.serve_forever()
