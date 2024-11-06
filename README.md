# Cinema Ticket QR

## Project Breakdown

The "Cinema Ticket" project involves developing a backend system that provides services to movie projection businesses, specifically cinemas. Through "Cinema Ticket," the business should enable its customers to purchase tickets for a movie projection online.

## Features
- Models movie, projection, cinema room, ticket CRUD
- Send ticket by mail
- QR on ticket to validate
- payment gateways not * implmented yet

## Dependencies

- Python 3.12
- [Docker](https://docs.docker.com/get-started/) >= 23

## Install Locally

To install and run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GatMaximoAr/cinema-web.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd cinema-ticket
   ```
3. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

6. **Run the test suite (Optional):**
   ```bash
   pytest -v
   ```


7. **Create a superuser**
   ```bash
   python manage.py createsuperuser --username=joe --email=joe@example.com
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver --settings=cinema.settings.local
   ```

9. **Start a local SMTP service**
   ```bash
   docker run --rm -p 1080:1080 -p 1025:1025 marlonb/mailcrab:latest
   ```

10. **Access the project:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Technology Stack

- **Programming Language:** Python 3.12
- **Framework:** Django 5
- **REST Plugin:** Django Rest Framework (DRF)
- **Testing Framework:** Pytest
- **Database:** MySQL
- **Storage:** To be determined
- **QR Implementation:** qrcode + pillow
- **Payment Gateways:** To be determined

### Development Tools

- **Version Control:** Git
- **Repository Hosting:** GitHub
- **Rest API Client Extension** [Thunder Client](https://docs.thunderclient.com/)