async function fetchPorts() {
            try {
                const response = await fetch('/kontrol/usb_ports');
                if (!response.ok) {
                    throw new Error('Сеть не отвечает');
                }
                const data = await response.json();
                const portSelect = document.getElementById('port-select');


                portSelect.innerHTML = '<option value="">-- Пожалуйста, выберите порт --</option>';
                data.ports.forEach(port => {
                    const option = document.createElement('option');
                    option.value = port.device;
                    option.textContent = `${port.device} - ${port.description}`;
                    portSelect.appendChild(option);
                });
            } catch (error) {
                console.error('Ошибка при загрузке портов:', error);
            }
        }


        window.onload = fetchPorts;


        document.getElementById('connect-button').addEventListener('click', async () => {
            const selectedPort = document.getElementById('port-select').value;
            if (selectedPort) {
                const response = await fetch('/kontrol/select_port', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ port: selectedPort }),
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(`Выбран порт: ${result.port}`);
                } else {
                    alert('Ошибка при выборе порта. Попробуйте позже.');
                }
            } else {
                alert('Пожалуйста, выберите порт.');
            }
        });

        document.getElementById('back-button').addEventListener('click', function() {
            window.location.href = '/';  // Замените '/' на URL вашего главного экрана
        });