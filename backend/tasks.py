from backend.worker import celery
from celery.schedules import crontab
from backend.models import *
from backend.mailer import send_mail, send_admin_mail
from datetime import datetime, timedelta
import csv
import os


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour=9, minute=00),
        send_daily_reminder.s(),
    )

    sender.add_periodic_task(
        crontab(hour=10, minute=0, day_of_month=1),
        monthly_report.s(),
    )


@celery.task
def send_daily_reminder():

    users = User.query.filter_by(is_blacklisted=False, role='student').all()
    drives = PlacementDrive.query.filter_by(status='approved').all()

    current_date = datetime.now().date()

    drive_list = []

    for drive in drives:
        company = Company.query.filter_by(company_id=drive.company_id).first()
        company_user = User.query.filter_by(id=company.user_id).first()
            
        if not company_user or company_user.is_blacklisted:
            continue
        
        if current_date <= drive.application_deadline <= current_date + timedelta(days=2):
            drive_list.append({
                'drive_id': drive.drive_id,
                'company_name': company.company_name if company else None,
                'job_title': drive.job_title,
                'application_deadline': str(drive.application_deadline)
            })

    if not drive_list or len(drive_list) == 0:
        for user in users:
            subject = "Reminder: Upcoming Drive Deadlines"

            message = f"<h3>Hello {user.username},</h3>"
            message += "<p>No Drives are closing within the next 2 days. But one must apply early to achieve success!!</p>"

            for drive in drive_list:
                message += f"""
                <p>
                Drive ID: {drive['drive_id']}<br>
                Company: {drive['company_name']}<br>
                Role: {drive['job_title']}<br>
                Deadline: {drive['application_deadline']}
                </p>
                <hr>
                """

            send_mail(user.email, subject, message)

    else:
        for user in users:
            subject = "Reminder: Upcoming Drive Deadlines"

            message = f"<h3>Hello {user.username},</h3>"
            message += "<p>These Drives are closing within 2 days!! Apply now!!</p>"

            for drive in drive_list:
                message += f"""
                <p>
                Drive ID: {drive['drive_id']}<br>
                Company: {drive['company_name']}<br>
                Role: {drive['job_title']}<br>
                Deadline: {drive['application_deadline']}
                </p>
                <hr>
                """

            send_mail(user.email, subject, message)

    return "Reminder sent successfully"

        



@celery.task
def monthly_report():

    today = datetime.now().date()

    first_day_current_month = today.replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)

    pm_drives_count = PlacementDrive.query.filter(
        PlacementDrive.created_date >= first_day_previous_month,
        PlacementDrive.created_date <= last_day_previous_month
    ).count()

    pm_applications_count = Application.query.filter(
        Application.applied_date >= first_day_previous_month,
        Application.applied_date <= last_day_previous_month
    ).count()

    pm_selected_count = Application.query.filter(
        Application.status == 'selected',
        Application.applied_date >= first_day_previous_month,
        Application.applied_date <= last_day_previous_month
    ).count()

    pm_rejected_count = Application.query.filter(
        Application.status == 'rejected',
        Application.applied_date >= first_day_previous_month,
        Application.applied_date <= last_day_previous_month
    ).count()


    cm_drives_count = PlacementDrive.query.filter(
        PlacementDrive.created_date >= first_day_current_month,
        PlacementDrive.created_date <= today
    ).count()

    cm_applications_count = Application.query.filter(
        Application.applied_date >= first_day_current_month,
        Application.applied_date <= today
    ).count()

    cm_selected_count = Application.query.filter(
        Application.status == 'selected',
        Application.applied_date >= first_day_current_month,
        Application.applied_date <= today
    ).count()

    cm_rejected_count = Application.query.filter(
        Application.status == 'rejected',
        Application.applied_date >= first_day_current_month,
        Application.applied_date <= today
    ).count()

 
    html_message = f"""
    <h2>Monthly Placement Report</h2>

    <p>
    <strong>Previous Month Report</strong>  
    [ Period: {first_day_previous_month} to {last_day_previous_month} ]
    </p>

    <ul>
        <li>Total Drives Conducted: {pm_drives_count}</li>
        <li>Total Applications Submitted: {pm_applications_count}</li>
        <li>Total Students Selected: {pm_selected_count}</li>
        <li>Total Students Rejected: {pm_rejected_count}</li>
    </ul>

    <p>
    <strong>Current Month Report</strong>
    [ Period: {first_day_current_month} to {today} ] 
    </p>
    

    <ul>
        <li>Total Drives Conducted: {cm_drives_count}</li>
        <li>Total Applications Submitted: {cm_applications_count}</li>
        <li>Total Students Selected: {cm_selected_count}</li>
        <li>Total Students Rejected: {cm_rejected_count}</li>
    </ul>

    <p>Report generated by Placement Portal System.</p>
    """

    send_admin_mail(html_message)
    return "Monthly report sent successfully"
   




@celery.task
def application_csv(student_id):

    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return "Student not found"

    user = User.query.filter_by(id=student.user_id).first()

    if user.is_blacklisted:
        return "User is blacklisted!! Can't download application history"

    applications = Application.query.filter_by(student_id=student_id).all()

    filename = f"student_{student_id}_applications.csv"
    filepath = os.path.join("exports", filename)

    os.makedirs("exports", exist_ok=True)

    with open(filepath, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Drive ID",
            "Company Name",
            "Job Title",
            "Student ID",
            "Application Status",
            "Applied Date"
        ])

        for application in applications:
            drive = PlacementDrive.query.filter_by(
                drive_id=application.drive_id
            ).first()

            if not drive:
                continue

            company = Company.query.filter_by(
                company_id=drive.company_id
            ).first()

            writer.writerow([
                drive.drive_id,
                company.company_name if company else "N/A",
                drive.job_title,
                application.student_id,
                application.status,
                str(application.applied_date)
            ])
    
    download_link = f"http://localhost:5000/download_csv/{filename}"

    if not applications or len(applications) == 0:
        subject = "Placement Applications Export Ready"

        message = f"""
        <h3>Hello {student.student_name}</h3>
        <p>Your placement application history CSV has been generated. But no applications found. Please apply for a drive first!!</p>
        <p>Click below to download:</p>
        <a href="{download_link}">Download CSV</a>
        """

        send_mail(user.email, subject, message)

    else:
        subject = "Placement Applications Export Ready"

        message = f"""
        <h3>Hello {student.student_name}</h3>
        <p>Your placement application history CSV has been generated.</p>
        <p>Click below to download:</p>
        <a href="{download_link}">Download CSV</a>
        """

        send_mail(user.email, subject, message)
    return "CSV Export Completed"