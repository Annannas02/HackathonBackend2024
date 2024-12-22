document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search-input");
    const domainFilter = document.getElementById("article-domain-options"); // Reference the dropdown
    const resultsContainer = document.getElementById("results-container");

    async function sendSearchRequest(query, domain) {
        try {
            // Make a POST request to the backend
            document.getElementById("homepage-content-frame").style.height="auto";
            const response = await fetch('http://localhost:5000/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query, // The search query string
                    domain, // The selected domain
                }),
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            console.log("Search request sent successfully!");
        } catch (error) {
            console.error("Error sending search request to backend:", error);
        }
    }

    async function fetchUpdatedArticles() {
        try {
            // Fetch the updated articles from mockData.json
            const response = await fetch('./static/mockData.json'); // Adjust path if needed
            if (!response.ok) {
                throw new Error(`Error fetching articles: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching updated articles from JSON:", error);
            return [];
        }
    }

    async function articleSearch() {
        const query = searchInput.value.trim(); // Get the trimmed search query
        const selectedDomain = domainFilter.value; // Get the selected domain

        // Send the search request to the backend
        await sendSearchRequest(query, selectedDomain);

        // Retrieve all updated articles
        const updatedArticles = await fetchUpdatedArticles();

        // Display the results
        displayResults(updatedArticles);
    }

    function displayResults(results) {
        resultsContainer.innerHTML = ""; // Clear previous results

        if (results.length === 0) {
            resultsContainer.innerHTML = "<div class='no-results'>No results found</div>";
            return;
        }

        results.forEach(item => {
            const resultBox = document.createElement("div");
            resultBox.classList.add("random-box");

            resultBox.innerHTML = `
                <div class="article-box">
                    <div class="article-title">${item.name}</div>
                    <hr class="article-line">
                    <div class="article-abstract text">${item.abstract}</div>
                    <div class="article-date">Created: ${item.date_created} | Updated: ${item.date_updated}</div>
                </div>
            `;

            resultsContainer.appendChild(resultBox);
        });
    }

    // Attach event listeners
    searchInput.addEventListener("input", articleSearch); // Listen for search input
    domainFilter.addEventListener("change", articleSearch); // Listen for dropdown changes
});
const manualSearch = debounceSearch(articleSearch, 300);