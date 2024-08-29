

console.log("Script loaded and running.");
console.log(marked.parse('I am using **marked**.'));

const btn = document.getElementById('generateBtn');
const loadingDiv = document.getElementById('loadingMessage');
const contentDiv = document.getElementById('newsletterContent');

const messages = [
    "Récupération de l'ensemble d'internet...",
    "Consultation de Steve Jobs pour synthétiser...",
    "Déploiement des nanobots pour écrire la newsletter...",
    "Invoquer des daemons pour traiter les données...",
    "Création d'un café virtuel pour les développeurs..."
];
let messageIndex = 0;

function jsonToMarkdown(json) {
    // This is a simplistic conversion for demonstration purposes.
    // You would expand this function to suit the specific structure of your JSON and the desired Markdown formatting.
    let markdown = '';
    for (let key in json) {
        if (json.hasOwnProperty(key)) {
            markdown += `${json[key]}\n\n`;
        }
    }
    return markdown;
}

function formatMarkdown(markdownText) {
    // This regex finds all markdown headers and adds a newline before them
    const formattedText = markdownText.replace(/(#+\s+)/g, '\n\n$1');
    return formattedText;
}
document.getElementById('generateBtn').addEventListener('click', function() {
    document.getElementById('loadingOverlay').classList.remove('hidden');
    document.body.style.overflow = 'hidden'; // Empêche le défilement
    startLoadingAnimation();
    contentDiv.innerHTML = ''; // Clear previous content
    btn.disabled = true;

    fetch('http://127.0.0.1:8000/newsletter/?subreddit=DaftPunk',{
        headers: {"ngrok-skip-browser-warning" : "69420"}
    })
        .then(response => response.json())
        .then(data => {
            btn.disabled = false;
            const rawHtml = marked.parse(data);
            contentDiv.innerHTML = rawHtml;
            contentDiv.classList.remove('hidden');
            
            // Cacher l'écran de chargement
            document.getElementById('loadingOverlay').classList.add('hidden');
            document.body.style.overflow = 'auto';
            
            // Cacher le contenu de la landing page
            document.getElementById('landing-content').style.display = 'none';
        })
        .catch(error => {
            console.log("error : " + error)
            loadingDiv.textContent = 'Failed to generate newsletter: ' + error;
            btn.disabled = false;
            
            // Ajoutez également ces lignes dans le bloc catch
            document.getElementById('loadingOverlay').classList.add('hidden');
            document.body.style.overflow = 'auto';
        });
});
function createParticle() {
  const particle = document.createElement('div');
  particle.className = 'absolute bg-white rounded-full opacity-0';
  particle.style.width = '4px';
  particle.style.height = '4px';
  particle.style.left = Math.random() * 100 + '%';
  particle.style.top = Math.random() * 100 + '%';
  document.getElementById('particleContainer').appendChild(particle);

  anime({
    targets: particle,
    opacity: [0, 0.5, 0],
    scale: [0, 1],
    translateX: anime.random(-50, 50),
    translateY: anime.random(-50, 50),
    duration: anime.random(1000, 3000),
    easing: 'easeOutExpo',
    complete: () => {
      particle.remove();
      createParticle();
    }
  });
}

function startLoadingAnimation() {
  const loadingMessages = [
    "Extraction de données depuis le futur lointain...",
    "Interception de signaux extraterrestres...",
    "Récupération des écrits perdus de la bibliothèque d'Alexandrie...",
    "Analyse des rêves des visionnaires...",
    "Piratage des pensées de génies disparus...",
    "Décodage des murmures des anciens arbres...",
    "Siphonnage des flux de conscience des philosophes...",
    "Capture des échos du Big Bang...",
    "Extraction de savoirs cachés dans les cavernes les plus profondes...",
    "Récolte des idées qui flottent dans l'atmosphère de Jupiter..."
  ];

  let currentIndex = 0;
  const messageElement = document.querySelector("#loadingOverlay h2");
  const progressBar = document.getElementById('progressBar');
  let progress = 0;

  function updateMessage() {
    anime({
      targets: messageElement,
      opacity: [1, 0],
      duration: 500,
      easing: 'easeOutExpo',
      complete: () => {
        messageElement.textContent = loadingMessages[currentIndex];
        anime({
          targets: messageElement,
          opacity: [0, 1],
          duration: 500,
          easing: 'easeInExpo'
        });
        currentIndex = (currentIndex + 1) % loadingMessages.length;
      }
    });
  }

  function updateProgressBar() {
    const duration = 7000; // 15 secondes
    const interval = 100; // Mise à jour toutes les 100ms
    const steps = duration / interval;
    const increment = 100 / steps;

    const progressAnimation = anime.timeline({
      duration: duration,
      easing: 'easeInOutQuad',
      update: function(anim) {
        progress = anim.progress;
        progressBar.style.width = `${progress}%`;
      }
    });

    for (let i = 0; i < steps; i++) {
      progressAnimation.add({
        duration: interval,
        progress: increment * (i + 1),
        easing: function() {
          return Math.random() * 0.9 + 0.1; // Variation aléatoire de la vitesse
        }
      });
    }
  }

  updateMessage();
  setInterval(updateMessage, 10000);
  updateProgressBar();

  for (let i = 0; i < 50; i++) {
    createParticle();
  }
}