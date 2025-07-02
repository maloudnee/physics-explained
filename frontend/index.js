const userInput = document.getElementById('userInput');
const explainBtn = document.getElementById('explainBtn');
const loadingDiv = document.getElementById('loading');
const resultDiv = document.getElementById('results');

explainBtn.addEventListener('click', async () => {
    const concept = userInput.value.trim();
    if(!concept){
        alert('Please enter a concept!');
        return;
    }

    // Show loading, clear previous results
    loadingDiv.classList.remove('hidden');
    resultDiv.innerHTML = '';
    explainBtn.disabled = true;

    try {
        const response = await fetch('https://localhost:3001/api/explain', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ concept: concept }),
        });

        if (!response.ok){
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        document.getElementById('conceptHeading').textContent = concept;

        // Converting markdown text to HTML
        resultsDiv.innerHTML = marked.parse(data.explanation);
    } catch (error) {
        resultDiv.innerHTML = '<p class="error">Oops! Something went wrong. Please try again. </p>';
        console.error('Error:', error);
    } finally {
        // Hide loading and re-enable button
        loadingDiv.classList.add('hidden');
        explainBtn.disabled = false;
    }
});