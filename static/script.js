function togglePassword(inputId) {
    var passwordInput = document.getElementById(inputId);
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}
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


var slideIndex = 1;
showSlides(slideIndex);
function plusSlides(n) {
    showSlides(slideIndex += n);
}
function currentSlide(n) {
    showSlides(slideIndex = n);
}
function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}
document.addEventListener("DOMContentLoaded", function () {
    var loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', function (event) {
        var passwordInput = document.getElementById('login-password').value;
        var confirmPasswordInput = document.getElementById('confirm-password').value;
        if (passwordInput !== confirmPasswordInput) {
            alert("Password and Confirm Password do not match. Please enter the same password in both fields.");
            event.preventDefault();
        } else {
            var usernameInput = document.getElementById('login-username').value;
            if (usernameInput !== "" && passwordInput !== "") {
                openHomePage();
            }
        }
    });
});


