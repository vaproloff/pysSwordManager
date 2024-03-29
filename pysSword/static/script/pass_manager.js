function showHidePassword() {
    const passInput = document.getElementById('id_password');
    passInput.type = passInput.type === 'password' ? 'text' : 'password';
}

function clipInputValue(inputId) {
    const input = document.getElementById(inputId)
    navigator.clipboard.writeText(input.value).then(function () {
        alert('Скопировано в буфер');
    }, function (err) {
        console.error('Ошибка при копировании в буфер', err);
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

function loadPasswordCreation(pushHistory = true) {
    fetch(`/passwords/new/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('password-details').innerHTML = data;
            if (pushHistory) history.pushState(null, null, `/passwords/#new_entry`);
        })
        .catch(error => console.error('Error:', error));
}

function loadPasswordEdition(entryId, pushHistory = true) {
    fetch(`/passwords/${entryId}/edit/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('password-details').innerHTML = data;
            if (pushHistory) history.pushState(null, null, `/passwords/#entry_${entryId}`);
        })
        .catch(error => console.error('Error:', error));
}

function loadFromHash(pushHistory) {
    const entryHash = window.location.hash;
    if (entryHash.startsWith('#entry_')) {
        loadPasswordEdition(entryHash.replace('#entry_', ''), pushHistory);
    } else if (entryHash.startsWith('#new_entry')) {
        loadPasswordCreation(pushHistory);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const passwordLinks = document.querySelectorAll('.password_entry_link');
    passwordLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const entryId = this.dataset.entryId;
            loadPasswordEdition(entryId);
        });
    });

    loadFromHash(true)
    window.addEventListener('popstate', function (event) {
        loadFromHash(false)
    });
});

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
    const entries = document.querySelectorAll('.password_entry_link');
    const query = document.getElementById('id_search_term').value.toLowerCase();

    entries.forEach(function (entry) {
        const title = entry.querySelector('.password_entry_title').innerText.toLowerCase();
        const login = entry.querySelector('.password_entry_login').innerText.toLowerCase();

        if (title.includes(query) || login.includes(query)) {
            entry.style.display = 'block';
        } else {
            entry.style.display = 'none';
        }
    });
}

const debouncedFilter = debounce(filterEntries, 500);

document.getElementById('id_search_term').addEventListener('input', debouncedFilter);

document.getElementById('clear-search-button').addEventListener('click', function () {
    document.getElementById('id_search_term').value = '';
    filterEntries()
});
