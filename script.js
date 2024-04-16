document.addEventListener('DOMContentLoaded', function() {
    // Attach the event listener to the form submission
    document.getElementById('ingredientForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        fetchProtein(); // Call the function to fetch protein based on user selections
        fetchAdditions(); // Additionally, fetch additions based on user selections
    });
});

function fetchProtein() {
    // Collect exclusion criteria and quantity from the form for proteins
    const queryString = new URLSearchParams({
        is_red_meat: document.getElementById('is_red_meat').checked,
        is_pork: document.getElementById('is_pork').checked,
        is_poultry: document.getElementById('is_poultry').checked,
        is_fish: document.getElementById('is_fish').checked,
        is_shellfish: document.getElementById('is_shellfish').checked,
        is_kosher: document.getElementById('is_kosher').checked,
        quantity: document.getElementById('protein_quantity').value
    }).toString();

    // Update the URL to point to your deployed backend server
    fetch(`https://162.233.27.149:80/api/protein?${queryString}`)
        .then(response => response.json())
        .then(data => displayProtein(data)) // Display the fetched proteins
        .catch(error => console.error('Error fetching protein:', error));
}

function displayProtein(protein) {
    const resultsDiv = document.getElementById('results'); // Ensure this div exists in your HTML
    resultsDiv.innerHTML = ''; // Clear previous results

    if (protein.length === 0) {
        resultsDiv.innerHTML = '<p>No proteins found based on the selected criteria.</p>';
        return;
    }

    protein.forEach(p => {
        const element = document.createElement('p');
        element.textContent = p.name; // Assuming the objects have a 'name' property
        resultsDiv.appendChild(element);
    });
}

function fetchAdditions() {
    // Collect criteria and quantity from the form for additions
    const queryString = new URLSearchParams({
        is_kosher: document.getElementById('is_kosher').checked,
        // Add other relevant criteria for additions here
        additions_quantity: document.getElementById('additions_quantity').value
    }).toString();

    // Update the URL to point to your deployed backend server
    fetch(`https://162.233.27.149:80/api/additions?${queryString}`)
        .then(response => response.json())
        .then(data => displayAdditions(data)) // Display the fetched additions
        .catch(error => console.error('Error fetching additions:', error));
}

function displayAdditions(additions) {
    const additionsDiv = document.getElementById('additions-results'); // Ensure this div exists in your HTML
    additionsDiv.innerHTML = ''; // Clear previous results

    if (additions.length === 0) {
        additionsDiv.innerHTML = '<p>No additions found based on the selected criteria.</p>';
        return;
    }

    additions.forEach(addition => {
        const element = document.createElement('p');
        element.textContent = addition.name; // Assuming the objects have a 'name' property
        additionsDiv.appendChild(element);
    });
}
