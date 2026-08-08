const tg = window.Telegram.WebApp;
tg.expand();

// Динамическое отображение кода цвета
const colorInput = document.getElementById('emoji-color');
const colorHexText = document.getElementById('color-hex');

colorInput.addEventListener('input', (e) => {
    colorHexText.textContent = e.target.value.toUpperCase();
});

document.getElementById('submit-btn').addEventListener('click', () => {
    const templateId = document.getElementById('template-select').value;
    const textValue = document.getElementById('emoji-text').value.trim();
    const colorValue = document.getElementById('emoji-color').value;

    if (!textValue) {
        alert('Пожалуйста, введите текст для эмодзи!');
        return;
    }

    const payload = {
        templateId: templateId,
        text: textValue,
        fill: colorValue
    };

    tg.sendData(JSON.stringify(payload));
});
