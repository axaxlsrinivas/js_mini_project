const form = document.getElementById('forgot-password-form');
const message = document.getElementById('fp-message');
const otpSection = document.getElementById('otp-section');
const resetSection = document.getElementById('reset-section');
const usernameInput = document.getElementById('fp-username');
const otpInput = document.getElementById('fp-otp');
const validateOtpBtn = document.getElementById('fp-validate-otp-btn');
const newPasswordInput = document.getElementById('fp-new-password');
const confirmPasswordInput = document.getElementById('fp-confirm-password');
const resetPasswordBtn = document.getElementById('fp-reset-password-btn');

let generatedOtp = null;

form.addEventListener('submit', function(e) {
    e.preventDefault();
    // Simulate sending OTP
    generatedOtp = Math.floor(100000 + Math.random() * 900000).toString();
    message.style.color = 'green';
    message.textContent = `OTP sent to your email. (Demo OTP: ${generatedOtp})`;
    otpSection.style.display = 'block';
    form.style.display = 'none';
});

validateOtpBtn.addEventListener('click', function() {
    if (otpInput.value === generatedOtp) {
        message.style.color = 'green';
        message.textContent = 'OTP validated. Please enter your new password.';
        otpSection.style.display = 'none';
        resetSection.style.display = 'block';
    } else {
        message.style.color = 'red';
        message.textContent = 'Invalid OTP. Please try again.';
    }
});

resetPasswordBtn.addEventListener('click', function() {
    const newPassword = newPasswordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    if (newPassword.length < 6) {
        message.style.color = 'red';
        message.textContent = 'Password must be at least 6 characters.';
        return;
    }
    if (newPassword !== confirmPassword) {
        message.style.color = 'red';
        message.textContent = 'Passwords do not match.';
        return; 
    }
    // Simulate password reset
    message.style.color = 'green';
    message.textContent = 'Password reset successful! You may now log in.';
    resetSection.style.display = 'none';
    // Navigate back to login after short delay
    setTimeout(function() {
        if (window.parent && window.parent !== window) {
            window.parent.document.getElementById('app-frame').src = '/app/auth/auth.html';
        } else {
            window.location.href = '/app/auth/auth.html';
        }
    }, 1500);
});
