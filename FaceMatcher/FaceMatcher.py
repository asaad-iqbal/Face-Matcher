import cv2
import face_recognition
import numpy as np
import pickle


class FaceMatcher(object):

    def __init__(self, encode_file_path):
        self.efp = encode_file_path
        try:
            with open(self.efp, 'rb') as handle:
                self.encodings = pickle.load(handle)
        except:
            self.encodings = {}

    def matchFace(self, img):
        matched_ids = []
        npimg = np.fromstring(img, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        h = img.shape[0]
        desirable_height = 600
        if h > desirable_height:
            r = desirable_height / img.shape[0]
            dim = (int(img.shape[1] * r), desirable_height)
            # perform the resizing
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        
        img_encodings = face_recognition.face_encodings(img)
        if not img_encodings:
            return {'status': 'Image does not have any face'}
        for img_encoding in img_encodings:
            for id, encodings in self.encodings.items():
                matches = face_recognition.compare_faces(encodings, img_encoding, tolerance=0.6)
                if True in matches:
                    if id not in matched_ids:
                        matched_ids.append(id)
        if not matched_ids:
            return {'status':'No match found'}
        
        return {'status':'Match found','UIDs': matched_ids}


    def addFace(self, id, img):
        if not id.strip():
            return {'status': 'uid empty'}
        npimg = np.fromstring(img, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        h = img.shape[0]
        desirable_height = 600
        if h > desirable_height:
            r = desirable_height / img.shape[0]
            dim = (int(img.shape[1] * r), desirable_height)
            # perform the resizing
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img_encodings = face_recognition.face_encodings(img)
        if not img_encodings:
            return {'status': 'Image does not have any face'}
        img_encoding = img_encodings[0]
        if id in self.encodings:
            for encoding in self.encodings[id]:
                if (img_encoding == encoding).all():
                    return {'status': 'Face was already uploaded'}
            self.encodings[id].append(img_encoding)
        else:
            self.encodings[id] = [img_encoding]
        with open('encodings.pickle', 'wb') as handle:
            pickle.dump(self.encodings, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return {'status': 'Face successully uploaded'}
