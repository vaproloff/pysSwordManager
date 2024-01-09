function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function () {
        alert('Password copied to clipboard!');
    }, function (err) {
        console.error('Unable to copy text to clipboard.', err);
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