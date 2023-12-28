# Django Authentication and IP Address Tracking

A Django web application for user authentication and IP Address Tracking

## Table of Contents

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

1. Clone the repository:

   ```bash
   git clone https://github.com/EV-OD/tcp_backend.git
   cd tcp_backend

   ```

2. Install npm dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ./automate
   ```

## Usage

1.  User Authentication

    - Visit the index.html as home page. http://127.0.0.1:8000/

    - After that visit register page at http://127.0.0.1:8000/register/ to create a new account

    - Then after registration, you cam log in at http://127.0.0.1:8000/login/ with your credentials.

    - Once logged in, you will be redirected to the home page at http://127.0.0.1:8000/ where your username is displayed.

    - You can log out by visiting http://127.0.0.1:8000/logout/.

    - You can check and report IP

2)  Data Visialization

    - Visit page at http://127.0.0.1:8000/ to view realtime process.

3)  Notifier and Connections Observer
    - It will notify you when there is new process analysis which is flagged.
    - User can watch the in more detail and also kill it

## License

- Review the license details in the LICENSE file.
