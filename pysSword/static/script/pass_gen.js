function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function () {
        alert('Password copied to clipboard!');
    }, function (err) {
        console.error('Unable to copy text to clipboard.', err);
    });
}