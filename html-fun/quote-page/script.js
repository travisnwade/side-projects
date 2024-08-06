window.onload = function() {
    fetch('quotes.txt')
        .then(response => response.text())
        .then(data => {
            const quotes = data.split('\n').filter(quote => quote.trim() !== '');
            const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
            document.getElementById('quote').textContent = randomQuote;
        })
        .catch(error => console.error('Error fetching quotes:', error));
};
