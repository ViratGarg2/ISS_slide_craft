var audioPlayer = new Audio();
var audioFile = null;
var previewVideo = document.getElementById('slideshow');

function handleFileSelect(event) {
    const files = event.target.files;
    if (files.length > 0) {
        handleImages(files);
    }
}

function openTab(tabName) {
    var i, tabcontent;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block";
}

function handleDragOver(event) {
    event.preventDefault();
}

function handleDrop(event) {
    event.preventDefault();
    const files = event.dataTransfer.files;
    handleImages(files);  
    saveImages(files);     
}

function saveImages(files) {
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]); 
    }

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); 
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function handleImages(files) {
    const preview = document.getElementById('preview');
    const loading = document.getElementById('loading');

    loading.style.display = 'flex';

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();

        reader.onload = function (e) {
            const imageContainer = document.createElement('div');
            imageContainer.className = 'image-container';
            imageContainer.innerHTML = `
                                        <img src="${e.target.result}" alt="Uploaded Image">
                                        <select class="duration-dropdown" name="durations[]"> <!-- Include name attribute for the select element -->
                                            <option value="3">3 seconds</option>
                                            <option value="5">5 seconds</option>
                                            <option value="10">10 seconds</option>
                                        </select>
                                       `;
            preview.appendChild(imageContainer);

            if (i === files.length - 1) {
                loading.style.display = 'none';
            }
        };

        reader.readAsDataURL(file);
    }
}

function handleTransitionEffectSelect() {
    var selectElement = document.getElementById('transition-dropdown');
    var selectedEffect = selectElement.options[selectElement.selectedIndex].value;

  
    fetch('/save_transition_effect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ effect: selectedEffect })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); 
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




function setDuration(select) {
    const duration = select.value;
    const imageContainer = select.parentNode;
    imageContainer.dataset.duration = duration; 
}

function handleAudioSelect(event) {
    const file = event.target.files[0];
    audioFile = file;
    document.getElementById('audio-info').setAttribute('style', 'color:purple;font-size:25px;');
    document.getElementById('audio-info').innerText = 'Selected audio file: ' + file.name;

    audioPlayer.src = URL.createObjectURL(file);
}
function Play_Video() {
var video = document.getElementById('video-preview');
if (video.paused) {
video.play();
}
}
function Pause_Video() {
var video = document.getElementById('video-preview');
if (video.play) {
video.pause();
}
}

function rewindPreview() {
var video = document.getElementById('video-preview');
video.currentTime = 0;
}


document.getElementById('playbtn').addEventListener('click',Play_Video());
document.getElementById('pausebtn').addEventListener('click',Pause_Video());
document.getElementById('rewindbtn').addEventListener('click', rewindPreview);


function handleProfilePictureUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('profile-image').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}



function logout() {
    localStorage.removeItem('token'); 
    window.location.href = '/'; 
}
var desiredDurationInput = document.getElementById("desired_duration");



function updateDesiredDuration() {
    var desiredDuration = document.getElementById("desired_duration").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/update_desired_duration", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ desired_duration: desiredDuration }));
}

function toggleMute() {
var video = document.getElementById('video-preview');
if (video.muted) {
    video.muted = false;
    document.getElementById('mutebtn').innerText = 'Mute';
} else {
    video.muted = true;
    document.getElementById('mutebtn').innerText = 'Unmute';
}
}

