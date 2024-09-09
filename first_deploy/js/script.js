import {showLoadingOverlay, hideLoadingOverlay, displayContent, hideAllExceptNavAndFooter, prepareForContentLoad} from "./ui.js";
import {startLoadingAnimation} from "./loading.js";
import {generateNewsletter} from "./fetch.js";

console.log(marked.parse('I am using **marked**.'));

// Toggle du menu hamburger pour mobile
const menuBtn = document.getElementById('menuBtn');
const mobileMenu = document.getElementById('mobileMenu');

menuBtn.addEventListener('click', () => {
  if (mobileMenu.classList.contains('hidden')) {
    mobileMenu.classList.remove('hidden');
    mobileMenu.style.maxHeight = mobileMenu.scrollHeight + 'px';
  } else {
    mobileMenu.style.maxHeight = '0';
    setTimeout(() => {
      mobileMenu.classList.add('hidden');
    }, 300);
  }
});

// Gestion du formulaire de thème
document.getElementById('themeForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const subreddit = document.getElementById('themeInput').value;
  generateNewsletter(subreddit); // Appel à la fonction de génération de newsletter
});











