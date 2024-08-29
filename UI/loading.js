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

setInterval(() => {
  const loadingMessage = document.querySelector("#loadingOverlay h2");
  loadingMessage.textContent = loadingMessages[currentIndex];
  currentIndex = (currentIndex + 1) % loadingMessages.length;
}, 5000);