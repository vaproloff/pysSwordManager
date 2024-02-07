function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function () {
        alert('Пароль успешно скопирован в буфер');
    }, function (err) {
        console.error('Ошибка при копировании пароля в буфер', err);
    });
}

function generatePassword() {
    fetch(`/generator/generate/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('id_password').value = data.password;
        })
        .catch(error => console.error('Error:', error));
}