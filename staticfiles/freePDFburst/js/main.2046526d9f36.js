var typed = new Typed('.element', {
    strings: ["Welcome to freePDFBurst.", "Burst your PDF file into seperate pages and recieve an email of each page."],
    typeSpeed: 30
});

var input = document.getElementById('customFile');
var infoArea = document.getElementById('file-name');

input.addEventListener('change', showFileName);

function showFileName(event) {

    // the change event gives us the input it occurred in 
    var input = event.srcElement;

    // the input has an array of files in the `files` property, each one has a name that you can use. We're just using the name here.
    var fileName = input.files[0].name;

    // use fileName however fits your app best, i.e. add it into a div
    infoArea.textContent = 'File to upload : ' + fileName;
}