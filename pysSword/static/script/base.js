document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        document.querySelectorAll('.messages li')
            .forEach(function (message) {
                message.remove();
            });
    }, 5000);
});
