from flask import Flask, send_file
from flask_restful import Api
from werkzeug.security import generate_password_hash
from backend.models import User
from backend.config import Config
from backend.extensions import db, cac, jwt
import os



def create_app():
    app = Flask(__name__, static_folder='frontend/static')
    app.config.from_object(Config)

    api = Api(app)

    db.init_app(app)
    cac.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        create_admin_user()

    from backend.apis import (
        LoginAPI, StudentRegisterAPI, CompanyRegisterAPI, LogOutAPI,

        AdminCompaniesAPI, AdminApproveRejectCompanyAPI, AdminPlacementDrivesAPI, AdminDriveDetailsAPI,
        AdminApproveRejectDriveAPI, AdminStudentsAPI, AdminSearchCompanyAPI, AdminSearchStudentAPI,
        AdminBlacklistStudentAPI, AdminBlacklistCompanyAPI, AdminStudentApplicationsAPI, AdminSummaryAPI, AdminProfileAPI,

        CompanyDrivesAPI, CompanyDriveDetailsAPI, CompanyCloseDriveAPI, CompanyCreatePlacementDriveAPI,
        CompanyStudentApplicationsAPI, CompanyApplicationDetailsAPI, CompanyUpdateApplicationStatusAPI, CompanyProfileAPI,

        StudentAllDrivesAPI, StudentDriveDetailsAPI, StudentApplyDriveAPI, StudentApplicationHistoryAPI,
        StudentExportApplicationsAPI, StudentEligibleDrivesAPI, StudentProfileAPI
    )

    api.add_resource(LoginAPI, '/api/login')
    api.add_resource(StudentRegisterAPI, '/api/student/register')
    api.add_resource(CompanyRegisterAPI, '/api/company/register')
    api.add_resource(LogOutAPI, '/api/logout')


    api.add_resource(AdminCompaniesAPI, '/api/admin/companies')
    api.add_resource(AdminApproveRejectCompanyAPI, '/api/admin/approve_reject_company')
    api.add_resource(AdminPlacementDrivesAPI, '/api/admin/placement_drives')
    api.add_resource(AdminDriveDetailsAPI, '/api/admin/drive_detail/<int:id>')
    api.add_resource(AdminApproveRejectDriveAPI, '/api/admin/approve_reject_drive')
    api.add_resource(AdminStudentsAPI, '/api/admin/students')
    api.add_resource(AdminSearchStudentAPI, '/api/admin/search_student/<int:id>')
    api.add_resource(AdminSearchCompanyAPI, '/api/admin/search_company/<int:id>')
    api.add_resource(AdminBlacklistStudentAPI, '/api/admin/blacklist_student')
    api.add_resource(AdminBlacklistCompanyAPI, '/api/admin/blacklist_company')
    api.add_resource(AdminStudentApplicationsAPI, '/api/admin/student_applications')
    api.add_resource(AdminSummaryAPI, '/api/admin/summary/<string:chart>')
    api.add_resource(AdminProfileAPI, '/api/admin/profile')


    api.add_resource(CompanyDrivesAPI, '/api/company/drives')
    api.add_resource(CompanyDriveDetailsAPI, '/api/company/drive_detail/<int:id>')
    api.add_resource(CompanyCloseDriveAPI, '/api/company/close_drive')
    api.add_resource(CompanyCreatePlacementDriveAPI, '/api/company/create_drive')
    api.add_resource(CompanyStudentApplicationsAPI, '/api/company/student_applications')
    api.add_resource(CompanyApplicationDetailsAPI, '/api/company/application_detail/<int:id>')
    api.add_resource(CompanyUpdateApplicationStatusAPI, '/api/company/update_application_status')
    api.add_resource(CompanyProfileAPI, '/api/company/profile')


    api.add_resource(StudentAllDrivesAPI, '/api/student/all_drives')
    api.add_resource(StudentDriveDetailsAPI, '/api/student/drive_detail/<int:id>')
    api.add_resource(StudentEligibleDrivesAPI, '/api/student/eligible_drives')
    api.add_resource(StudentApplyDriveAPI, '/api/student/apply_drive')
    api.add_resource(StudentApplicationHistoryAPI, '/api/student/application_history')
    api.add_resource(StudentExportApplicationsAPI, '/api/student/export_csv')
    api.add_resource(StudentProfileAPI, '/api/student/profile')


    return app



def create_admin_user():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            username='Admin',
            email='admin@gmail.com',
            hashed_password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()



app = create_app()


from backend.worker import init_celery
celery = init_celery(app)


@app.route("/download_csv/<filename>")
def download_csv(filename):
    filepath = os.path.join(app.root_path, "exports", filename)

    if not os.path.exists(filepath):
        return {"error": "File not found"}, 404

    return send_file(filepath, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
