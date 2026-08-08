const tg = window.Telegram.WebApp;
tg.expand(); // Растягиваем мини-приложение на весь экран

document.getElementById('submit-btn').addEventListener('click', () => {
    const textValue = document.getElementById('emoji-text').value;
    const colorValue = document.getElementById('emoji-color').value;

    // Упаковываем настройки в JSON
    const payload = {
        text: textValue,
        fill: colorValue
    };

    // Передаем данные боту и закрываем мини-приложение
    tg.sendData(JSON.stringify(payload));
});
