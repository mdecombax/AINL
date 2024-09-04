// Log messages to confirm the script is running and the `marked` library is working
console.log("Script loaded and running.");
console.log(marked.parse('I am using **marked**.'));

// DOM elements selection
const btn = document.getElementById('generateBtn');
const loadingDiv = document.getElementById('loadingMessage');
const contentDiv = document.getElementById('newsletterContent');

// Messages for the loading animation
const messages = [
    "Récupération de l'ensemble d'internet...",
    "Consultation de Steve Jobs pour synthétiser...",
    "Déploiement des nanobots pour écrire la newsletter...",
    "Invoquer des daemons pour traiter les données...",
    "Création d'un café virtuel pour les développeurs..."
];

// Function to convert JSON to Markdown
// This function is simplified; adapt it based on the actual structure of your JSON
function jsonToMarkdown(json) {
    let markdown = '';
    for (let key in json) {
        if (json.hasOwnProperty(key)) {
            markdown += `${json[key]}\n\n`;
        }
    }
    return markdown;
}

// Function to format the markdown by adding newlines before headers
function formatMarkdown(markdownText) {
    return markdownText.replace(/(#+\s+)/g, '\n\n$1');
}

// Function to start the loading animation and fetch the newsletter content
function handleGenerateClick() {
    // Show the loading overlay and disable scrolling
    document.getElementById('loadingOverlay').classList.remove('hidden');
    document.body.style.overflow = 'hidden';

    // Clear previous content and disable the button
    contentDiv.innerHTML = '';
    btn.disabled = true;

    // Start the loading animation
    startLoadingAnimation();

    // Fetch the newsletter content
    fetch('http://127.0.0.1:8000/newsletter/?subreddit=claudeai', {
        headers: { "ngrok-skip-browser-warning": "69420" }
    })
        .then(response => response.json())
        .then(data => {
            // Re-enable the button and display the fetched markdown content
            btn.disabled = false;
            const rawHtml = marked.parse(data);
            contentDiv.innerHTML = rawHtml;
            contentDiv.classList.remove('hidden');

            // Hide the loading overlay and re-enable scrolling
            document.getElementById('loadingOverlay').classList.add('hidden');
            document.body.style.overflow = 'auto';

            // Hide landing content
            document.getElementById('landing-content').style.display = 'none';
        })
        .catch(error => {
            // Handle errors by displaying a message and re-enabling the button
            console.error("Error fetching newsletter: ", error);
            loadingDiv.textContent = 'Failed to generate newsletter: ' + error;
            btn.disabled = false;

            // Ensure loading overlay is hidden and scrolling is re-enabled
            document.getElementById('loadingOverlay').classList.add('hidden');
            document.body.style.overflow = 'auto';
        });
}

// Attach click event listener to the button
btn.addEventListener('click', handleGenerateClick);

// Function to create animated particles for the loading animation
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

// Function to start the loading animation (message and progress bar)
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

    // Update the loading message with a fade-out/fade-in animation
    function updateMessage() {
        anime({
            targets: messageElement,
            opacity: [1, 0],
            duration: 100,
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

    // Animate the progress bar over a 7-second duration
    function updateProgressBar() {
        const duration = 7000;
        const interval = 100;
        const steps = duration / interval;
        const increment = 100 / steps;

        const progressAnimation = anime.timeline({
            duration: duration,
            easing: 'easeInOutQuad',
            update: function (anim) {
                progressBar.style.width = `${anim.progress}%`;
            }
        });

        for (let i = 0; i < steps; i++) {
            progressAnimation.add({
                duration: interval,
                progress: increment * (i + 1),
                easing: function () {
                    return Math.random() * 0.9 + 0.1; // Random speed variation
                }
            });
        }
    }

    // Initial message and progress bar updates
    updateMessage();
    setInterval(updateMessage, 10000);
    updateProgressBar();

    // Create multiple particles for the animation
    for (let i = 0; i < 50; i++) {
        createParticle();
    }
}
