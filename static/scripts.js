document.getElementById("email-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent form from reloading the page

    // Get the value of the email text area
    let emailText = document.getElementById("email_text").value;

    // Send the email text to the Flask backend using fetch
    fetch("/predict", {
        method: "POST",  // HTTP method
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",  // Setting the content type
        },
        body: `email_text=${encodeURIComponent(emailText)}`,  // Send the email text as form data
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        // Update the result div with the prediction
        document.getElementById("result").innerHTML = `<h3>Result: ${data.result}</h3>`;
    })
    .catch(error => {
        console.error('Error:', error);  // Log any error to the console
    });
});
