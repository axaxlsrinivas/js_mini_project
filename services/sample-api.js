// Simple REST API using Express.js for user registration and login
// To use: npm install express body-parser cors

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

// In-memory user store (for demo only)
const users = [];

// Registration endpoint
app.post('/api/register', (req, res) => {
    const { username, email, password } = req.body;
    if (!username || !email || !password) {
        return res.status(400).json({ message: 'All fields are required.' });
    }
    if (users.find(u => u.email === email)) {
        return res.status(409).json({ message: 'Email already registered.' });
    }
    users.push({ username, email, password });
    res.status(201).json({ message: 'Registration successful.' });
});

// Login endpoint
app.post('/api/login', (req, res) => {
    const { email, password } = req.body;
    const user = users.find(u => u.email === email && u.password === password);
    if (!user) {
        return res.status(401).json({ message: 'Invalid email or password.' });
    }
    res.json({ message: 'Login successful.', user: { username: user.username, email: user.email } });
});

app.listen(PORT, () => {
    console.log(`API server running on http://localhost:${PORT}`);
});
