from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import *
from backend.tasks import application_csv
from datetime import datetime
from backend.extensions import cac
from sqlalchemy import desc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os



#------------------------------------ LOGIN AND REGISTRATION APIS ----------------------------------#\

class LoginAPI(Resource):
    def post(self):
        cred = request.get_json()

        if not cred:
            response = {'message': 'Login credentials required'}
            return make_response(jsonify(response), 400)
        
        email = cred.get('email')
        password = cred.get('password')

        if not email or not password:
            response = {'message': 'Both email and password are required'}
            return make_response(jsonify(response), 400)
    
        user = User.query.filter_by(email=email).first()
        
        if not user:
            response = {'message': 'User not found!! Please register first.'}
            return make_response(jsonify(response), 404)
        
        if not check_password_hash(user.hashed_password, password):
            response = {'message': 'Incorrect password'}
            return make_response(jsonify(response), 401)
        
        if user.is_blacklisted:
            response = {'message': 'Your account has been blacklisted. Reach out to admin.'}
            return make_response(jsonify(response), 403)

        
        if user.role in ['company', 'student']:

            if user.role == 'student':
                student = Student.query.filter_by(user_id=user.id).first()
                if not student:
                    response = {'message': 'Student profile not found.'}
                    return make_response(jsonify(response), 404)
            elif user.role == 'company':
                company = Company.query.filter_by(user_id=user.id).first()
                if not company:
                    response = {'message': 'Company profile not found.'}
                    return make_response(jsonify(response), 404)

                if company.status !=  'approved':
                    response = {'message': f'Company registration stage: {str.upper(company.status)}. You can only login after approval.'}
                    return make_response(jsonify(response), 403)
        
        
        
        auth_token = create_access_token(identity=user.email)
        response = {
            'message': 'Login Successful',
            'auth_token': auth_token,
            'name': user.username,
            'email': user.email,
            'role': user.role
        }
        return make_response(jsonify(response), 200)





class StudentRegisterAPI(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            response = {'message': 'Fill all the required fields'}
            return make_response(jsonify(response), 400)
        
        student_name = data.get('student_name')
        email = data.get('email')
        password = data.get('password')
        branch = data.get('branch').lower()
        cgpa = float(data.get('cgpa'))
        year = int(data.get('year'))
        resume_path = data.get('resume_path', '')

        if not all([student_name, email, password, branch, cgpa, year]):
            response = {'message': 'Fill all the required fields'}
            return make_response(jsonify(response), 400)

        user = User.query.filter_by(email=email).first()

        if user:
            response = {'message': 'User already exists! Please Login.'}
            return make_response(jsonify(response), 409)
        
        hashed_password = generate_password_hash(password)
        new_student = User(
            username=student_name,
            email=email,
            hashed_password=hashed_password,
            role='student'
        )
        db.session.add(new_student)
        db.session.flush()

        student_profile = Student(
            user_id=new_student.id,
            student_name=student_name,
            branch=branch,
            cgpa=cgpa,
            year=year,
            resume_path=resume_path,
        )

        db.session.add(student_profile)
        db.session.commit()
        cac.delete_memoized(AdminStudentsAPI.get)

        response = {'message': 'Student registered successfully!! Please Login.'}
        return make_response(jsonify(response), 201)
    




class CompanyRegisterAPI(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            response = {'message': 'Fill all the required fields'}
            return make_response(jsonify(response), 400)
        
        company_name = data.get('company_name')
        email = data.get('email')
        password = data.get('password')
        hr_contact = data.get('hr_contact')

        if not all([company_name, email, password, hr_contact]):
            response = {'message': 'Fill all the required fields'}
            return make_response(jsonify(response), 400)

        user = User.query.filter_by(email=email).first()

        if user:
            response = {'message': 'Company already exists! Please Login.'}
            return make_response(jsonify(response), 409)
        
        hashed_password = generate_password_hash(password)
        new_company = User(
            username=company_name,
            email=email,
            hashed_password=hashed_password,
            role='company'
        )
        db.session.add(new_company)
        db.session.flush()

        company_profile = Company(
            user_id=new_company.id,
            company_name=company_name,
            hr_contact=hr_contact
        )

        db.session.add(company_profile)
        db.session.commit()
        cac.delete_memoized(AdminCompaniesAPI.get)

        response = {'message': 'Company registered successfully!! Wait for admin approval.'}
        return make_response(jsonify(response), 201)
    


#------------------------------------------- ADMIN APIS -------------------------------------------#


class AdminCompaniesAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        companies = Company.query.order_by(Company.company_id.desc()).all()
        companies_list = []
        for company in companies:
            user = User.query.filter_by(id=company.user_id).first()
            drive_count = PlacementDrive.query.filter_by(company_id=company.company_id).count()
            companies_list.append({
                'id': company.company_id,
                'name': company.company_name,
                'company_email': user.email,
                'hr_contact': company.hr_contact,
                'drive_count': drive_count,
                'status': company.status.upper(),
                'is_blacklisted': user.is_blacklisted
            })
        
        response = {'Companies': companies_list}
        return make_response(jsonify(response), 200)





class AdminApproveRejectCompanyAPI(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)

        data = request.get_json()

        if not data or not data.get('action'):
            response = {'message': 'Action required (approve/reject)'}
            return make_response(jsonify(response), 400)
        
        company_id = data.get('id')
        company = Company.query.filter_by(company_id=company_id).first()
        action = data.get('action').lower()

        if not company:
            response = {'message': 'Company not found'}
            return make_response(jsonify(response), 404)
        
        if action == 'approve':
            company.status = 'approved'
            message = 'Company approved successfully. They can now login'
        elif action == 'reject':
            company.status = 'rejected'
            message = 'Company registration rejected.'
        else:
            return make_response(jsonify({'message': 'Invalid action. Use approve or reject'}), 400)

        db.session.commit()
        cac.delete_memoized(AdminCompaniesAPI.get)
        cac.delete_memoized(AdminDriveDetailsAPI.get)
        response = {'message': message,
                    'company_id': company.company_id,
                    'company_name': company.company_name,
                    'status': company.status.upper()}
                    
        return make_response(jsonify(response), 200)





class AdminPlacementDrivesAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        drives = PlacementDrive.query.order_by(PlacementDrive.drive_id.desc()).all()
        drives_list = []
        for drive in drives:
            company = Company.query.filter_by(company_id=drive.company_id).first()
            application_count = Application.query.filter_by(drive_id=drive.drive_id).count()
            drives_list.append({
                'drive_id': drive.drive_id,
                'company_id': company.company_id if company else None,
                'company_name': company.company_name if company else None,
                'job_title': drive.job_title.upper(),
                'job_description': drive.job_description,
                'eligible_branch': drive.eligible_branch,
                'eligible_cgpa': drive.eligible_cgpa,
                'eligible_year': drive.eligible_year,
                'application_deadline' : str(drive.application_deadline),
                'total_applications': application_count,
                'status' : drive.status.upper(), 
                'created_date' : str(drive.created_date)
            })
        
        response = {'All_Placement_Drives': drives_list}
        return make_response(jsonify(response), 200)





class AdminDriveDetailsAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self, id):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        drive = PlacementDrive.query.filter_by(drive_id=id).first()

        if not drive:
            response = {'message': 'Drive not found'}
            return make_response(jsonify(response), 404)
        
        company = Company.query.filter_by(company_id=drive.company_id).first()
        application_count = Application.query.filter_by(drive_id=drive.drive_id).count()
        drive_det = {
            'drive_id': drive.drive_id,
            'company_id': company.company_id if company else None,
            'company_name': company.company_name if company else None,
            'job_title': drive.job_title.upper(),
            'job_desc': drive.job_description,
            'eligible_branch': drive.eligible_branch.upper(),
            'eligible_cgpa': drive.eligible_cgpa,
            'eligible_year': drive.eligible_year,
            'deadline' : str(drive.application_deadline),
            'total_applications': application_count,
            'status' : drive.status.upper(), 
            'created_date' : str(drive.created_date)
        }
        response = {'details': drive_det}
        return make_response(jsonify(response), 200)





class AdminApproveRejectDriveAPI(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        data = request.get_json()

        if not data or not data.get('action'):
            response = {'message': 'Action required (approve/reject)'}
            return make_response(jsonify(response), 400)
        
        drive_id = data.get('id')
        if not drive_id:
            response = {'message': 'Drive ID required'}
            return make_response(jsonify(response), 400)
        
        drive = PlacementDrive.query.filter_by(drive_id=drive_id).first()
        action = data.get('action').lower()

        if not drive:
            response = {'message': 'Drive not found'}
            return make_response(jsonify(response), 404)
        
        if drive.status != 'pending':
            response = {'message': f'Drive is already {str.upper(drive.status)}. Cannot change status now.'}
            return make_response(jsonify(response), 400)
        
        if action == 'approve':
            drive.status = 'approved'
            message = 'Drive approved successfully.'
        elif action == 'reject':
            drive.status = 'rejected'
            message = 'Drive rejected.'
        else:
            return make_response(jsonify({'message': 'Invalid action. Use approve or reject'}), 400)

        db.session.commit()
        cac.delete_memoized(StudentEligibleDrivesAPI.get)
        cac.delete_memoized(StudentAllDrivesAPI.get)
        cac.delete_memoized(AdminPlacementDrivesAPI.get)
        company = Company.query.filter_by(company_id=drive.company_id).first()
        response = {'message': message,
                    'drive_id': drive.drive_id,
                    'company_id': company.company_id,
                    'company_name': company.company_name,
                    'status': drive.status}
                    
        return make_response(jsonify(response), 200)





class AdminStudentsAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        students = Student.query.order_by(Student.student_id.desc()).all()
        students_list = []
        for student in students:
            user = User.query.filter_by(id=student.user_id).first()
            students_list.append({
                'student_id': student.student_id,
                'student_name': student.student_name,
                'email': user.email,
                'branch': student.branch.upper(),
                'year': student.year,
                'cgpa': student.cgpa,
                'is_blacklisted': user.is_blacklisted
            })
        response = {'Students': students_list}
        return make_response(jsonify(response), 200)
        




class AdminBlacklistStudentAPI(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        data = request.get_json()
        student_id = data.get('id')
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            response = {'message': 'Student not found'}
            return make_response(jsonify(response), 404)
        
        student_user = User.query.filter_by(id=student.user_id).first()

        if student_user.is_blacklisted:
            student_user.is_blacklisted = False
            response = {'message': 'Student removed from blacklist successfully!!'}
        else:
            student_user.is_blacklisted = True
            response = {'message': 'Student blacklisted successfully!!'}

        db.session.commit()
        cac.delete_memoized(AdminStudentsAPI.get)
        return make_response(jsonify(response), 200)





class AdminBlacklistCompanyAPI(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        data = request.get_json()
        company_id = data.get('id')
        company = Company.query.filter_by(company_id=company_id).first()
        if not company:
            response = {'message': 'Company not found'}
            return make_response(jsonify(response), 404)
        
        company_user = User.query.filter_by(id=company.user_id).first()

        if company_user.is_blacklisted:
            company_user.is_blacklisted = False
            response = {'message': 'Company removed from blacklist successfully!!'}
        else:
            company_user.is_blacklisted = True
            response = {'message': 'Company blacklisted successfully!!'}

        db.session.commit()
        cac.delete_memoized(StudentEligibleDrivesAPI.get)
        cac.delete_memoized(StudentAllDrivesAPI.get)
        cac.delete_memoized(AdminCompaniesAPI.get)
        return make_response(jsonify(response), 200)





class AdminSearchStudentAPI(Resource):
    @jwt_required()
    def get(self, id):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        student_id = id
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            response = {'message': 'Student not found'}
            return make_response(jsonify(response), 404)
        
        student_user = User.query.filter_by(id=student.user_id).first()
        student_info = {
            'id': student.student_id,
            'student_email': student_user.email,
            'name': student.student_name,
            'branch': student.branch.upper(),
            'year': student.year,
            'cgpa': student.cgpa,
            'is_blacklisted': student_user.is_blacklisted
        }
        response = {'Student_Info': student_info}
        return make_response(jsonify(response), 200)





class AdminSearchCompanyAPI(Resource):
    @jwt_required()
    def get(self, id):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        company_id = id
        company = Company.query.filter_by(company_id=company_id).first()
        if not company:
            response = {'message': 'Company not found'}
            return make_response(jsonify(response), 404)
        
        company_user = User.query.filter_by(id=company.user_id).first()
        drive_count = PlacementDrive.query.filter_by(company_id=company.company_id).count()
        company_info = {
            'id': company.company_id,
            'company_email': company_user.email,
            'name': company.company_name,
            'hr_contact': company.hr_contact,
            'drive_count': drive_count,
            'status': company.status.upper(),
            'is_blacklisted': company_user.is_blacklisted
        }
        response = {'Company_Info': company_info}
        return make_response(jsonify(response), 200)





class AdminStudentApplicationsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        applications = Application.query.order_by(Application.application_id.desc()).all()
        applications_list = []
        for app in applications:
            drive = PlacementDrive.query.filter_by(drive_id=app.drive_id).first()
            company = Company.query.filter_by(company_id=drive.company_id).first()
            applications_list.append({
                'application_id': app.application_id,
                'drive_id': app.drive_id,
                'company_id': company.company_id,
                'student_id': app.student_id,
                'applied_date': str(app.applied_date),
                'status': app.status.upper()
            })
        response = {'Applications': applications_list}
        return make_response(jsonify(response), 200)
    




class AdminSummaryAPI(Resource):
    @jwt_required()
    def get(self, chart):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        showchartfor = chart
        if showchartfor not in ['placement', 'drives']:
            response = {'message': 'Invalid graph type requested. Use placement or drives'}
            return make_response(jsonify(response), 400)
        
        if showchartfor == 'placement':
            applications = Application.query.count()
            if applications == 0:
                response = {'message': 'No applications found to generate placement statistics!!'}
                return make_response(jsonify(response), 200)
            else:
                applied_count = Application.query.filter_by(status='applied').count()
                selected_count = Application.query.filter_by(status='selected').count()
                rejected_count = Application.query.filter_by(status='rejected').count()

                plt.bar(['Applied', 'Selected', 'Rejected'], [applied_count, selected_count, rejected_count], color=['yellow', 'green', 'red'])
                plt.xlabel('Placement Stages')
                plt.ylabel('Number of Students')
                plt.title('Placement Statistics Overview')
                plt.tight_layout()
                os.makedirs(os.path.join('frontend', 'static', 'charts'), exist_ok=True)
                plt.savefig('./frontend/static/charts/placement_summary.png')
                plt.close()
                return { 'Graph' : 'placement_summary.png' }, 200
            
        elif showchartfor == 'drives':
            drives = PlacementDrive.query.count()
            if drives == 0:
                response = {'message': 'No placement drives found to generate drive statistics!!'}
                return make_response(jsonify(response), 200)
            else:
                companies  = Company.query.filter_by(status='approved').all()
                drive_counts = []
                company_names = []
                for company in companies:
                    drive_count = PlacementDrive.query.filter_by(company_id=company.company_id).count()
                    drive_counts.append(drive_count)
                    company_names.append(company.company_name)
                
                plt.bar(company_names, drive_counts, color='green')
                plt.xlabel('Companies')
                plt.ylabel('Number of Placement Drives')
                plt.title('Placement Drives per Company')
                plt.tight_layout()
                os.makedirs(os.path.join('frontend', 'static', 'charts'), exist_ok=True)
                plt.savefig('./frontend/static/charts/drive_summary.png')
                plt.close()
                return {'Graph' : 'drive_summary.png' }, 200





class AdminProfileAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        profile_info = {
            'name': user.username,
            'email': user.email
        }
        return make_response(jsonify(profile_info), 200)
    
    @jwt_required()
    def put(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'admin':
            response = {'message': 'You are not authorized !! Admin access required.'}
            return make_response(jsonify(response), 403)
        
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            response = {'message': 'Both name and email are required'}
            return make_response(jsonify(response), 400)
        
        emails = [user.email for user in User.query.filter(User.id != user.id).all()]
        if email in emails:
            response = {'message': 'Email already in use. Please try a different email!!'}
            return make_response(jsonify(response), 400)
        
        user.username = name
        user.email = email
        db.session.commit()
        cac.delete_memoized(AdminProfileAPI.get)
        response = {'message': 'Profile updated successfully'}
        return make_response(jsonify(response), 200)

#------------------------------------------- COMPANY APIS -------------------------------------------#

class CompanyDrivesAPI(Resource):
    @jwt_required()
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'company':
            response = {'message': 'You are not authorized !! Company access required.'}
            return make_response(jsonify(response), 403)
        
        company = Company.query.filter_by(user_id=user.id).first()
        if not company:
            response = {'message': 'Company profile not found!!'}
            return make_response(jsonify(response), 403)
        
        drives = PlacementDrive.query.filter_by(company_id=company.company_id).order_by(PlacementDrive.created_date.desc()).all()
        drives_list = []
        for drive in drives:
            drives_list.append({
                'id': drive.drive_id,
                'job_title': drive.job_title.upper(),
                'job_desc': drive.job_description,
                'eligible_branch': drive.eligible_branch.upper(),
                'eligible_cgpa': drive.eligible_cgpa,
                'eligible_year': drive.eligible_year,
                'app_deadline': drive.application_deadline,
                'status': drive.status.upper(),
                'created_date': drive.created_date
            })
        response = {'Drives': drives_list}
        return make_response(jsonify(response), 200)





class CompanyDriveDetailsAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self, id):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'company':
            response = {'message': 'You are not authorized !! Company access required.'}
            return make_response(jsonify(response), 403)
        
        drive = PlacementDrive.query.filter_by(drive_id=id).first()

        if not drive:
            response = {'message': 'Drive not found'}
            return make_response(jsonify(response), 404)
    
        company = Company.query.filter_by(company_id=drive.company_id).first()
        application_count = Application.query.filter_by(drive_id=drive.drive_id).count()
        drive_det = {
            'drive_id': drive.drive_id,
            'company_id': company.company_id if company else None,
            'company_name': company.company_name if company else None,
            'job_title': drive.job_title.upper(),
            'job_desc': drive.job_description,
            'eligible_branch': drive.eligible_branch.upper(),
            'eligible_cgpa': drive.eligible_cgpa,
            'eligible_year': drive.eligible_year,
            'deadline' : str(drive.application_deadline),
            'total_applications': application_count,
            'status' : drive.status.upper(), 
            'created_date' : str(drive.created_date)
        }    
        response = {'details': drive_det}
        return make_response(jsonify(response), 200)




class CompanyCloseDriveAPI(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'company':
            response = {'message': 'You are not authorized !! Company access required.'}
            return make_response(jsonify(response), 403)
        
        data = request.get_json()
        drive_id = data.get('id')

        if not drive_id:
            response = {'message': 'Drive ID required'}
            return make_response(jsonify(response), 400)

        drive = PlacementDrive.query.filter_by(drive_id=drive_id).first()

        if not drive:
            response = {'message': 'Drive not found'}
            return make_response(jsonify(response), 404)

        if drive.status=='approved':
            drive.status='closed'
            db.session.commit()
            response = {'message': 'Drive Closed successfully!!'}
            cac.delete_memoized(StudentAllDrivesAPI.get)
            cac.delete_memoized(StudentEligibleDrivesAPI.get)
            cac.delete_memoized(AdminPlacementDrivesAPI.get)
            return make_response(jsonify(response), 200)
        
        else:
            response = {'message': 'Cannot Close Pending or Rejected Drives!!'}
            return make_response(jsonify(response), 403)


        




class CompanyCreatePlacementDriveAPI(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'company':
            response = {'message': 'You are not authorized !! Company access required.'}
            return make_response(jsonify(response), 403)
        
        company = Company.query.filter_by(user_id=user.id).first()
        if not company:
            response = {'message': 'Company profile not found!!'}
            return make_response(jsonify(response), 403)
        
        if company.status != 'approved':
            response = {'message': 'Company is not yet approved by admin. Cannot create placement drive!!'}
            return make_response(jsonify(response), 403)
        
        data = request.get_json()
        if not data or not all([data.get('job_title'), data.get('job_description'),
                           data.get('eligible_branch'), data.get('eligible_cgpa'),
                           data.get('eligible_year'), data.get('application_deadline')]):
            response = {'message': 'Fill all the required fields'}
            return make_response(jsonify(response), 400)
        
        try:
            deadline = datetime.strptime(data.get('application_deadline'), '%Y-%m-%d').date()
            if deadline <= datetime.now().date():
                response = {'message': 'Invalid deadline!! Deadline should be in future'}
                return make_response(jsonify(response), 400)
        except ValueError:
            response = {'message': 'Invalid date format for application_deadline. Use YYYY-MM-DD'}
            return make_response(jsonify(response), 400)
        
        new_drive = PlacementDrive(
                    company_id = company.company_id,
                    job_title = data.get('job_title'),
                    job_description = data.get('job_description'),
                    eligible_branch = data.get('eligible_branch').lower(),
                    eligible_cgpa = float(data.get('eligible_cgpa')),
                    eligible_year = int(data.get('eligible_year')),
                    application_deadline = deadline
        )
        db.session.add(new_drive)
        db.session.commit()
        cac.delete_memoized(StudentEligibleDrivesAPI.get)
        cac.delete_memoized(StudentAllDrivesAPI.get)
        cac.delete_memoized(AdminCompaniesAPI.get)
        cac.delete_memoized(AdminPlacementDrivesAPI.get)

        response = {'message': 'Placement drive created successfully. Waiting for admin approval',
                    'drive_id': new_drive.drive_id,
                    'company_name': company.company_name,
                    'job_title': new_drive.job_title,
                    'status': new_drive.status}
        return make_response(jsonify(response), 201)





class CompanyStudentApplicationsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'company':
            response = {'message': 'You are not authorized !! Company access required.'}
            return make_response(jsonify(response), 403)
        
        company = Company.query.filter_by(user_id=user.id).first()
        if not company:
            response = {'message': 'Company profile not found!!'}
            return make_response(jsonify(response), 403)
        
        drives = PlacementDrive.query.filter(PlacementDrive.company_id == company.company_id, PlacementDrive.status != 'closed').all()
        application_list = []

        for drive in drives:
            applications  = Application.query.filter_by(drive_id=drive.drive_id).all()
            for application in applications:
                student = Student.query.filter_by(student_id=application.student_id).first()
                application_list.append({
                    'application_id' : application.application_id,
                    'drive_id' : application.drive_id,
                    'student_id' : application.student_id,
                    'student_name' : student.student_name, 
                    'student_branch' : student.branch.upper(),
                    'student_year' : student.year,
                    'student_cgpa' : student.cgpa,
                    'applied_date' : str(application.applied_date),
                    'status' : application.status.upper(),
                    'job_title': drive.job_title.upper(),
                    'job_desc': drive.job_description
                })
            
        response = {'Applications': application_list}
        return make_response(jsonify(response), 200)




class CompanyApplicationDetailsAPI(Resource):
    @jwt_required()
    def get(self, id):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'company':
            response = {'message': 'You are not authorized !! Company access required.'}
            return make_response(jsonify(response), 403)
        
        app = Application.query.filter_by(application_id=id).first()

        if not app:
            response = {'message': 'Application not found'}
            return make_response(jsonify(response), 404)

        student = Student.query.filter_by(student_id=app.student_id).first()
        drive = PlacementDrive.query.filter_by(drive_id=app.drive_id).first()
        details = {
            'application_id': app.application_id,
            'drive_id': app.drive_id,
            'job_title': drive.job_title.upper(),
            'student_id': app.student_id,
            'student_name': student.student_name,
            'branch': student.branch.upper(),
            'cgpa': student.cgpa,
            'year': student.year,
            'resume': student.resume_path,
            'applied_date': str(app.applied_date),
            'status': app.status.upper()
        }
        response = {'details': details}
        return make_response(jsonify(response), 200)
    




class CompanyUpdateApplicationStatusAPI(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'company':
            response = {'message': 'You are not authorized !! Company access required.'}
            return make_response(jsonify(response), 403) 

        data = request.get_json()
        application_id = data.get('id')
        if not data or not data.get('action'):
            response = {'message': 'Action required (/select/reject)'}
            return make_response(jsonify(response), 400)
    
        company = Company.query.filter_by(user_id=user.id).first()
        app = Application.query.filter_by(application_id=application_id).first()
    
        if not app:
            response = {'message': 'Application not found'}
            return make_response(jsonify(response), 404)
        
        drive = PlacementDrive.query.filter_by(drive_id=app.drive_id).first()

        if drive.company_id != company.company_id:
            response = {'message': 'You can only update Application status of Your drive!!'}
            return make_response(jsonify(response), 403)
        else:
            action = data.get('action').lower()
            if action == 'select':
                app.status = 'selected'
                message = 'Application selected successfully.'   
            elif action == 'reject':
                app.status = 'rejected'
                message = 'Application rejected successfully.' 
            else:
                return make_response(jsonify({'message': 'Invalid action. Use select or reject'}), 400)  

        db.session.commit()
        cac.delete_memoized(StudentEligibleDrivesAPI.get)
        cac.delete_memoized(AdminPlacementDrivesAPI.get)
        response = {'message': message}   
        return make_response(jsonify(response), 200)
    




class CompanyProfileAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'company':
            response = {'message': 'You are not authorized !! Company access required.'}
            return make_response(jsonify(response), 403) 
        
        company = Company.query.filter_by(user_id=user.id).first()
        profile_info = {
            'name': user.username,
            'email': user.email,
            'hr_contact': company.hr_contact
        }
        return make_response(jsonify(profile_info), 200)
    
    @jwt_required()
    def put(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'company':
            response = {'message': 'You are not authorized !! Company access required.'}
            return make_response(jsonify(response), 403)
        
        company = Company.query.filter_by(user_id=user.id).first()
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        hr_contact = data.get('hr_contact')

        if not name or not email or not hr_contact:
            response = {'message': 'Name and Email and hr_contact all three are required'}
            return make_response(jsonify(response), 400)
        
        emails = [user.email for user in User.query.filter(User.id != user.id).all()]
        if email in emails:
            response = {'message': 'Email already in use. Please try a different email!!'}
            return make_response(jsonify(response), 400)
        
        user.username = name
        user.email = email
        company.hr_contact = hr_contact
        db.session.commit()
        cac.delete_memoized(CompanyProfileAPI.get)
        response = {'message': 'Profile updated successfully'}
        return make_response(jsonify(response), 200)
    
#---------------------------------------------- STUDENT APIS --------------------------------------------#

class StudentAllDrivesAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'student':
            response = {'message': 'You are not authorized !! Student access required.'}
            return make_response(jsonify(response), 403)
        
        student = Student.query.filter_by(user_id=user.id).first()
        drives = PlacementDrive.query.filter(PlacementDrive.status == 'approved', PlacementDrive.application_deadline >= datetime.now().date()).order_by(PlacementDrive.drive_id.desc()).all()
        drives_list = []
        for drive in drives:
            company = Company.query.filter_by(company_id=drive.company_id).first()
            company_user = User.query.filter_by(id=company.user_id).first()

            application = Application.query.filter_by(drive_id=drive.drive_id, student_id=student.student_id).first()

            if application:
                applied = True
            else:
                applied = False
            
            if not company_user or company_user.is_blacklisted:
                continue

            drives_list.append({
                'drive_id': drive.drive_id,
                'company_id': company.company_id if company else None,
                'company_name': company.company_name if company else None,
                'job_title': drive.job_title.upper(),
                'job_description': drive.job_description,
                'eligible_branch': drive.eligible_branch.upper(),
                'eligible_cgpa': drive.eligible_cgpa,
                'eligible_year': drive.eligible_year,
                'application_deadline' : str(drive.application_deadline),
                'applied': applied
            })
        
        response = {'All_Placement_Drives': drives_list}
        return make_response(jsonify(response), 200)
    



class StudentDriveDetailsAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self, id):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'student':
            response = {'message': 'You are not authorized !! Student access required.'}
            return make_response(jsonify(response), 403)
        
        drive = PlacementDrive.query.filter_by(drive_id=id).first()

        if not drive:
            response = {'message': 'Drive not found'}
            return make_response(jsonify(response), 404)
        
        company = Company.query.filter_by(company_id=drive.company_id).first()
        application_count = Application.query.filter_by(drive_id=drive.drive_id).count()
        drive_det = {
            'drive_id': drive.drive_id,
            'company_id': company.company_id if company else None,
            'company_name': company.company_name if company else None,
            'job_title': drive.job_title.upper(),
            'job_desc': drive.job_description,
            'eligible_branch': drive.eligible_branch.upper(),
            'eligible_cgpa': drive.eligible_cgpa,
            'eligible_year': drive.eligible_year,
            'deadline' : str(drive.application_deadline),
            'total_applications': application_count,
            'status' : drive.status.upper(), 
            'created_date' : str(drive.created_date)
        }
    
        response = {'details': drive_det}
        return make_response(jsonify(response), 200)
    



    
class StudentApplyDriveAPI(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'student':
            response = {'message': 'You are not authorized !! Student access required.'}
            return make_response(jsonify(response), 403)
        
        student = Student.query.filter_by(user_id=user.id).first()
        if not student:
            response = {'message': 'Student profile not found!!'}
            return make_response(jsonify(response), 403)
        
        data = request.get_json()
        drive_id = data.get('id')

        if not drive_id:
            response = {'message': 'Drive ID required'}
            return make_response(jsonify(response), 400)

        drive = PlacementDrive.query.filter_by(drive_id=drive_id, status='approved').first()
        if not drive:
            response = {'message': 'Placement drive not found or not approved yet or closed!!'}
            return make_response(jsonify(response), 404)
        
        if drive.application_deadline < datetime.now().date():
            response = {'message': 'Application deadline is passed'}
            return make_response(jsonify(response), 403)
        
        existing_application = Application.query.filter_by(student_id=student.student_id, drive_id=drive_id).first()
        if existing_application:
            response = {'message': f'You have already Applied for the drive. Your application status is {str.upper(existing_application.status)}'}
            return make_response(jsonify(response), 409)
        
        
        if float(student.cgpa) < float(drive.eligible_cgpa) or int(student.year) < int(drive.eligible_year) or student.branch.lower() != drive.eligible_branch.lower():
            response = {'message': 'You are not eligible to apply for this drive!!'}
            return make_response(jsonify(response), 403)
        
        
        new_application = Application(
            student_id = student.student_id,
            drive_id = drive.drive_id
        )
        db.session.add(new_application)
        db.session.commit()
        cac.delete_memoized(StudentEligibleDrivesAPI.get)
        cac.delete_memoized(StudentAllDrivesAPI.get)
        response = {'message': 'Application submitted successfully!!',
                    'application_id': new_application.application_id,
                    'drive_id': drive.drive_id,
                    'job_title': drive.job_title,
                    'status': new_application.status}
        return make_response(jsonify(response), 201)
  



class StudentEligibleDrivesAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'student':
            response = {'message': 'You are not authorized !! Student access required.'}
            return make_response(jsonify(response), 403)

        student = Student.query.filter_by(user_id=user.id).first()

        if not student:
            response = {'message': 'Student profile not found!!'}
            return make_response(jsonify(response), 403)

        drives = PlacementDrive.query.filter(PlacementDrive.status == 'approved', PlacementDrive.application_deadline >= datetime.now().date()).order_by(PlacementDrive.drive_id.desc()).all()

        eligible_drives = []

        for drive in drives:
            company = Company.query.filter_by(company_id=drive.company_id).first()
            company_user = User.query.filter_by(id=company.user_id).first()
            application = Application.query.filter_by(drive_id=drive.drive_id, student_id=student.student_id).first()

            if application:
                applied = True
            else:
                applied = False

            if not company_user or company_user.is_blacklisted:
                continue

            if (
                float(student.cgpa) >= float(drive.eligible_cgpa) and
                int(student.year) >= int(drive.eligible_year) and
                student.branch.strip().lower() == drive.eligible_branch.strip().lower()
            ):

                eligible_drives.append({
                    'drive_id': drive.drive_id,
                    'company_name': company.company_name if company else None,
                    'job_title': drive.job_title.upper(),
                    'job_description': drive.job_description,
                    'eligible_branch': drive.eligible_branch.upper(),
                    'eligible_cgpa': drive.eligible_cgpa,
                    'eligible_year': drive.eligible_year,
                    'application_deadline' : str(drive.application_deadline),
                    'applied': applied
                })
        
        response = {'eligible_drives': eligible_drives}
        return make_response(jsonify(response), 200)





class StudentApplicationHistoryAPI(Resource):
    @jwt_required()
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'student':
            response = {'message': 'You are not authorized !! Student access required.'}
            return make_response(jsonify(response), 403)
        
        student = Student.query.filter_by(user_id=user.id).first()
        if not student:
            response = {'message': 'Student profile not found!!'}
            return make_response(jsonify(response), 403)
        
        applications = Application.query.filter_by(student_id=student.student_id).order_by(Application.application_id.desc()).all()
        applications_list = []
        for application in applications:
            drive_id = application.drive_id
            drive = PlacementDrive.query.filter_by(drive_id=drive_id).first()
            if not drive:
                continue
            company = Company.query.filter_by(company_id=drive.company_id).first()
            applications_list.append({
                'application_id': application.application_id,
                'drive_id': application.drive_id,
                'company_name': company.company_name if company else None,
                'job_title': drive.job_title.upper(),
                'applied_date': application.applied_date.strftime('%Y-%m-%d'),
                'status': application.status.upper()
            })
        response = {'Application_History': applications_list}
        return make_response(jsonify(response), 200)




class StudentExportApplicationsAPI(Resource):

    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'student':
            response = {'message': 'You are not authorized !! Student access required.'}
            return make_response(jsonify(response), 403)

        student = Student.query.filter_by(user_id=user.id).first()

        if not student:
            return make_response(jsonify({'message': 'Student profile not found'}), 404)

        application_csv.delay(student.student_id)

        return make_response(jsonify({
            'message': 'CSV export started. You will be notified once completed.'
        }), 200)





class StudentProfileAPI(Resource):
    @jwt_required()
    @cac.memoize(timeout=300)
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'student':
            response = {'message': 'You are not authorized !! Student access required.'}
            return make_response(jsonify(response), 403) 
        
        student = Student.query.filter_by(user_id=user.id).first()
        profile_info = {
            'name': user.username,
            'email': user.email,
            'branch': student.branch,
            'year': student.year,
            'cgpa': student.cgpa,
            'resume': student.resume_path
        }
        return make_response(jsonify(profile_info), 200)
    
    @jwt_required()
    def put(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.role != 'student':
            response = {'message': 'You are not authorized !! Student access required.'}
            return make_response(jsonify(response), 403)
        
        student = Student.query.filter_by(user_id=user.id).first()
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        branch = data.get('branch')
        year = data.get('year')
        cgpa  = data.get('cgpa')
        resume = data.get('resume')
        
        emails = [user.email for user in User.query.filter(User.id != user.id).all()]
        if email in emails:
            response = {'message': 'Email already in use. Please try a different email!!'}
            return make_response(jsonify(response), 400)
        
        user.username = name
        user.email = email
        student.branch = branch
        student.year = year
        student.cgpa = cgpa
        student.resume_path = resume
        db.session.commit()
        cac.delete_memoized(StudentProfileAPI.get)
        cac.delete_memoized(StudentEligibleDrivesAPI.get)
        cac.delete_memoized(StudentAllDrivesAPI.get)
        response = {'message': 'Profile updated successfully'}
        return make_response(jsonify(response), 200)
    
#--------------------------------------------- LOGOUT API --------------------------------------------#

class LogOutAPI(Resource):
    @jwt_required()
    def post(self):
        response = {'message': 'Logged out successfully'}
        return make_response(jsonify(response), 200)

