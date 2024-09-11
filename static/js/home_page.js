// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('nav ul li a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation to service cards on scroll
    const serviceCards = document.querySelectorAll('.service-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    serviceCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });

    // Add hover effect to most requested services
    const mostRequestedServices = document.querySelectorAll('.most-requested-service');
    mostRequestedServices.forEach(service => {
        service.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#4CAF50';
            this.style.color = '#fff';
        });
        service.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '#fff';
            this.style.color = '#333';
        });
    });

    // Add functionality to search bar
    const searchBar = document.querySelector('.search-bar input');
    const searchButton = document.querySelector('.search-bar button');
    searchButton.addEventListener('click', function() {
        alert('Searching for: ' + searchBar.value);
        // Implement actual search functionality here
    });
});