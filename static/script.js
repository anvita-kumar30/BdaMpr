// script.js
document.getElementById("emailForm").onsubmit = function(event) {
    event.preventDefault();
    let emailContent = document.getElementById("email").value;

    fetch('/send_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'email=' + encodeURIComponent(emailContent),
    })
    .then(response => response.json())
    .then(data => {
        let resultSection = document.getElementById(data.result === "Spam" ? "spam-list" : "normal-list");

        // Create a new list item for the email
        let emailItem = document.createElement("li");
        emailItem.textContent = data.email;

        // Append it to the respective section (Spam or Normal)
        resultSection.appendChild(emailItem);

        // Clear the email content after submission
        document.getElementById("email").value = '';
    })
    .catch(error => {
        console.error("Error:", error);
    });
};

// Add event listener for the form submission
document.getElementById("emailForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting normally
    
    // Get the email content from the textarea
    const emailContent = document.getElementById("email").value;
  
    // Count the total words in the email content and display it
    const totalWordCount = countWords(emailContent);
  
    // Display the total word count in the 'word-count' paragraph
    document.getElementById("word-count").innerText = "Total Words: " + totalWordCount;
  
    // Display the entered email content in the 'email-section' paragraph
    document.getElementById("email-section").innerText = emailContent;
  });
  
  // Function to count total words in the email content
  function countWords(text) {
    // Trim and split the text by spaces or newlines to get the words
    let words = text.trim().split(/\s+/);
    // Filter out any empty strings and return the word count
    return words.filter(word => word.length > 0).length;
  }
  