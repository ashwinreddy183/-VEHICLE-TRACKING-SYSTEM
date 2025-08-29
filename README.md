
# Vehicle Tracking System
The Vehicle Tracking System is a Django-based web application designed to track and manage various transport vehicles, including buses and e-rickshaws. It integrates real-time location tracking using Folium maps and provides different login options for users, service providers (bus conductors and rickshaw drivers), and administrators. The system also utilizes Outlook email integration for user notifications.

## Getting Started

### Prerequisites

- Ensure you have Python installed. If not, download and install it from [python.org](https://www.python.org/).
- Clone the repository and download the files to your desired folder.

### Installation

1. Open Command Prompt and navigate to the project directory:
    ```bash
    cd C:\Users\chara\Documents\Python  # Replace with your directory
    ```
2. Create a virtual environment:
    ```bash
    py -m venv env_name
    ```
3. Activate the virtual environment:
    ```bash
    env_name\scripts\activate.bat
    ```
4. Install the required dependencies:
    ```bash
    pip install django folium six
    ```

### Configuration

1. Create an Outlook email account and enable the POP and IMAP section in the sync mail settings.
2. Update the `info.py` file with your Outlook email credentials by replacing `sample@outlook.com` and `password`.

### Running the Application

1. Run the development server:
    ```bash
    python manage.py runserver
    ```
2. A link will be displayed in the command prompt. Copy this link and paste it into your browser.

### Usage

#### Home Page

- The home page provides three login options:
  - User Login (Get Started button)
  - Admin Login
  - Service Provider Login (Bus conductors and rickshaw drivers)

#### User Login

1. Click the Get Started button.
2. Click the Signup button to be redirected to the signup page.
3. Register using your IITG email. An activation link will be sent to your email.
4. Click the activation link in the email to be redirected back to the home page. You are now successfully logged in.
5. Select your preferred vehicle to view its details.

#### Service Provider Login

1. Open a new tab and open the index page.
2. Click on the Service Provider Login.
3. Select "Bus" and use the following (default)credentials:
    - **Bus_id:** bus_service
    - **Password:** bus_1234
4. Enter the vehicle details:
    - **Bus Number:** AP1234(example)
    - Enter any two places as start and end locations.
6. A page will display the Bus Number and a box to update the number of vacancies. Provide location access and wait for approximately 5-10 seconds to fetch coordinates. These coordinates will be updated in the bus database.
7. Refresh the bus information page of the user side to see updated coordinates and the bus status changed to "running". The red marker is your location, and the blue marker is the bus location.

#### E-Rickshaw

- Follow similar steps as above for E-Rickshaw.
- E-Rickshaw (default)credentials:
    - **Rickshaw_number:** AR1234
    - **Vehicle_key:** AR1234pass
- Here we have option to update the number of pre-bookings.

#### Admin Login

- Admin login credentials:
    - **Username:** admin
    - **Password:** admin12345
Certainly! Here's the updated "Future Improvements" section including the additional point about IITG bus passes:

---

## Future Improvements

- **Google Maps Integration**: Integrate Google Maps to display distance and estimated travel time based on real-time traffic conditions.
  
- **Deployment**: Deploy the application to a cloud platform (e.g., Heroku, AWS) for public access and scalability.
  
- **Additional Transport Options**: Expand tracking capabilities to include other transport modes such as ferry and cab services.
  
- **IITG Bus Pass Integration**: Implement integration with IITG bus passes to streamline entry procedures, reducing the need for manual checks every time someone enters IITG premises.

