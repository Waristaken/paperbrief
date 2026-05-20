// Keep track of the selected file globally
let selectedFile = null;

// When user picks a file, store it and show the filename
document.getElementById("fileInput").addEventListener("change", function(e) {
    selectedFile = e.target.files[0];
    
    if (selectedFile) {
        document.getElementById("fileName").textContent = selectedFile.name;
        document.getElementById("analyzeBtn").disabled = false;
    }
});

// Main function that runs when user clicks Analyze
async function analyzePaper() {
    if (!selectedFile) return;

    // Show loading, hide previous results
    document.getElementById("loading").hidden = false;
    document.getElementById("results").hidden = true;
    document.getElementById("analyzeBtn").disabled = true;

    // Build form data — this is how we send a file to the backend
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        // Send the file to our Flask /analyze route
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        // Populate the results into the HTML
        displayResults(data);

    } catch (err) {
        alert("Something went wrong. Check your terminal for errors.");
        console.error(err);
    } finally {
        // Always hide loading when done, whether success or error
        document.getElementById("loading").hidden = true;
        document.getElementById("analyzeBtn").disabled = false;
    }
}

function displayResults(data) {
    // Title and difficulty
    document.getElementById("paperTitle").textContent = data.title;
    document.getElementById("difficultyBadge").textContent = data.difficulty;

    // Problem and summary paragraphs
    document.getElementById("problemText").textContent = data.problem;
    document.getElementById("summaryText").textContent = data.summary;

    // Helper function to populate a <ul> from an array
    function fillList(elementId, items) {
        const ul = document.getElementById(elementId);
        ul.innerHTML = "";
        items.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            ul.appendChild(li);
        });
    }

    fillList("claimsList", data.claims);
    fillList("methodsList", data.methods);
    fillList("findingsList", data.findings);

    // Show the results section
    document.getElementById("results").hidden = false;

    // Scroll down smoothly so user sees the results
    document.getElementById("results").scrollIntoView({ behavior: "smooth" });
}
