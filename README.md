
### Real-Time Monitoring Web Application

This Flask-based web application enables real-time monitoring of various environmental parameters and provides visual feedback through a user-friendly interface. The application interacts with a Firebase backend to fetch and display data.

#### Features:
- **Real-Time Data Monitoring**: Fetches and displays real-time data from a Firebase database.
- **Image Display**: Retrieves the latest image stored in Firebase Storage and displays it on the web interface.
- **Temperature Monitoring**: Fetches temperature readings and displays them on the dashboard.
- **Humidity Monitoring**: Fetches humidity readings and displays them on the dashboard.
- **Gas Status Display**: Fetches gas status readings and displays them on the dashboard.
- **Gyroscope Status Display**: Fetches gyroscope readings and displays them on the dashboard.
- **Image Timestamp Display**: Fetches the timestamp of the latest image and displays it on the dashboard.

#### Technologies Used:
- **Flask**: A micro web framework for Python used to build the web application.
- **Pyrebase**: Python wrapper for the Firebase API used for interfacing with Firebase services.
- **Firebase Realtime Database**: Cloud-hosted NoSQL database provided by Google Firebase, used to store real-time data.
- **Firebase Storage**: Cloud storage provided by Google Firebase, used to store images.
- **HTML Templates**: Jinja2 templates for rendering dynamic HTML content on the web interface.
- **CSS**: Styling to enhance the visual presentation of the web interface.

#### Installation and Setup:
1. Clone or download the repository containing the Flask application code.
2. Ensure you have Python installed on your system.
3. Install dependencies using pip:
   ```
   pip install -r Requirements.txt
   ```
4. Modify the `firebaseConfig` dictionary in the code with your Firebase project's configuration.
5. Run the Flask application using the command:
   ```
   python main.py
   ```
6. Access the application through a web browser by navigating to `http://localhost:5000/`.

#### Usage:
- Upon accessing the web application, you will be presented with a dashboard displaying real-time data.
- The dashboard includes sections for image display, temperature monitoring, humidity monitoring, gas status display, gyroscope status display, and image timestamp display.
- The latest image stored in Firebase Storage is displayed on the dashboard.
- Temperature, humidity, gas status, gyroscope status, and image timestamp data are fetched from the Firebase Realtime Database and displayed dynamically on the dashboard.
- Data is updated in real-time without requiring page refreshes.

#### Contributors:
- [Adule Solomon -(https://github.com/solkiona)]
- [Mba Chibueze -(https://github.com/mbachibueze)]


#### Support and Contact:
[For further inquiries kindly reachout via email at <a href="mailto:solkiona@gmail.com">solkiona@gmail.com</a>]

By following these steps, you will be able to set up and run the Real-Time Monitoring Web Application on your local machine. If you encounter any issues or have any questions, feel free to reach out for support.