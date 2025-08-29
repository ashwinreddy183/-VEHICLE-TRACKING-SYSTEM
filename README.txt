1) Download the ZIP file and unzip it to a specific folder.
2) Open command prompt and change directory to that folder.
      Use following command:
		"cd C:\Users\chara\Documents\Python" (replace directory with your directory)
3)Create a virtual environment using following command:
		"py -m venv env_name"
4)Activate environment:
		"env_name\scripts\activate.bat"
5)Install all the dependencies:
		"pip install django"
		"pip install folium"
		"pip install six"

5.5) Create an outlook mail and enable POP and IMAP section of sync mail in settings. Use credentials of your mail in info.py file by replacing sample@outlook.com and password
6)Run following command to run website:
		"python manage.py runserver"

7)And link will be displayed in command prompt.Copy the link the given link and paste in your browser

8)Home page will be opened. Three login options will be there.
        User login (Get started button)
	Admin login
	Service Provider Login(Bus conductors and rickshaw drivers)
9)Open user login and you will see signup button. Click that you will be redirected to signup page.
10)Use your IITG mail to register. A mail will be sent to your IITG email address. A link for atcivation will be sent to you.
11)Copy that link and paste in your browser. You will be redirected to home page. You are succesfully logged in. Now again click on get started button.
12)You will see two options. Bus and AutoRickshaw. Select on BUS.
13)All the bus details will be displayed. All the bus status is displayed as Halted because no conductor has logged in for the coordinates to update.
14)Now open a new tab using link from STEP 7. Click on service provider login.
15) Select Bus. Credentials are as follows.(I have hard coded credentials of bus workers)
         Bus_id : bus_service    Password: bus_1234
16) Now you should enter to which vehicle you are responsible. Use following credentials.
	Bus Number: AP1234
	Enter any two places as start and end
17) A page will open displaying Bus Number and a box to to update number of vacancies. Give location access and wait for some time (apprx. 5s-10s) to fetch coordinates.These coordinates will be updated to bus database.
18)Now open the page containing bus information in a table in STEP 13. Refresh the page to see updated coordinates and status of bus changed to running. Click on generate map and then click on view map. A map will pop up having two markers. Red marker is your location and blue is bus location. But in this case as project is not deployed , both markers will be at same location.
19) Do similar steps for E-rickshaw.
20) E-Rickshaw credentials:
		Rickshaw_number : AR1234
		Vehicle_key : AR1234pass
21) ADMIN login credentials:
	username:admin
	password:admin12345


