document.addEventListener('DOMContentLoaded', function() {
    var createBtn = document.getElementById('create-btn');
    var modal = document.getElementById('new-folder-card');
    var closeBtn = document.querySelector('.close-btn');
    var createFolderBtn = document.getElementById('create-folder-btn');
    
    createBtn.addEventListener('click', function() {
        modal.style.display = 'flex';
    });

    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    createFolderBtn.addEventListener('click', function() {
        var folderName = document.getElementById('folder-name').value;
        if (folderName.trim() !== "") {
            // Handle the creation of the folder with the name `folderName`
            console.log('Folder Created: ' + folderName);
            modal.style.display = 'none';
        } else {
            alert('Please enter a folder name');
        }
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
