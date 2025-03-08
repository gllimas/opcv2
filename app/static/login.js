document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/auth/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            username: username,
            password: password,
        }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token); // Сохраните токен в localStorage
        window.location.href = '/'; // Перенаправьте на главную страницу
    } else {
        document.getElementById('login-response').innerText = 'Ошибка входа: неверное имя пользователя или пароль';
    }
});