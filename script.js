// Инициализация Telegram WebApp
const tg = window.Telegram.WebApp;
tg.expand(); // Разворачиваем на весь экран

document.getElementById('save-btn').addEventListener('click', () => {
    const textValue = document.getElementById('emoji-text').value;
    const colorValue = document.getElementById('emoji-color').value;

    // Упаковываем данные в JSON объект
    const formData = {
        text: textValue,
        fill: colorValue
    };

    // Отправляем данные боту и закрываем Mini App
    tg.sendData(JSON.stringify(formData));
});
