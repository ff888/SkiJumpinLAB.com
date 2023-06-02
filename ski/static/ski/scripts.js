// Get the navbar links
var navbarLinks = document.querySelectorAll('.nav-link');

// Attach a click event listener to each navbar link
navbarLinks.forEach(function (link) {
    link.addEventListener('click', function (event) {
        // Prevent the default link behavior
        event.preventDefault();

        // Show the spinner when a navbar link is clicked
        document.getElementById('loader').style.display = 'block';

        // Perform the navigation (e.g., change the page content)
        var targetUrl = link.getAttribute('href');
        fetch(targetUrl)
            .then(function (response) {
                // Check if the response was successful (status code between 200 and 299)
                if (response.ok) {
                    // Assuming the response is HTML, extract the content from the response
                    return response.text();
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
            .then(function (htmlContent) {
                // Create a temporary element to hold the retrieved HTML content
                var tempElement = document.createElement('div');
                tempElement.innerHTML = htmlContent;

                // Update the 'content' element with the retrieved element
                var newContentElement = tempElement.querySelector('#content');
                if (newContentElement) {
                    var currentContentElement = document.getElementById('content');
                    currentContentElement.innerHTML = newContentElement.innerHTML;
                }

                // Hide the spinner after the content has been loaded
                document.getElementById('loader').style.display = 'none';
            })
            .catch(function (error) {
                // Handle any errors that occurred during the fetch request
                console.error('An error occurred:', error);
            });
    });
});
