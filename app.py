import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for, jsonify
import  jwt
import datetime
import os
from werkzeug.utils import secure_filename
import cv2
import subprocess
import math
from flask import session
from flask import send_from_directory
import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageSequenceClip, ImageClip, AudioFileClip
from PIL import Image
import numpy as np
from moviepy.video.fx import all as vfx
from moviepy.editor import VideoFileClip
from flask import Flask, render_template, request, redirect, url_for, send_file


def connect_to_database():
    conn_params = {
        'host': 'slidecraft-4426.g95.gcp-us-west2.cockroachlabs.cloud',
        'port': 26257,
        'user': 'khwaish',   
        'password': 'vcgRLrp1-4aFAia-eYYx1A',
        'database': 'sys',
        'sslmode': 'verify-full',
        'sslrootcert': 'root.crt'
    }

    conn_str = "host={host} port={port} user={user} password={password} dbname={database} sslmode={sslmode} sslrootcert={sslrootcert}".format(**conn_params)

    # Connect to the database
    try:
        conn = psycopg2.connect(conn_str)
        print("Successfully connected to database")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        
        # Check if the root.crt file exists
        if not os.path.exists('root.crt'):
            print("Error: root.crt file not found")
            
        return None

def set_username(username):
    session['username'] = username

def get_username():
    return session.get('username', None)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

url = 'postgresql://khwaish:vcgRLrp1-4aFAia-eYYx1A@slidecraft-4426.g95.gcp-us-west2.cockroachlabs.cloud:26257/sys?sslmode=verify-full'

def create_tables():
    try:
        conn = connect_to_database()
        if conn is None:
            print("Error: Could not connect to database")
            return
        
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_login (id SERIAL PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), name VARCHAR(255), dob DATE);")
        cursor.execute("CREATE TABLE IF NOT EXISTS uploaded_images (id SERIAL PRIMARY KEY, Duration INT, name VARCHAR(255), path VARCHAR(255), size INT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS audio_files (id SERIAL PRIMARY KEY, file_name VARCHAR(255), file_path VARCHAR(255))")
        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print("Error creating tables:", e)

create_tables()


def fetch_user_details():
    try:
        conn = connect_to_database()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT id, username, name, dob FROM user_login")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    except psycopg2.Error as e:
        print("Error fetching user details:", e)
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_submit():
    username = request.form['username']
    password = request.form['password']
    name = request.form['name'] 
    dob = request.form['dob']   

    try:
        conn = connect_to_database()
        if conn is None:
            return 'Error connecting to database. Please try again.'
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_login WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            conn.close()
            return 'Username already exists. Please choose a different one.'
        else:
            cursor.execute("INSERT INTO user_login(username, password, name, dob) VALUES (%s, %s, %s, %s)", (username, password, name, dob))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
    except psycopg2.Error as e:
        print("Error signing up:", e)
        return 'Error signing up. Please try again.'


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_handler', methods=['POST'])
def login_submit():
    data = request.json
    if data is None:
        return jsonify({'message': 'JSON data not found'}), 400
    
    username = data.get('username')
    password = data.get('password')
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_login WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            set_username(username)
            token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            cursor.close()
            conn.close()
            return jsonify({'message': 'successful', 'token': token})
        else:
            return jsonify({'message': 'Invalid username or password. Please sign up first.'})
    except psycopg2.Error as e:
        print("Error logging in:", e)
        return jsonify({'message': 'Error logging in. Please try again.'})

@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    files = request.files.getlist('files[]')

    if not files:
        return jsonify({'message': 'No selected file'}), 400

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        for file in files:
            if file.filename == '':
                continue
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            cursor.execute("INSERT INTO uploaded_images (name, path) VALUES (%s, %s)", (filename, file_path))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dropbox'))

    except psycopg2.Error as e:
        print("Error uploading files to CockroachDB:", e)
        return jsonify({'message': 'Error uploading files'}), 500


@app.route('/save_transition_effect', methods=['POST'])
def save_transition_effect():
    data = request.json
    if 'effect' not in data:
        return jsonify({'message': 'No transition effect provided'}), 400           
    global T_effect
    T_effect = data.get('effect')

    return jsonify({'message': 'Transition effect saved successfully'}), 200

# @app.route('/update_desired_duration', methods=['POST'])
# def update_desired_duration():
#     data = request.form 
#     desired_duration = data.get('desired_duration')
#     if desired_duration is not None:
#         desired_duration = int(desired_duration)  
#         session['desired_duration'] = desired_duration 
#         return redirect(url_for('dropbox'))
#     else:
#         return jsonify({'message': 'Invalid data received'}), 400


from moviepy.editor import ImageSequenceClip, concatenate_videoclips

def create_video(transition_effect='pixelize'):
    try:
        conn = connect_to_database()
        if conn is None:
            print("Error: Could not connect to database")
            return False
            
        cursor = conn.cursor()

        image_folder = os.path.join(os.getcwd(), 'uploads')
        
        # Ensure the folder exists
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        # Get all image files and sort them to ensure consistent order
        image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])

        if not image_files:
            print("No image files found.")
            return False

        # Print the number of images found for debugging
        print(f"Found {len(image_files)} images: {[os.path.basename(f) for f in image_files]}")

        fps = 24
        size = (256, 144)
        desired_duration = session.get('desired_duration', 2)

        clips = []
        i = 0
        for image_file in image_files:
            try:
                image_array_list = []
                img = Image.open(image_file)
                img = img.resize(size)
                
                num_frames = int(desired_duration * fps)
                
                for _ in range(num_frames):
                    image_array_list.append(np.array(img))
                
                clip = ImageSequenceClip(image_array_list, fps=fps)
                
                clip_file_path = f"clip{i}.mp4"
                clip.write_videofile(clip_file_path, codec='libx264', audio_codec='aac')
                
                # Verify the clip was created
                if os.path.exists(clip_file_path):
                    print(f"Successfully created {clip_file_path}")
                    i += 1
                    cursor.execute("INSERT INTO uploaded_images (name, path) VALUES (%s, %s)", 
                                 (clip_file_path, os.path.abspath(clip_file_path)))
                else:
                    print(f"Failed to create {clip_file_path}")
            except Exception as e:
                print(f"Error processing image {image_file}: {e}")

        conn.commit()

        # Handle the case where no clips were created
        if i == 0:
            print("No clips were created from the images.")
            return False

        # Create a list for the transitioned clips
        transitioned_clips = []
        
        # Add the first clip
        if os.path.exists("clip0.mp4"):
            trans_clip_start = VideoFileClip("clip0.mp4")
            transitioned_clips.append(trans_clip_start)
        else:
            print("First clip (clip0.mp4) not found")
            return False

        # Apply transitions between clips
        for j in range(i-1):  # Changed from i-2 to i-1 to include all clips
            try:
                if os.path.exists(f"clip{j}.mp4") and os.path.exists(f"clip{j+1}.mp4"):
                    apply_transition(f"clip{j}.mp4", f"clip{j+1}.mp4", f"transitioned_clip{j}.mp4", 0.25, 0, T_effect)
                    if os.path.exists(f"transitioned_clip{j}.mp4"):
                        trans_clip = VideoFileClip(f"transitioned_clip{j}.mp4")
                        transitioned_clips.append(trans_clip)
                    else:
                        print(f"Failed to create transition clip {j}")
                else:
                    print(f"Clip {j} or {j+1} not found")
            except Exception as e:
                print(f"Error creating transition between clips {j} and {j+1}: {e}")

        # Ensure we have clips to concatenate
        if len(transitioned_clips) == 0:
            print("No transition clips were created.")
            return False

        # Concatenate all clips
        final_clip = concatenate_videoclips(transitioned_clips)
        final_clip.fps = fps
        final_clip.write_videofile("final_video.mp4", codec='libx264', audio_codec='aac')

        # Clean up temporary files
        for j in range(i):
            temp_clip = f"clip{j}.mp4"
            if os.path.exists(temp_clip):
                os.remove(temp_clip)

            transitioned_clip = f"transitioned_clip{j}.mp4"
            if os.path.exists(transitioned_clip):
                os.remove(transitioned_clip)

        # Add audio to the video
        add_audio_to_video()

        # Clean up the uploads folder
        delete_folders()
        
        cursor.close()
        conn.close()
        
        return True

    except psycopg2.Error as e:
        print("Error interacting with CockroachDB:", e)
        return False
    except Exception as e:
        print(f"Unexpected error in create_video: {e}")
        return False

def add_audio_to_video():
    try:

        conn = connect_to_database()
        cursor = conn.cursor()


        output_video_path = os.path.join(os.getcwd(), 'final_video.mp4')


        if not os.path.exists(output_video_path):
            print("Final video does not exist.")
            return False


        cursor.execute("SELECT file_path FROM audio_files ORDER BY id DESC LIMIT 1")
        latest_audio_path = cursor.fetchone()

        if latest_audio_path:
            latest_audio_path = latest_audio_path[0]

            duration_cmd = ['ffprobe', '-i', output_video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
            duration_output = subprocess.check_output(duration_cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
            video_duration = float(duration_output)

            audio_duration_cmd = ['ffprobe', '-i', latest_audio_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
            audio_duration_output = subprocess.check_output(audio_duration_cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
            audio_duration = float(audio_duration_output)

            if video_duration > audio_duration:
                
                loop_audio_cmd = ['ffmpeg', '-y', '-i', latest_audio_path, '-filter_complex', f'[0:a]aloop=loop=-1:size={int(video_duration/audio_duration)}[a]', '-map', '[a]', 'looped_audio.mp3']
                subprocess.run(loop_audio_cmd)
                latest_audio_path = os.path.join(os.getcwd(), 'looped_audio.mp3')
            elif audio_duration > video_duration:
                
                trimmed_audio_path = os.path.join(os.getcwd(), 'trimmed_audio.mp3')
                trim_audio_cmd = ['ffmpeg', '-y', '-i', latest_audio_path, '-ss', '0', '-t', str(video_duration), '-acodec', 'copy', trimmed_audio_path]
                subprocess.run(trim_audio_cmd)
                latest_audio_path = trimmed_audio_path

            
            video_with_audio_path = os.path.join(os.getcwd(), 'static/video_with_audio.mp4')
            subprocess.run(['ffmpeg', '-y', '-i', output_video_path, '-i', latest_audio_path, '-codec', 'copy', video_with_audio_path])

            
            if os.path.exists(video_with_audio_path):
                return True
            else:
                print("Failed to create video with audio.")
                return False
        else:
            print("No audio files found.")
            return False

    except (psycopg2.Error, subprocess.CalledProcessError) as e:
        print("Error adding audio to video:", e)
        return False
    finally:
        
        if conn:
            cursor.close()
            conn.close()


def apply_transition(input_video1, input_video2, output_video, duration, offset, transition):
    try:
        
        command = [
            "ffmpeg",
            '-i', input_video1,
            '-i', input_video2,
            '-filter_complex', f'xfade=transition={transition}:duration={duration}:offset={offset}',
            output_video
        ]
        
        
        subprocess.run(command)

        return True
    except subprocess.CalledProcessError as e:
        print("Error applying transition:", e)
        return False



def create_transitioned_clip(clip1, clip2, transition_effect='pixelize'):
    transition_duration = 1  
    transition_offset = 3  



    
def add_audio_to_clip(clip):
    try:
       
        conn = connect_to_database()
        cursor = conn.cursor()

        
        cursor.execute("SELECT file_path FROM audio_files ORDER BY id DESC LIMIT 1")
        latest_audio_path = cursor.fetchone()

        if latest_audio_path:
            latest_audio_path = latest_audio_path[0]
            audio_clip = AudioFileClip(latest_audio_path)
            clip = clip.set_audio(audio_clip)

        return clip

    except psycopg2.Error as e:
        print("Error fetching audio file path from CockroachDB:", e)
        return clip  

    finally:
        
        if conn:
            cursor.close()
            conn.close()



def fetch_audio_files():
    try:
        conn = connect_to_database()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT file_name, file_path FROM audio_files")
        audio_files = cursor.fetchall()
        cursor.close()
        conn.close()
        return audio_files
    except psycopg2.Error as e:
        print("Error fetching audio files:", e)
        return []

@app.route('/admin')
def admin():
    users = fetch_user_details()
    return render_template('admin.html', users=users)

@app.route('/dropbox')
def dropbox():
    audio_files = fetch_audio_files()
    username = get_username()
    video_with_audio_exists = os.path.exists(os.path.join(os.getcwd(), 'static', 'video_with_audio.mp4'))

    return render_template('dropbox.html', audio_files=audio_files, username=username, video_exists=video_with_audio_exists)



@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    data = request.form 
    desired_duration = data.get('desired_duration')
    if desired_duration is not None:
        desired_duration = int(desired_duration)  
        session['desired_duration'] = desired_duration
    if 'audio' not in request.files or desired_duration is None:
        return jsonify({'message': 'No audio part'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'message': 'No selected audio'}), 400

    audio_folder = os.path.join(os.getcwd(), 'audio_uploads')
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    filename = secure_filename(audio_file.filename)
    audio_path = os.path.join(audio_folder, filename)
    audio_file.save(audio_path)

    try:
        
        conn = connect_to_database()
        cursor = conn.cursor()

        
        cursor.execute("INSERT INTO audio_files (file_name, file_path) VALUES (%s, %s)", (filename, audio_path))
        conn.commit()
        
        
        cursor.close()
        conn.close()

        
        create_video()

        return redirect(url_for('dropbox'))

    except psycopg2.Error as e:
        print("Error executing SQL query:", e)
        return jsonify({'message': 'Error storing audio file data in the database.'}), 500

    except Exception as e:
        print("Error uploading audio:", e)
        return jsonify({'message': 'An error occurred while processing your request.'}), 500


from flask import request, jsonify


import os

@app.route('/download_video')
def download_video():
    
    video_with_audio_exists = os.path.exists('static/video_with_audio.mp4')
    
    
    slideshow_exists = os.path.exists('static/slideshow.mp4')
    
    
    video_exists = video_with_audio_exists or slideshow_exists
    
    
    if video_with_audio_exists:
        video_path = 'static/video_with_audio.mp4'
        filename = 'video_with_audio.mp4'
    elif slideshow_exists:
        video_path = 'static/slideshow.mp4'
        filename = 'slideshow.mp4'
    else:
        return 'No video available for download.'
    
    
    return send_file(video_path, as_attachment=True, attachment_filename=filename)

    
if __name__ == '__main__':
    app.run(debug=True)