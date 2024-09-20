# Services Django Project

Welcome to the Services Django Project! This project provides a platform for companies and customers to connect, offering various services in a user-friendly interface. This README will guide you through the setup and running of the project.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [License](#license)

## Features
- User registration for companies and customers.
- Dynamic profile pages with service offerings.
- Customer service request management.
- Simple and intuitive design using HTML, CSS, and JavaScript.

## Technologies Used
- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (configurable)
- **Styling:** Tailwind CSS (optional)
- **Version Control:** Git

## Setup Instructions

Follow these steps to set up the project on your local machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Raymond9734/Netfix.git
   cd Netfix

2. **Run the Setup Script:**

Make the setup.sh script executable:
```sh
chmod +x setup.sh
```
Execute the script once to create the virtual environment, install dependencies, and set up your project:
```sh
./setup.sh
```
## Running the Project
After completing the setup, you can start the Django development server if its not running yet after the setup:
```sh
python manage.py runserver
```
The server will start running at http://127.0.0.1:8000/. You can access the application in your web browser.

## Usage
**Register as a Company or Customer:** Navigate to the registration page to create an account.
**Profile Management:** Once logged in, you can manage your profile, services, and requests.
**Service Requests:** Customers can request services, which are handled by registered companies.
## License
This project is licensed under the MIT License. See the LICENSE file for details.