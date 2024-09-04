import { displayContent, enableGenerateButton, hideLoadingOverlay, hideLandingContent, handleError } from './ui.js';

// Fetch the newsletter content from the API
export function fetchNewsletter() {
    fetch('http://127.0.0.1:8000/newsletter/?subreddit=startups', {
        headers: { "ngrok-skip-browser-warning": "69420" }
    })
    .then(response => response.json())
    .then(data => {
        enableGenerateButton();
        const rawHtml = marked.parse(data);
        displayContent(rawHtml);
        hideLoadingOverlay();
        hideLandingContent();
    }) 
    .catch(error => {
        handleError(error);
    });
}
