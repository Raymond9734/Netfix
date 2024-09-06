document.getElementById('toggleDescriptionBtn').addEventListener('click', function() {
    var descriptionField = document.getElementById('descriptionField');
    if (descriptionField.style.display === 'none') {
        descriptionField.style.display = 'block';
        this.textContent = 'Hide Company Description';
    } else {
        descriptionField.style.display = 'none';
        this.textContent = 'Add Company Description';
    }
});