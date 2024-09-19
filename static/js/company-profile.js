document.addEventListener('DOMContentLoaded', function() {
 
    // Add smooth scroll effect
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
  
    // Add fade-in effect for sections
    const sections = document.querySelectorAll('.profile-details, .services-section, .customer-reviews');
    const fadeInOptions = {
        threshold: 0.1
    };
  
    const fadeInObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            }
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        });
    }, fadeInOptions);
  
    sections.forEach(section => {
        fadeInObserver.observe(section);
    });
  });