$(document).ready(function() {

    $("#book-form").submit(function(e) {
        e.preventDefault();
    });

    $('#submit').click(function() {
        add_this();
    });

    // Ensure user is authenticated (optional, if you want to add authentication)
    // Firebase authentication part can be removed if you want to implement your own authentication
    // firebase.auth().onAuthStateChanged(user => {
    //     if(!user) {
    //         window.location = 'index.html';
    //     }
    // });

});

function add_this() {
    var BookCode = document.getElementById("book_code").value;
    var BookName = document.getElementById("book_name").value;
    var Author1 = document.getElementById("author1").value;
    var Author2 = document.getElementById("author2").value;
    var Subject = document.getElementById("Subject").value;
    var Tags = document.getElementById("tags").value;

    // Prepare the data to send to the backend
    var data = {
        titre: BookName,
        annee_publication: 2023, // You might want to adjust this (date input is not in the form)
        editeur: "Editeur exemple", // Adjust according to your form fields
        reference: BookCode,
    };

    // Send the data to the FastAPI backend (change URL if necessary)
    $.ajax({
        url: "http://127.0.0.1:8000/documents/", // FastAPI URL
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function(response) {
            console.log("Document successfully added!", response);
            alert("Successfully Book Added");
            window.location = 'admin_portal.html'; // Redirect after adding the book
        },
        error: function(xhr, status, error) {
            console.error("Error adding document:", error);
            alert("Error adding the book.");
        }
    });
}
