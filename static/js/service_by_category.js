const services = JSON.parse(document.getElementById('services-data').textContent);
const categories = JSON.parse(document.getElementById('categories-data').textContent);

// Assuming you have a global variable or a DOM element that contains whether the user is a customer
const isCustomer = JSON.parse(document.getElementById('is-customer').textContent); // You should pass this from your Django template
console.log(isCustomer)
function renderCategories() {
    const container = document.getElementById('category-container');
    categories.forEach(category => {
        const card = document.createElement('div');
        card.className = 'category-card floating';
        card.innerHTML = `
            <h3>${category.name}</h3>
            <p>Click to see services in this category</p>
        `;
        card.addEventListener('click', () => {
            renderServicesByCategory(category.id);
        });
        container.appendChild(card);
    });
}

function renderAllServices() {
    const container = document.getElementById('service-container');
    services.sort((a, b) => b.id - a.id).forEach(service => {
        const card = document.createElement('div');
        card.className = 'service-card';
        let requestServiceLink = `<p><strong>Posted by:</strong> ${service.company.username}</p>`;

        // Only render the "Request Service" link if the user is a customer
        if (isCustomer) {
            requestServiceLink = `<a href="/services/request_service/${service.company.username}/${service.id}/">Request Service</a>`;
        }

        card.innerHTML = `
            <h2>${service.name}</h2>
            <p>${service.description}</p>
            <p>Category: ${service.field}</p>
            <p>Price per hour: $${service.price_hour}</p>
            <p>Rating: ${service.rating}/5</p>
            ${requestServiceLink}  <!-- Conditionally added link -->
        `;
        container.appendChild(card);
    });
}

function renderServicesByCategory(categoryId) {
    const container = document.getElementById('service-container');
    container.innerHTML = ''; 
    const filteredServices = services.filter(service => service.field === categoryId);
    if (filteredServices.length == 0) {
        const err = document.createElement('div');
        err.textContent = `No service found in ${categories.find(c => c.id === categoryId).name} category`
        container.appendChild(err);
        return;
    }

    filteredServices.forEach(service => {
        const card = document.createElement('div');
        card.className = 'service-card';
        let requestServiceLink = `<p><strong>Posted by:</strong> ${service.company.username}</p>`;;
        // Only render the "Request Service" link if the user is a customer
        if (isCustomer) {
            const requestServiceUrl = `/services/request_service/${service.company.username}/${service.id}/`;
            requestServiceLink = `<a href="${requestServiceUrl}">Request Service</a>`;
        }

        card.innerHTML = `
            <h2>${service.name}</h2>
            <p>${service.description}</p>
            <p>Price per hour: $${service.price_hour}</p>
            <p>Rating: ${service.rating}/5</p>
            ${requestServiceLink}  <!-- Conditionally added link -->
        `;
        container.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    renderCategories();
    renderAllServices();
});
