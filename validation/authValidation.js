// Validation functions for authentication
export function isValidUsername(username) {
    return username && username.length >= 3;
}

export function isValidPassword(password) {
    return password && password.length >= 6;
}
