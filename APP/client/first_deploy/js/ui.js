export function displayContent(rawHtml) {
  const contentDiv = document.getElementById('newsletterContent');
  contentDiv.innerHTML = rawHtml;
  contentDiv.classList.remove('hidden');
}

export function hideAllExceptNavAndFooter() {
  // Sélectionner toutes les divs dans le document
  const allDivs = document.querySelectorAll('div');
  
  // Boucle à travers toutes les divs et masque celles qui ne sont pas dans le nav ou le footer
  allDivs.forEach(div => {
    const isInNav = div.closest('nav') !== null;
    const isInFooter = div.closest('footer') !== null;

    if (!isInNav && !isInFooter) {
      div.classList.add('hidden'); // Masquer la div
    }
  });
}

// Fonction pour afficher l'overlay de chargement
export function showLoadingOverlay() {
  document.getElementById('loadingOverlay').classList.remove('hidden');
}

// Fonction pour masquer l'overlay de chargement
export function hideLoadingOverlay() {
  document.getElementById('loadingOverlay').classList.add('hidden');
}

export function prepareForContentLoad() {
    const contentDiv = document.getElementById('newsletterContent');
    contentDiv.innerHTML = '';
  }