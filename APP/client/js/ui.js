// Show loading overlay and disable scrolling
export function showLoadingOverlay() {
    document.getElementById('loadingOverlay').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Hide loading overlay and re-enable scrolling
export function hideLoadingOverlay() {
    document.getElementById('loadingOverlay').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Clear the content and disable the generate button
export function prepareForContentLoad() {
    const contentDiv = document.getElementById('newsletterContent');
    contentDiv.innerHTML = '';
    const btn = document.getElementById('generateBtn');
    btn.disabled = true;
}

// Enable the generate button after content is loaded or on error
export function enableGenerateButton() {
    const btn = document.getElementById('generateBtn');
    btn.disabled = false;
}

// Display the fetched HTML content in the page
export function displayContent(rawHtml) {
    const contentDiv = document.getElementById('newsletterContent');
    contentDiv.innerHTML = rawHtml;
    contentDiv.classList.remove('hidden');
}

// Handle the fetch error by logging it and displaying a message
export function handleError(error) {
    const loadingDiv = document.getElementById('loadingMessage');
    console.error("Error fetching newsletter: ", error);
    loadingDiv.textContent = 'Failed to generate newsletter: ' + error;
    hideLoadingOverlay();
    enableGenerateButton();
}

// Hide the landing page content after the newsletter is loaded
export function hideLandingContent() {
    document.getElementById('landing-content').style.display = 'none';
}
