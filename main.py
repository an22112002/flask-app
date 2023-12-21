from flask import Flask, request, jsonify, json
from flask_restful import Api, Resource, abort, reqparse
from hashlib import md5
import random

from connectDB import MySqlDB_connect

BASE_STR = '''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-=+[{]}\|;:<>/?`~'''

def random_string(lenght):
    s = ""
    for i in range(0, lenght):
        s+=BASE_STR[random.randint(0, 88)]
    return s

def MD5_hashing(text):
    MD5 = md5()
    MD5.update(text.encode("utf-8"))
    return MD5.hexdigest()

def checkEdited(sectionScore):
    if None in sectionScore.values():
        return False
    else:
        return True
    
def toFloat(x):
    if x is not None:
        return float(x)
    else:
        return 0
app = Flask(__name__)
api = Api(app)

account_post_get_args = reqparse.RequestParser()
account_post_get_args.add_argument("account", type=str, help="Tên tài khoản", required=True)
account_post_get_args.add_argument("password", type=str, help="Mật khẩu tài khoản", required=True)
account_put_args = reqparse.RequestParser()
account_put_args.add_argument("id", type=str, help="Id người dùng", required=True)
account_put_args.add_argument("newPassword", type=str, help="Mật khẩu mới", required=True)

class Account(Resource):
    def get(self):
        data = account_post_get_args.parse_args()
        info = db.getAccountInfo(data["account"])
        if len(info) == 0:
            abort(409, message="Không có tài khoản này")
        else:
            if MD5_hashing(info[0]['Spice']+data["password"]) == info[0]['Spice&Password']:
                return {"message" : "Cho phép truy cập", "Id" : info[0]['Id']}
            else:
                abort(409, message="Sai mật khẩu")
    def put(self):
        data = account_put_args.parse_args()
        spice = random_string(10)
        values = (spice, MD5_hashing(spice+data["newPassword"]), data["id"])
        result = db.changePassword(values)
        if result:
            return {'message' : "Mật khẩu đã được đổi"}
        else:
            abort(409, message="Mật khẩu chưa được đổi")
    def post(self):
        data = account_post_get_args.parse_args()
        info = db.getAccountInfo(data["account"])
        # Kiểm tra tên đã có chưa
        if len(info) != 0:
            abort(409, message="Tên đã được đăng ký")
        else:
            # Thêm vào database
            id = random_string(10)
            while db.haveID_user(id):
                id = random_string(10)
            spice = random_string(10)
            new_account = (id, data["account"], spice, MD5_hashing(spice+data["password"]))
            result = db.createAnAccount(new_account)
            if result:
                return {'message' : "Tài khoản đã được thêm vào"}
            else:
                abort(409, message="Tài khoản chưa được thêm")
    
ep_get_args = reqparse.RequestParser()
ep_get_args.add_argument("id", type=str, help="Id người dùng", required=True)
ep_post_args = reqparse.RequestParser()
ep_post_args.add_argument("id", type=str, help="Id người dùng", required=True)
ep_post_args.add_argument("TenChuongTrinh", type=str, help="Id người dùng", required=True)
ep_post_args.add_argument("TongSoTinChi", type=float, help="Id người dùng", required=True)
ep_del_args = reqparse.RequestParser()
ep_del_args.add_argument("id_chuongTrinh", type=str, help="Id chương trình", required=True)
class EducationProgram(Resource):
    def get(self):
        data = ep_get_args.parse_args()
        data_chuongtrinh = db.getEducationProgram(data["id"])
        if data_chuongtrinh == None:
            abort(409, message="Không có chương trình đào tạo nào")
        else:
            return jsonify(data_chuongtrinh) 
    def post(self):
        data = ep_post_args.parse_args()
        id_program = random_string(10)
        while db.haveID_program(id_program):
            id_program = random_string(10)
        if db.addNewEducationProgram((id_program, data["TenChuongTrinh"], data["TongSoTinChi"], data["id"])):
            return {'message' : "Đã thêm chương trình"}
        else:
            abort(409, message="Chưa thêm chương trình")

    def delete(self):
        data = ep_del_args.parse_args()
        if db.deleteEducationProgram(data["id_chuongTrinh"]):
            return {'message' : "Đã xóa chương trình"}
        else:
            abort(409, message="Chưa xóa chương trình")

ss_post_args = reqparse.RequestParser()
ss_post_args.add_argument("Id_ChuongTrinh", type=str, help="Id người dùng", required=True)
ss_post_args.add_argument("TenMon", type=str, help="Id người dùng", required=True)
ss_post_args.add_argument("SoTinChi", type=float, help="Id người dùng", required=True)
ss_post_args.add_argument("TiLeTX", type=str, help="Id người dùng", required=True)
ss_post_args.add_argument("TiLeDiem", type=str, help="Id người dùng", required=True)
ss_get_args = reqparse.RequestParser()
ss_get_args.add_argument("id_chuongTrinh", type=str, help="Id chương trình", required=True)
ss_del_args = reqparse.RequestParser()
ss_del_args.add_argument("id_hocPhan", type=str, help="Id học phần", required=True)
ss_put_args = reqparse.RequestParser()
ss_put_args.add_argument("Id_HocPhan", type=str, help="Id học phần", required=True)
ss_put_args.add_argument("Tx1", type=float, required=True)
ss_put_args.add_argument("Tx2", type=float, required=True)
ss_put_args.add_argument("Tx3", type=float, required=True)
ss_put_args.add_argument("Tx4", type=float, required=True)
ss_put_args.add_argument("Tx5", type=float, required=True)
ss_put_args.add_argument("Cc", type=float, required=True)
ss_put_args.add_argument("Gk", type=float, required=True)
ss_put_args.add_argument("Ck", type=float, required=True)
class SectionScore(Resource):
    def get(self):
        data = ss_get_args.parse_args()
        data_diemhocphan = db.getSectionScore(data["id_chuongTrinh"])
        for diemhocphan in data_diemhocphan:
            # thêm giá trị Edited để biết diemhocphan đã nhập chưa
            diemhocphan["Edited"] = checkEdited(diemhocphan)
            # đổi dữ liệu decimal sang float để gửi đi
            diemhocphan["Tx1"] = toFloat(diemhocphan["Tx1"])
            diemhocphan["Tx2"] = toFloat(diemhocphan["Tx2"])
            diemhocphan["Tx3"] = toFloat(diemhocphan["Tx3"])
            diemhocphan["Tx4"] = toFloat(diemhocphan["Tx4"])
            diemhocphan["Tx5"] = toFloat(diemhocphan["Tx5"])
            diemhocphan["GiuaKy"] = toFloat(diemhocphan["GiuaKy"])
            diemhocphan["CuoiKy"] = toFloat(diemhocphan["CuoiKy"])
            diemhocphan["ChuyenCan"] = toFloat(diemhocphan["ChuyenCan"])
        return jsonify(data_diemhocphan) 
    # thêm học phần mới
    def post(self):
        data = ss_post_args.parse_args()
        Id_HocPhan = random_string(10)
        while db.haveID_score(Id_HocPhan):
            Id_HocPhan = random_string(10)
        new_score = (Id_HocPhan, data["Id_ChuongTrinh"], data["TenMon"], data["SoTinChi"], data["TiLeTX"], data["TiLeDiem"])
        if db.addNewSectionScore(new_score):
            return {'message' : "Học phần đã được thêm vào"}
        else:
            abort(409, message="Học phần chưa được thêm")
    def put(self):
        d = ss_put_args.parse_args()
        updateValue = (d["Tx1"],d["Tx2"],d["Tx3"],d["Tx4"],d["Tx5"],d["Gk"],d["Ck"],d["Cc"],d["Id_HocPhan"])
        if db.updateSectionScore(updateValue):
            return {'message' : "Học phần đã được cập nhật"}
        else:
            abort(409, message="Học phần chưa được cập nhật")
    def delete(self):
        data = ss_del_args.parse_args()
        if db.deleteSectionScore(data["id_hocPhan"]):
            return {'message' : "Đã xóa học phần"}
        else:
            abort(409, message="Chưa xóa học phần")
        

api.add_resource(Account, "/account")
api.add_resource(EducationProgram, "/ep")
api.add_resource(SectionScore, "/ss")

if __name__ == '__main__':
    db = MySqlDB_connect()
    app.run(host="0.0.0.0", port=5000, debug=True)
