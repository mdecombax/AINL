

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

btn.addEventListener('click', function() {
    contentDiv.innerHTML = ''; // Clear previous content
    btn.disabled = true;

    // Start loading messages
    let messageInterval = setInterval(function() {
        loadingDiv.textContent = messages[messageIndex++];
        if (messageIndex >= messages.length) messageIndex = 0;
    }, 5000);

    // fetch("https://5741-34-79-1-11.ngrok-free.app/newsletters")
    fetch('https://3082-34-140-83-82.ngrok-free.app/newsletter/?subreddit=artificial',{
        headers: {"ngrok-skip-browser-warning" : "69420"}
    })
        .then(response => response.json())
        .then(data => {
            clearInterval(messageInterval);
            btn.disabled = false;
            const rawHtml = marked.parse(data);
            contentDiv.innerHTML = rawHtml;
            contentDiv.classList.remove('hidden');
        })
        .catch(error => {
            console.log("error : " + error)
            clearInterval(messageInterval);
            loadingDiv.textContent = 'Failed to generate newsletter: ' + error;
            btn.disabled = false;
        });
});
