# start import lib
import base64, io, cv2, numpy as np
from PIL import Image
from flask import jsonify
from server.face_processing.processing import get_face, get_emberding
from numpy.linalg import norm
from server.db.connectDB import connection

# from server.person import Person

connect = connection()
def signup(PerSon):
    imgBase64 = PerSon.face_base64
    username = PerSon.username
    name = PerSon.name
    phone = PerSon.phone
    email = PerSon.email
    sex = PerSon.sex
    try:
        cur = connect.cursor()
        select = " SELECT * FROM person WHERE username = '%s' " % (username)
        cur.execute(select) # kiểm tra tên đăng nhập đã tồn tại hay chưa
        data = cur.fetchall()
        if (len(data) > 0):
            note = "Tên đăng nhập đã tồn tại!!!"
            print(note)
            return jsonify({'status': 0, 'result': note})
        else:
            img = base64.b64decode(str(imgBase64))  # giải mã ảnh khuôn mặt đăng kí
            img = Image.open(io.BytesIO(img))
            img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            face = get_face(img)
            note = ""
            if face is None:  # kiểm tra khuôn mặt trong ảnh đăng kí
                note += "The registered photo must contain only one face. Please check again!"
            if note != "":
                return jsonify({'status': 0, 'result': note})
            else:
                face_emberding = get_emberding(face)  # lấy đặc trưng khuôn mặt
                face_str = ""
                for i in range(len(face_emberding)):
                    face_str += str(face_emberding[i]) + " "
                insert = "INSERT INTO person VALUES('%s', '%s', '%s', '%s', '%s', '%s','%s') " % (
                    username, name, phone, email, sex, face_str, str(imgBase64))
                cur.execute(insert) # lưu các thông tin người dùng vào db
                connect.commit()
                return jsonify({'status': 1})
    except Exception as e:
        print("Error: ", e)
        note = "The system is maintenance!"
        return jsonify({'status': 0, 'result': note})


def login(Person):
    username = Person.username
    imgBase64 = Person.face_base64
    try:
        cur = connect.cursor()
        select = " SELECT * FROM person WHERE username = '%s' " % (username)
        cur.execute(select)
        data = cur.fetchall()
        if (len(data) == 0):  # kiem tra ten dang nhap
            note = "Username does not exist!!!"
            return jsonify({'status': 0, 'result': note})
        else:
            for row in data:  # lay thong tin user
                username = row[0]
                name = row[1]
                phone = row[2]
                email = row[3]
                sex = row[4]
                face_str = row[5]
                face_base64 = row[6]
            face_str = face_str.strip()
            face_str = face_str.split(" ")
            face_signup = np.array(face_str, dtype=float)
            # Kiem tra thong tin khuon mat dang nhap
            img = base64.b64decode(str(imgBase64))
            img = Image.open(io.BytesIO(img))
            img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            face = get_face(img)
            note = ""
            if face is None: # ảnh đăng nhập không hợp lệ
                note += "The login photo must contain only one face. Please check again!"
                print("Ảnh không hợp lệ")
                print(
                    "------------------------------------------------------------------------------------------------------------")
                return jsonify({'status': 0, 'result': note})
            else:
                face_login = get_emberding(face) # trích xuất đặc trưng khuôn mặt đăng nhập
                sim = np.dot(face_signup, face_login) / (norm(face_signup) * norm(face_login)) # tính độ tương đồng với khuôn mặt đã đăng kí
                print("Độ tương đồng giữa 2 khuôn mặt là: ", sim)
                print(
                    "------------------------------------------------------------------------------------------------------------")
                if (sim > 0.53): #so sánh với ngưỡng
                    return jsonify({'status': 1, 'username': username,
                                    'name': name, 'phone': phone,
                                    'email': email, 'sex': sex, 'face_base64': face_base64})
                else:
                    note = "The face does not match your username, please check again!"
                    return jsonify({'status': 0, 'result': note})
    except Exception as e:
        print("Error: ", e)
        note = "The system is maintenance!"
        return jsonify({'status': 0, 'result': note})


def return_profile(Person):
    username = Person.username
    try:
        cur = connect.cursor()
        select = " SELECT * FROM person WHERE username = '%s' " % (username)
        cur.execute(select)
        data = cur.fetchall()

        for row in data:  # lay thong tin user
            username = row[0]
            name = row[1]
            phone = row[2]
            email = row[3]
            sex = row[4]
            face_base64 = row[6]
        return jsonify({'status': 1, 'username': username,
                        'name': name, 'phone': phone,
                        'email': email, 'sex': sex, 'face_base64': face_base64})
    except Exception as e:
        print("Error: ", e)
        note = "The system is maintenance!"
        return jsonify({'status': 0, 'result': note})


def change_profile(Person):
    username = Person.username
    imgBase64 = Person.face_base64
    name = Person.name
    phone = Person.phone
    email = Person.email
    sex = Person.sex
    try:
        img = base64.b64decode(str(imgBase64)) # giải mã ảnh khuôn mặt
        img = Image.open(io.BytesIO(img))
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        face = get_face(img)
        note = ""
        if face is None: #kiểm tra ảnh khuôn mặt
            note += "The updated photo must contain only one face. Please check again!"
        if note != "":
            return jsonify({'status': 0, 'result': note})
        else:
            face_emberding = get_emberding(face) # trích xuất đặc trưng khuôn mặt mới
            face_str = ""
            for i in range(len(face_emberding)):
                face_str += str(face_emberding[i]) + " "

        cur = connect.cursor()
        update = "UPDATE person SET name = '%s', phone = '%s', email = '%s', sex = '%s', face_emberding = '%s',face_base64 = '%s' WHERE  username = '%s' " % (
            name, phone, email, sex, face_str, str(imgBase64), username)
        cur.execute(update) # cập nhật lại thông tin người dùng
        connect.commit()
        return jsonify({'status': 1})
    except:
        return jsonify({'status': 0, 'result': "The system is maintenance!!!"})
