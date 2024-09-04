// Create an animated particle for the background effect
export function createParticle() {
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

// Animate the progress bar during the loading phase
function animateProgressBar() {
    const progressBar = document.getElementById('progressBar');
    const duration = 7000; // 7 seconds
    const interval = 100; // Update every 100ms
    const steps = duration / interval;
    const increment = 100 / steps;

    anime.timeline({
        duration: duration,
        easing: 'easeInOutQuad',
        update: function (anim) {
            progressBar.style.width = `${anim.progress}%`;
        }
    });
}

// Update the loading message with a fade-in/out effect
function updateLoadingMessage(messages, currentIndex) {
    const messageElement = document.querySelector("#loadingOverlay h2");

    anime({
        targets: messageElement,
        opacity: [1, 0],
        duration: 100,
        easing: 'easeOutExpo',
        complete: () => {
            messageElement.textContent = messages[currentIndex];
            anime({
                targets: messageElement,
                opacity: [0, 1],
                duration: 500,
                easing: 'easeInExpo'
            });
        }
    });
}

// Start the loading animation (messages, progress bar, and particles)
export function startLoadingAnimation() {
    const loadingMessages = [
        "Extraction de données depuis le futur lointain...",
        "Interception de signaux extraterrestres...",
        "Récupération des écrits perdus de la bibliothèque d'Alexandrie...",
        "Analyse des rêves des visionnaires...",
        // Add more messages as needed
    ];

    let currentIndex = 0;

    updateLoadingMessage(loadingMessages, currentIndex);
    setInterval(() => {
        currentIndex = (currentIndex + 1) % loadingMessages.length;
        updateLoadingMessage(loadingMessages, currentIndex);
    }, 10000);

    animateProgressBar();

    // Create multiple particles for the background effect
    for (let i = 0; i < 50; i++) {
        createParticle();
    }
}
