// Authentication JS logic for login/register

document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const message = document.getElementById('auth-message');

    // Simple static authentication for demo
    if (username === 'user' && password === 'password') {
        message.style.color = 'green';
        message.textContent = 'Login successful!';
        // Redirect or further logic can go here
    } else {
        message.style.color = 'red';
        message.textContent = 'Invalid username or password.';
    }
});

// Forgot Password button action
const forgotBtn = document.getElementById('forgot-password-btn');
if (forgotBtn) {
    forgotBtn.addEventListener('click', function() {
        // Navigate parent iframe to forgot password page using absolute path
        if (window.parent && window.parent !== window) {
            window.parent.document.getElementById('app-frame').src = '/app/forgot-password/forgot-password.html';
        } else {
            // Fallback: open in current window if not in iframe
            window.location.href = '/app/forgot-password/forgot-password.html';
        }
    });
}

// Register button action
const registerBtn = document.getElementById('register-btn');
if (registerBtn) {
    registerBtn.addEventListener('click', function() {
        // Navigate parent iframe to forgot password page using absolute path
        if (window.parent && window.parent !== window) {
            window.parent.document.getElementById('app-frame').src = '/app/register/register.html';
        } else {
            // Fallback: open in current window if not in iframe
            window.location.href = '/app/register/register.html';
        }
    });
}

// Google Sign-In button action
const googleBtn = document.getElementById('google-signin-btn');
if (googleBtn) {
    googleBtn.addEventListener('click', function() {
        alert('Google Sign-In functionality is not implemented yet.');
    });
}
