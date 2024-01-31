function showHidePassword() {
    const passInput = document.getElementById('id_password');
    passInput.type = passInput.type === 'password' ? 'text' : 'password';
}

function getPassword(passEntryId) {
    return new Promise((resolve, reject) => {
        fetch(`/passwords/get/${passEntryId}`)
            .then(response => response.json())
            .then(data => resolve(data.password))
            .catch(error => {
                console.error('Error:', error);
                reject(error);
            });
    });
}

function showPassword(passEntryId) {
    getPassword(passEntryId)
        .then(password => {
            document.getElementById('decrypted_password').innerText = password;
        })
        .catch(error => {
            console.error('Ошибка при получении пароля:', error);
        });
}

function copyPassword(passEntryId) {
    getPassword(passEntryId)
        .then(password => {
            navigator.clipboard.writeText(password)
                .then(function () {
                    alert('Пароль успешно скопирован в буфер обмена!');
                }, function (err) {
                    alert('Ошибка при копировании пароля в буфер обмена');
                    console.error('Unable to copy text to clipboard.', err);
                });
        })
        .catch(error => {
            console.error('Ошибка при получении пароля:', error);
        });
}

function loadPasswordDetail(entryId) {
    fetch(`/passwords/${entryId}/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('id_right_side').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

function loadPasswordCreation() {
    fetch(`/passwords/new/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('id_right_side').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

function loadPasswordEdition(entryId) {
    fetch(`/passwords/${entryId}/edit/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('id_right_side').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function () {
    const passwordLinks = document.querySelectorAll('.password_entry_link');
    console.log(passwordLinks)
    passwordLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const entryId = this.dataset.entryId;
            loadPasswordDetail(entryId);
        });
    });
});

