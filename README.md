#  Django Authentication and IP Address Tracking

A Django web application for user authentication and IP Address Tracking

##  Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)


## Description
This Django project provides user authentication features and IP tracking functionalities. Users can register, login and logout. In this project, the IP addresses re tracked, and various flags are set based on different actions like:
a. Registry changes
b. Sub-Process Analysis
c. Footprints


## features
- User Authentication (Register, Login, Logout)
- IP Tracking
  - Autoflagging IPs
  - Setting Public Flags for IPs
  - Setting Authentication Flags for IPs
  - Retrieving Flags for IPs
  - Checking if an IP exists

## Installation
 
  - Python setup

  - Create a virtual environment

  - Activate the virtual environment
       source venv/bin/activate  # On macOS/Linux
       venv\Scripts\activate     # On Windows
  - Install dependencies
     # pip install requirements.txt

  - Apply migrations
     python manage.py makemigrations
     python manage.py migrate

  - Run the development server
     python manage.py runserver

## User Authentication

  - Visit the index.html as home page.

  - After that visit register page at http://127.0.0.1:8000/register/  to create a new account

  - Then after registration, you cam log in at http://127.0.0.1:8000/login/ with your credentials.

  -Once logged in, you will be redirected to the home page at  http://127.0.0.1:8000/ where your username is displayed.

  - You can log out by visiting http://127.0.0.1:8000/logout/.

## Ip Address Tracking

  - Visit the report page at http://127.0.0.1:8000/report/ to view and interact with IP tracking features.

  - Explore the different functionalities such as autoflagging IPs, setting public flags, setting authentication flags, retrieving flags, and   checking if an IP exists.

## Contributions

  - If you'd like to contribute to the project, please follow the guidelines in the CONTRIBUTING.md file.

## License
   - Review the license details in the LICENSE file.


  



  






