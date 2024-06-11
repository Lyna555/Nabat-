document.addEventListener("DOMContentLoaded", function () {
    const dropZone = document.getElementById('cloud_container');
    const fileInput = document.getElementById('image');
    const cloudImage = document.getElementById('cloud');
    const form = document.getElementById('plant');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('highlight'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('highlight'), false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);

    // Handle file selection via input
    fileInput.addEventListener('change', handleFiles, false);

    // Validate form submission
    form.addEventListener('submit', function (event) {
        if (!fileInput.files.length) {
            event.preventDefault();
            alert('Please choose or drag an image before submitting.');
        }
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        handleFiles();
    }

    function handleFiles() {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (event) {
                cloudImage.src = event.target.result;
            }
            reader.readAsDataURL(file);
        }
    }
});
