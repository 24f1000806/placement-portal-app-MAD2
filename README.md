# Placement Portal Web Application - V2

Institutes require efficient systems to manage campus recruitment activities involving companies and students. Currently, many institutes rely on spreadsheets, emails, or manual coordination, which makes it difficult to manage company approvals, placement drives, student registrations, and application tracking.

This project develops a **multi-user Placement Portal Web Application (PPA)** that facilitates seamless interaction between **Admin (Institute)**, **Companies**, and **Students**, providing a centralized system to manage the entire recruitment lifecycle.

---

## ✨ Features

### 👨‍💼 Admin (Institute Placement Cell)
- Manages and approves company registrations and placement drives.
- Views and manages all students, companies, and placement drives.
- Can search for students or companies.
- Can blacklist or deactivate companies and students.
- Views reports and placement statistics.

### 🏢 Company
- Registers company profile on the platform.
- Creates placement drives (after admin approval).
- Views student applications for their drives.
- Shortlists students and updates application status.
- Schedules interviews and updates final selection results.

### 🎓 Student
- Registers, logs in, and updates profile.
- Views approved placement drives (with eligibility-based filtering/searching).
- Applies for placement exams/drives.
- Views application status and placement history.
- Edits profile and uploads resume.

### 📊 System Functionalities
- **Application Tracking & Status Updates**: Dynamic updates for application statuses.
- **Placement History Management**: Maintains complete placement history for each student.
- **Automated Reminders & Reports**: Scheduled jobs for daily reminders and monthly activity reports.
- **User Triggered Async Jobs**: Export applications as CSV.
- **Performance & Caching**: Caching implemented for improved performance and optimized API response times.
- **Role-based Access Control**: Secure login/register functionality for students and companies, and admin login only.

---

## ⚙️ Steps to Run the Application

### 0️⃣ Initial Setup

1.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    ```
2.  **Activate the Virtual Environment**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### 1️⃣ Start Redis Server
Open a new WSL terminal and run:
```bash
redis-server
```

### 2️⃣ Run the Backend
```bash
python app.py
```

### 3️⃣ Start the Frontend
Open a new terminal
```bash
cd frontend
npm install
npm run dev
```

### 4️⃣ Start Background Jobs
Open two **separate** terminals for these commands:
*   **Terminal 1 (Celery Worker):**
    ```bash
    python -m celery -A app.celery worker --pool=solo --loglevel=info
    ```
*   **Terminal 2 (Celery Beat):**
    ```bash
    python -m celery -A app.celery beat --loglevel=info
    ```

### 5️⃣ Start Mail Server
Download [MailHog](https://github.com/mailhog/MailHog/releases) and place it in the project folder.
Then run in a new terminal
```bash
./MailHog
```

To stop the application, press `CTRL + C` in all terminals. Then deactivate the Virtual Environment (if used) by running `deactivate`.