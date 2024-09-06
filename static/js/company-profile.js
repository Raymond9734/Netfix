document.addEventListener('DOMContentLoaded', function() {
    const editCompanyInfoBtn = document.getElementById('editCompanyInfo');
    const manageServicesBtn = document.getElementById('manageServices');
    const addReviewBtn = document.getElementById('addReview');
    const companyServices = document.getElementById('companyServices');
    const customerReviews = document.getElementById('customerReviews');
  
    
    editCompanyInfoBtn.addEventListener('click', function() {
        // Placeholder for edit company info functionality
        alert('Edit company info functionality will be implemented here.');
    });
  
    manageServicesBtn.addEventListener('click', function() {
        companyServices.readOnly = !companyServices.readOnly;
        this.textContent = companyServices.readOnly ? 'Edit Services' : 'Save Services';
    });
  
    addReviewBtn.addEventListener('click', function() {
        const reviewText = prompt('Enter your review:');
        if (reviewText) {
            const reviewElement = document.createElement('div');
            reviewElement.className = 'review';
            reviewElement.innerHTML = `
                <p>${reviewText}</p>
                <small>Anonymous - ${new Date().toLocaleDateString()}</small>
            `;
            customerReviews.appendChild(reviewElement);
        }
    });
  
   
  
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