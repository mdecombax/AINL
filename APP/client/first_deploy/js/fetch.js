// Fonction pour gérer l'appel à l'API et afficher les articles
export async function generateNewsletter(subreddit) {
    showLoadingOverlay()
    const apiUrl = `http://127.0.0.1:8000/test/?subreddits=${encodeURIComponent(subreddit)}`;
  
    prepareForContentLoad();
    startLoadingAnimation();    
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
        })
  }
  