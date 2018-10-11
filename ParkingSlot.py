import cv2

class ParkingSlot:

    def __init__(self, _point_tl, _point_tr, _point_bl, _point_br, _id):
        self.point_tl = _point_tl
        self.point_tr = _point_tr
        self.point_bl = _point_bl
        self.point_br = _point_br
        self.state = False
        self.id = _id

    def __str__(self):
        return "ID: %s , Top left: %s, Top right: %s, Bottom left: %s, Bottom right: %s" % (self.id, self.point_tl, self.point_tr, self.point_bl, self.point_br)