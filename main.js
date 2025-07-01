document.getElementById('change-message-btn').addEventListener('click', function() {
    const message = document.getElementById('welcome-message');
    if (message.textContent === 'Welcome to your JavaScript Web App!') {
        message.textContent = 'You clicked the button!';
    } else {
        message.textContent = 'Welcome to your JavaScript Web App!';
    }
});
