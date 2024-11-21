function captureImage() {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");

    // Capture the current frame from the video stream
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Get the base64-encoded image
    const imageData = canvas.toDataURL("image/jpeg");

    // Send the base64 image to the Flask backend for emotion detection
    fetch("/detect_face", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: imageData }),
    })
    .then(response => response.json())
    .then(data => {
        // Display emotion and suggestions
        document.getElementById("emotion").textContent = `Emotion: ${data.emotion}`;
        const suggestionsList = document.getElementById("suggestions");
        suggestionsList.innerHTML = "";
        data.suggestions.forEach(suggestion => {
            const li = document.createElement("li");
            li.textContent = suggestion;
            suggestionsList.appendChild(li);
        });
    })
    .catch(error => {
        console.error("Error processing the image:", error);
    });
}
// Function to fetch the latest suggestion
function fetchSuggestion() {
    fetch('/get_suggestion')
        .then(response => response.json())
        .then(data => {
            // Update the suggestion text on the page
            document.getElementById('suggestion-text').innerText = data.suggestion;
        })
        .catch(error => {
            console.error('Error fetching suggestion:', error);
        });
}

// Call fetchSuggestion every 3 seconds to update suggestion dynamically
setInterval(fetchSuggestion, 3000);



