document.getElementById('temperature-form').onsubmit = async (event) => {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const formData = new FormData(event.target);
    const temperature = formData.get('temperature');

    try {
        const response = await fetch('/seting/add_temperature', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ temperature: parseInt(temperature) }),
        });

        if (response.ok) {
            alert('Температура успешно отправлена!');
        } else {
            alert('Ошибка при отправке температуры.');
        }
    } catch (error) {
        alert(`Ошибка: ${error.message}`);
    }
};

        // Код для генерации часов и минут
        const hourOnSelect = document.getElementById('hour-on');
        const minuteOnSelect = document.getElementById('minute-on');
        const hourOffSelect = document.getElementById('hour-off');
        const minuteOffSelect = document.getElementById('minute-off');

        // Генерация часов
        for (let i = 0; i <= 23; i++) {
            hourOnSelect.innerHTML += `<option value="${i}">${i}</option>`;
            hourOffSelect.innerHTML += `<option value="${i}">${i}</option>`;
        }

        // Генерация минут
        for (let i = 0; i <= 59; i++) {
            minuteOnSelect.innerHTML += `<option value="${i}">${i}</option>`;
            minuteOffSelect.innerHTML += `<option value="${i}">${i}</option>`;
        }

        // Код для отправки времени
        document.getElementById('time-form').onsubmit = async (event) => {
            event.preventDefault(); // Предотвращаем стандартное поведение формы

            const formData = new FormData(event.target);
            const hourOn = formData.get('hour-on');
            const minuteOn = formData.get('minute-on');
            const hourOff = formData.get('hour-off');
            const minuteOff = formData.get('minute-off');

           // Определяем, какая кнопка была нажата
           const submitButton = event.submitter.id;

           let url;
           let body;

           if (submitButton === 'submit-clock-water') {
               url='/seting/clock_water'; // URL для включения полива
               body={ hour : parseInt(hourOn), minute : parseInt(minuteOn) };
           } else if (submitButton === 'submit-clock-water-off') {
               url='/seting/clock_water_off'; // URL для отключения полива
               body={ hour : parseInt(hourOff), minute : parseInt(minuteOff) };
           }

          // Отправка данных на сервер
          const response= await fetch(url, {
              method:'POST',
              headers:{
                  'Content-Type':'application/json',
              },
              body : JSON.stringify(body),
          });

          if (response.ok) {
              const result= await response.json();
              alert(result.message); // Показываем сообщение от сервера
          } else {
              alert('Ошибка при отправке времени.');
          }
      };


document.getElementById('show-settings').onclick = async () => {
    const outputDiv = document.getElementById('settings-output');

    // Проверяем текущее состояние блока
    if (outputDiv.style.display === 'none' || outputDiv.style.display === '') {
        outputDiv.innerHTML = ''; // Очищаем предыдущие результаты

        try {
            const temperatureResponse = await fetch('/seting/last_temperature');
            const clockWaterResponse = await fetch('/seting/last_clock_water');
            const clockWaterOffResponse = await fetch('/seting/last_clock_water_off');

            if (temperatureResponse.ok) {
                const temperatureData = await temperatureResponse.json();
                outputDiv.innerHTML += `<p>Температура: ${temperatureData.temperature} °C</p>`;
            } else {
                outputDiv.innerHTML += `<p>${(await temperatureResponse.json()).message}</p>`;
            }

            if (clockWaterResponse.ok) {
                const clockWaterData = await clockWaterResponse.json();
                outputDiv.innerHTML += `<p>Время включения полива: ${clockWaterData.time}</p>`;
            } else {
                outputDiv.innerHTML += `<p>${(await clockWaterResponse.json()).message}</p>`;
            }

            if (clockWaterOffResponse.ok) {
                const clockWaterOffData = await clockWaterOffResponse.json();
                outputDiv.innerHTML += `<p>Время отключения полива: ${clockWaterOffData.time}</p>`;
            } else {
                outputDiv.innerHTML += `<p>${(await clockWaterOffResponse.json()).message}</p>`;
            }

        } catch (error) {
            outputDiv.innerHTML = `<p>Ошибка: ${error.message}</p>`;
        }

        outputDiv.style.display = 'block'; // Показываем блок
    } else {
        outputDiv.style.display = 'none'; // Скрываем блок
    }
};

