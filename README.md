# SlideCraft

SlideCraft is a web application built using **Flask, Python, HTML, CSS, and JavaScript** that allows users to create customized slideshow videos. Users can upload images, set the display duration for each image, choose transitions, add background music, and generate a final video seamlessly.

## ✨ Features

-  **Image Upload**: Users can upload multiple images to create a slideshow.
-  **Custom Duration**: Select the time duration for each image in the video.
-  **Transitions**: Choose from various transition effects between images.
-  **Background Music**: Upload an audio file to be played in the video.
-  **Video Generation**: Combines selected images, transitions, and music into a single video file.
-  **User Authentication**: Secure login and session management (if applicable).


## 🎥 Demo Run

You can check out a live demo of SlideCraft here:
[🔗 Demo Link](https://iiithydstudents-my.sharepoint.com/:v:/g/personal/virat_garg_students_iiit_ac_in/EXRGWzG6InVMnukfDIlKYi4BBPgK2OxT8IxchGdA4r-lrw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=qwQ6E9) (Replace with actual link when available)

## 🛠 Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL (for storing user data and uploaded files path)
- **Media Processing**: FFmpeg (for video and audio processing)

## 🚀 Installation

### Prerequisites
Ensure you have the following installed:
-  Python 3.x
-  Flask
-  FFmpeg
-  PostgreSQL

### Steps to Run the Project

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/slidecraft.git
   cd slidecraft
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables (if needed):
   ```sh
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

5. Run the Flask application:
   ```sh
   flask run
   ```

6. Open your browser and visit:
   ```
   http://127.0.0.1:5000/
   ```

