function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function () {
        alert('Пароль успешно скопирован в буфер');
    }, function (err) {
        console.error('Ошибка при копировании пароля в буфер', err);
    });
}
