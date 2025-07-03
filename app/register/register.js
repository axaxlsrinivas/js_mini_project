document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const messageDiv = document.getElementById('registerMessage');

    // Basic validation
    if (!username || !email || !password || !confirmPassword) {
        messageDiv.textContent = 'All fields are required.';
        messageDiv.style.color = 'red';
        return;
    }
    if (password !== confirmPassword) {
        messageDiv.textContent = 'Passwords do not match.';
        messageDiv.style.color = 'red';
        return;
    }

    // Call REST API for registration
    try {
        const response = await fetch('http://localhost:3000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });
        const data = await response.json();
        if (response.ok) {
            messageDiv.textContent = 'Registration successful! You can now login.';
            messageDiv.style.color = 'green';
            setTimeout(() => {
                window.location.href = '../auth/auth.html';
            }, 1500);
        } else {
            messageDiv.textContent = data.message || 'Registration failed.';
            messageDiv.style.color = 'red';
        }
    } catch (err) {
        messageDiv.textContent = 'Registration failed. Please try again.';
        messageDiv.style.color = 'red';
    }
});
