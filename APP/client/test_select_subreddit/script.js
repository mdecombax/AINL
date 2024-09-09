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

function displayContent(rawHtml) {
  const contentDiv = document.getElementById('newsletterContent');
  contentDiv.innerHTML = rawHtml;
  contentDiv.classList.remove('hidden');
}

function hideAllExceptNavAndFooter() {
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
function showLoadingOverlay() {
  document.getElementById('loadingOverlay').classList.remove('hidden');
}

// Fonction pour masquer l'overlay de chargement
function hideLoadingOverlay() {
  document.getElementById('loadingOverlay').classList.add('hidden');
}

// Fonction pour masquer le contenu principal (garder le header et le footer)
function hideMainContent() {
  document.getElementById('main_content').classList.add('hidden');

}

// Fonction pour afficher les articles sous forme de cards
function displayArticles(articles) {
  hideMainContent(); // Masquer tout sauf le header et le footer

  const container = document.createElement('div');
  container.className = 'container mx-auto py-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'; // Classes Tailwind pour la mise en page

  // Créer une card pour chaque article
  articles.forEach(article => {
      const card = document.createElement('div');
      card.className = 'bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300 cursor-pointer';

      // Ajout de l'état de sélection
      card.addEventListener('click', () => {
          card.classList.toggle('bg-blue-100'); // Toggle de la couleur
          card.classList.toggle('selected'); // Ajouter ou retirer la classe 'selected'
      });

      const title = document.createElement('h3');
      title.className = 'text-xl font-bold mb-4';
      title.textContent = article.post_title;

      const subreddit = document.createElement('p');
      subreddit.className = 'text-gray-500 text-sm mb-2';
      subreddit.textContent = `${article.subreddit}`;

      const link = document.createElement('p');
      link.className = 'text-blue-500 hover:underline';
      link.textContent = 'Voir plus'; // Pas de redirection

      card.appendChild(title);
      card.appendChild(subreddit);
      card.appendChild(link);
      container.appendChild(card);
  });

  // Ajouter le container des cards dans le body, avant le footer
  const footer = document.querySelector('footer');
  document.body.insertBefore(container, footer);

  // Afficher le bouton de confirmation après l'affichage des articles
  const confirmBtn = document.getElementById('confirmSelectionBtn');
  confirmBtn.classList.remove('hidden');
}


document.getElementById('confirmSelectionBtn').addEventListener('click', () => {
  const selectedCards = document.querySelectorAll('.selected'); // Get all selected cards
  // Use a Set to ensure uniqueness of selected subreddits
  const selectedSubreddits = new Set();

  selectedCards.forEach(card => {
    const subreddit = card.querySelector('p').textContent;
    console.log(subreddit); // Log the subreddit
    selectedSubreddits.add(subreddit); // Add each subreddit to the Set
  });
  if (selectedSubreddits.size > 0) {
      // Show loading overlay while waiting for the API response
      showLoadingOverlay();
      
      // Construct the API URL with selected subreddits
      const subredditString = Array.from(selectedSubreddits).join(',');
      
      const apiUrl = `http://127.0.0.1:8000/newsletter_from_subreddits/?subreddits=${encodeURIComponent(subredditString)}`;

      // Perform the fetch request with custom header
      fetch(apiUrl)
      .then(response => response.json()) // Assuming the response is in HTML format
      .then(data => {
          console.log(data);
          const rawHtml = marked.parse(data);
          console.log(rawHtml)
          // Hide loading overlay after the response is received
          hideAllExceptNavAndFooter();
          // Display the fetched content
          hideLoadingOverlay();
          displayContent(rawHtml);
      })
      .catch(error => {
          console.error('Erreur lors de la requête API:', error);
          hideLoadingOverlay(); // Hide the overlay in case of an error
      });
  } else {
      alert('Veuillez sélectionner au moins un subreddit.');
  }
});

// Fonction pour gérer l'appel à l'API et afficher les articles
async function generateNewsletter(theme) {
  try {
      // Affiche l'overlay de chargement
      showLoadingOverlay();

      // Simuler l'appel à l'API (ici tu mettras l'appel réel à l'API)
      const response = await fetch('http://127.0.0.1:8000/posts_from_theme/?keyword=' + theme);
      const data = await response.json();
      const dataeval = await eval(data)

      // Ajouter un log pour vérifier la structure des données
      console.log('Réponse de l\'API:', typeof(dataeval));
      console.log('Données reçues:', dataeval);

      // Masquer l'overlay après la réponse de l'API
      hideAllExceptNavAndFooter();

      // Si data est un tableau, on peut afficher les articles
      if (Array.isArray(dataeval)) {
          displayArticles(dataeval);
      } else {
          console.error('La réponse API n\'est pas un tableau');
      }
  } catch (error) {
      console.error('Erreur lors de la génération de la newsletter', error);
      hideLoadingOverlay(); // Masquer l'overlay même en cas d'erreur
  }
}

// Gestion du formulaire de thème
document.getElementById('themeForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const theme = document.getElementById('themeInput').value;
  generateNewsletter(theme); // Appel à la fonction de génération de newsletter
});
