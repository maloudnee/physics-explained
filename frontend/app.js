const userInput = document.getElementById('userInput');
const explainBtn = document.getElementById('explainBtn');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');
const resultSection = document.getElementById('resultSection');
const inputSection = document.querySelector('.container');
const backBtn = document.getElementById('backBtn');
const conceptHeading = document.getElementById('conceptHeading');


function fadeTo(from, to){
    from.classList.add('hidden');
    setTimeout(() => {
        from.style.display = 'none';
        to.style.display = 'flex';
        requestAnimationFrame(() => {
            to.classList.remove('hidden');
        })
    }, 800);
}
explainBtn.addEventListener('click', async () => {
    const concept = userInput.value.trim();
    if(!concept){
        alert('Please enter a concept!');
        return;
    }

    conceptHeading.textContent = concept;
    resultsDiv.innerHTML = '';

    fadeTo(inputSection, loadingDiv);

    try {
        const response = await fetch('https://localhost:5000/api/explain', {
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

        // Converting markdown text to HTML
        resultsDiv.innerHTML = marked.parse(data.explanation);
    } catch (error) {
        resultsDiv.innerHTML = '<p class="error">Oops! Something went wrong. Please try again. </p>';
        console.error('Error:', error);
    } finally {
        fadeTo(loadingDiv, resultSection);
    }
});

backBtn.addEventListener('click', () => {
    userInput.value = '';
    resultsDiv.innerHTML = '';
    fadeTo(resultSection, inputSection);
})