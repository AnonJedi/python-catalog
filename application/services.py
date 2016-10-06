from application.models import Admin


class AdminService:

    @staticmethod
    def check_admin_login(username, password):
        admin_from_db = Admin.query.filter(Admin.username == username).first()
        if admin_from_db:
            return admin_from_db.check_password(password)
        return False
