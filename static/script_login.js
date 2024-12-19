document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;
    console.log(username);
    console.log(password);
    fetch('/login_handler', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'username': username,
            'password': password
        })
    })
        .then(response => response.json())
        .then(data => {
            if(data.message === 'successful') {
                localStorage.setItem('token', data.token);
                window.location.href = '/dropbox';
            } else {
                alert('Invalid username or password');
            }
        })
        .catch(error => console.error('Error:', error));
});
window.onload = function () {
    var token = localStorage.getItem('token');
    if (token) {
        window.location.href = '/dropbox';
    }
};
function openLoginPage() {
    window.open('/login', '_blank');
}
function openHomePage() {
    window.open('/', '_blank');
}
function openSignupPage() {
    window.open('/signup', '_blank');
}
function openDropbox() {
    window.open('/dropbox', '_blank');
}
function adminLogin() {
    var usernameInput = document.getElementById('login-username').value;
    var passwordInput = document.getElementById('login-password').value;
    if (usernameInput === "admin" && passwordInput === "admin") {
        window.location.href = '/admin';
    } else {
        openHomePage();
    }
}