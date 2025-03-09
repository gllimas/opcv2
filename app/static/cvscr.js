const facesList = document.getElementById("faces");
const websocket = new WebSocket("ws://localhost:8080/ws/video");

websocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    facesList.innerHTML = ""; // Очистить список

    data.names.forEach((name, index) => {
        const li = document.createElement("li");
        li.textContent = `${name} at ${data.locations[index]}`;
        facesList.appendChild(li);
    });
};

websocket.onclose = function(event) {
    console.log("WebSocket closed:", event);
};

websocket.onerror = function(error) {
    console.error("WebSocket error:", error);
};

        // Обработка формы загрузки
document.getElementById('upload-form').onsubmit = async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const responseDiv = document.getElementById('response');

    const response = await fetch('/api/upload/', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (response.ok) {
        responseDiv.innerHTML = `<p>Загрузка успешна! ID: ${result.id}, Заголовок: ${result.title}</p>`;
    } else {
        responseDiv.innerHTML = `<p>Ошибка: ${result.message}</p>`;
    }
};

document.getElementById('logoutButton').addEventListener('click', () => {
    localStorage.removeItem('access_token');
    window.location.href = 'login';
});


const token = localStorage.getItem('access_token');

if (!token) {
    alert('Авторизуйтесь');
    window.location.href = '/login';
} else {

    fetch('/protected-resource', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('userData').innerText = JSON.stringify(data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

