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

function loadPasswordCreation() {
    fetch(`/passwords/new/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('password-details').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

function loadPasswordEdition(entryId) {
    fetch(`/passwords/${entryId}/edit/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('password-details').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

function debounce(func, delay) {
    let timeoutId;
    return function () {
        const context = this;
        const args = arguments;
        clearTimeout(timeoutId);
        timeoutId = setTimeout(function () {
            func.apply(context, args);
        }, delay);
    };
}

function filterEntries() {
    const searchInput = document.getElementById('id_search_term');
    const entries = document.querySelectorAll('.password_entry_link');

    const searchTerm = searchInput.value.toLowerCase();

    entries.forEach(function (entry) {
        const title = entry.querySelector('.password_entry_title').innerText.toLowerCase();
        const login = entry.querySelector('.password_entry_login').innerText.toLowerCase();

        if (title.includes(searchTerm) || login.includes(searchTerm)) {
            entry.style.display = 'block';
        } else {
            entry.style.display = 'none';
        }
    });
}

function clipInputValue(inputId) {
    const input = document.getElementById(inputId)
    navigator.clipboard.writeText(input.value).then(function () {
        alert('Скопировано в буфер');
    }, function (err) {
        console.error('Ошибка при копировании в буфер', err);
    });
}

const debouncedFilter = debounce(filterEntries, 500);

document.getElementById('id_search_term').addEventListener('input', debouncedFilter);

document.getElementById('clear-search-button').addEventListener('click', function () {
    document.getElementById('id_search_term').value = '';
    filterEntries()
});

document.addEventListener('DOMContentLoaded', function () {
    const passwordLinks = document.querySelectorAll('.password_entry_link');
    passwordLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const entryId = this.dataset.entryId;
            loadPasswordEdition(entryId);
        });
    });
});

