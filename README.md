# COVID-19 Hospital Management System

A Django-based web application designed to manage hospital operations during the COVID-19 pandemic. This system facilitates efficient management of patients, beds, and doctors, helping healthcare providers track patient symptoms, assign beds, and manage doctor visits.

## Features

- Patient Management: Add and manage patient details including contact information, symptoms, prior ailments, assigned bed, doctor, and status.
- Bed Management: Track bed availability and occupancy status.
- Doctor Management: Manage doctor information and assign doctors to patients.
- Symptom Tracking: Multi-select symptom tracking for patients to monitor COVID-19 related symptoms.
- User-friendly interface with templates for patient lists, dashboards, and login.

## Tech Stack

- Frontend:
  - HTML5
  - CSS3
  - jQuery
  - Bootstrap 4
- Backend:
  - Django 3.1
  - django-filter
  - django-multiselectfield
- Database:
  - SQLite
- Deployment:
  - Gunicorn
  - Whitenoise
- Other:
  - Python packages as listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd COVID-19 Hospital Management Python Django-1
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and go to:
   ```
   http://127.0.0.1:8000/
   ```

## Usage

- Use the web interface to add and manage patients, beds, and doctors.
- Login functionality is available to secure access.
- Dashboard provides an overview of hospital status.

## Screenshots

Screenshots of the application interface can be found in the `Screenshots/` directory, showcasing various features such as the dashboard, patient list, and login pages.

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Contributing

Please refer to the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidelines on contributing to this project.

---

This README is designed to be ATS (Applicant Tracking System) friendly with clear headings and structured content for easy parsing.
