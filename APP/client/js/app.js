console.log(marked.parse('I am using **marked**.'));


// Import necessary functions
import { showLoadingOverlay, prepareForContentLoad, hideLoadingOverlay, enableGenerateButton, displayContent, handleError, hideLandingContent } from './ui.js';
import { startLoadingAnimation } from './animation.js';
import { fetchNewsletter } from './fetch.js';

// Attach click event listener to the generate button
const btn = document.getElementById('generateBtn');

btn.addEventListener('click', function () {
    showLoadingOverlay();
    prepareForContentLoad();
    startLoadingAnimation();
    fetchNewsletter();
});
