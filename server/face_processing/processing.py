import numpy as np
from insightface.model_zoo import get_model

from server.face_processing import face_align

model = get_model('arcface_r100_v1')  # init model get_emmberding_face
ctx_id = -1
model.prepare(ctx_id=ctx_id)

from mtcnn.mtcnn import MTCNN

detector = MTCNN()

def get_face(Img):
    faces = detector.detect_faces(Img)
    if len(faces) != 1:
        return None
    else:
        box = faces[0]['box']
        keypoints = faces[0]['keypoints']
        left_eye = keypoints['left_eye']
        right_eye = keypoints['right_eye']
        nose = keypoints['nose']
        mouth_left = keypoints['mouth_left']
        mouth_right = keypoints['mouth_right']
        points = np.asarray([left_eye, right_eye, nose, mouth_left, mouth_right])
        face_extracted = face_align.preprocess(Img, box, points, image_size='112,112')
        return face_extracted


def get_emberding(face_aligned):
    return model.get_embedding(face_aligned).flatten()


# def similarity_two_face(img1_base64, img2_base64):
#     if img1_base64 is None or img2_base64 is None:
#         note = "Loi gui anh, vui long gui lai!"
#         return 0, note
#     else:
#         try:
#             img1 = base64.b64decode(str(img1_base64))
#             img1 = Image.open(io.BytesIO(img1))
#             # img1 = img1.convert('RGB')
#             img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_BGR2RGB)
#             face1 = get_face(img1)
#
#             img2 = base64.b64decode(str(img2_base64))
#             img2 = Image.open(io.BytesIO(img2))
#             # img2 = img2.convert('RGB')
#             img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_BGR2RGB)
#             # face2 = model.get_input(img2)
#             face2 = get_face(img2)
#
#             note = ""
#             if face1 is None or face2 is None:
#                 note += "Mỗi ảnh phải chứa duy nhất một khuôn mặt. Vui lòng kiểm tra lại!"
#             if note != "":
#                 return 0, note
#             else:
#                 emb1 = model.get_embedding(face1).flatten()
#                 print(emb1)
#                 emb2 = model.get_embedding(face2).flatten()
#                 sim = np.dot(emb1, emb2) / (norm(emb1) * norm(emb2))
#                 return 1, round(float(sim), 2)
#         except Exception as e:
#             print("Error: ", e)
#             note = "Lỗi xử lí!"
#             return 0, note


# def get_facee(file):
#     img = Image.open(file)
#     img = img.convert('RGB')
#     img = asarray(img)
#     img2 = img
#     faces = detector.detect_faces(img)
#     x1, y1, width, height = faces[0]['box']
#     x2, y2 = x1 + width, y1 + height
#     # cắt khuôn mặt
#     face = img[y1:y2, x1:x2]
#     # image = Image.fromarray(face)
#     # image = image.resize((112,112))
#     # face_array = asarray(image)
#     face_array = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
#     cv2.imshow('t', face_array)
#     cv2.waitKey(0)
#
#     img2 = get_face(img2)
#     img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
#     cv2.imshow('t', img2)
#     cv2.waitKey(0)

# get_facee("D:\Đồ án\Ảnh\chuacat.jpg")
