document.addEventListener("DOMContentLoaded", function () {
    const logoutMessage = document.querySelector(".logout-text");
    const homeLink = document.querySelector(".logout-home-link");

    // Ensure elements exist before trying to modify them
    if (logoutMessage && homeLink) {
        // Example: Change logout message after a few seconds
        setTimeout(function () {
            logoutMessage.textContent = "You have successfully logged out!";
        }, 2000);

        // Example: Fade-out effect before redirect
        homeLink.addEventListener("click", function (event) {
            event.preventDefault(); // Stop immediate navigation
            logoutMessage.textContent = "Redirecting to the homepage...";
            document.body.style.opacity = 0.7; // Fade effect
            setTimeout(function () {
                window.location.href = homeLink.href; // Navigate after delay
            }, 1500);
        });
    } else {
        console.error('Required elements not found in the DOM.');
    }
});
