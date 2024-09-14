const overlay = document.getElementById('overlay');
const popup = document.getElementById('popup');
const stars = document.querySelectorAll('.star');
const submitReview = document.getElementById('submitReview');
const markComplete = document.getElementById('markComplete');
const successMessage = document.getElementById('successMessage');


let rating = 0;
let csrfToken = document.querySelector('form [name=csrfmiddlewaretoken]').value;

let serviceId = 0

// Function to open the popup and populate it with service details
function openPopup(serviceField, serviceName, address, serviceTime, status, serviceID) {
    document.getElementById('popupServiceName').textContent = serviceName;
    document.getElementById('popupAddress').textContent = address;
    document.getElementById('popupServiceTime').textContent = serviceTime;
    document.getElementById('popupStatus').textContent = status;
    serviceId = serviceID
    overlay.style.display = 'block';
    popup.style.display = 'block';
}

// Function to close the popup
function closePopup() {
    overlay.style.display = 'none';
    popup.style.display = 'none';
}

// Function to handle star rating click and update visual feedback
stars.forEach(star => {
    star.addEventListener('click', () => {
        rating = parseInt(star.getAttribute('data-rating'));
        updateStars();
    });
});

function updateStars() {
    stars.forEach(star => {
        const starRating = parseInt(star.getAttribute('data-rating'));
        star.classList.toggle('active', starRating <= rating);
    });
}

// Submit the review and rating
submitReview.addEventListener('click', () => {
    const review = document.getElementById('review').value.trim();
    if (rating === 0 || review === '') {
        alert('Please provide both a rating and a review before submitting.');
    } else {
        // Prepare the review data to be sent
        const reviewData = {
            rating: rating,
            review: review,
            status: 'completed',
            csrfmiddlewaretoken: csrfToken
        };

        // Make an AJAX request to submit the review
        fetch(`/submit-review/${serviceId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(reviewData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                successMessage.textContent = 'Thank you for your review!';
                successMessage.style.display = 'block';
                setTimeout(() => successMessage.style.display = 'none', 3000);
                closePopup();  // Close the popup after submitting
            } else {
                alert('There was an error submitting your review.');
                console.log(data)
            }
        })
        .catch(error => {
            console.error('Error submitting review:', error);
        });
    }
});

// Mark the service as completed
markComplete.addEventListener('click', () => {
    // Send request to update service status to "Completed"
    fetch(`/mark-service-complete/${serviceId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            status: 'completed',
            csrfmiddlewaretoken: csrfToken
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('popupStatus').textContent = 'Completed';
            document.getElementById('popupStatus').style.color = '#4CAF50';
            markComplete.disabled = true;
            successMessage.textContent = 'Service marked as completed!';
            successMessage.style.display = 'block';
            setTimeout(() => successMessage.style.display = 'none', 3000);
        } else {
            alert('Error marking service as completed.');
        }
    })
    .catch(error => {
        console.error('Error updating service status:', error);
    });
});
