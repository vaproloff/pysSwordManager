function showEditField(formId, inputId, curValue) {
    document.getElementById(formId).style.display = 'block';
    document.getElementById(inputId).value = curValue;
}

function showChangePasswordForm() {
    document.getElementById('password-form').style.display = 'block';
}
