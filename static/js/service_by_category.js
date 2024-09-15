const services = JSON.parse(document.getElementById('services-data').textContent);
const categories = JSON.parse(document.getElementById('categories-data').textContent);
const isCustomer = JSON.parse(document.getElementById('is-customer').textContent);

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
    container.innerHTML = '';  // Clear previous content
    services.sort((a, b) => b.id - a.id).forEach(service => {
        const card = document.createElement('div');
        card.className = 'service-card';
        let requestServiceLink = `<p><strong>Posted by:</strong> ${service.company.username}</p>`;

        // Only render the "Request Service" link if the user is a customer
        if (isCustomer) {
            requestServiceLink = `<a href="/services/request_service/${service.company.username}/${service.id}/">Request Service</a>`;
        }

        // Reset fill variables before assigning new values based on rating
        let fill1 = "", fill2 = "", fill3 = "", fill4 = "", fill5 = "";
        
        switch (Number(service.rating)) {
            case 1:
                fill1 = 'filled';
                break;
            case 2:
                fill1 = 'filled';
                fill2 = 'filled';
                break;
            case 3:
                fill1 = 'filled';
                fill2 = 'filled';
                fill3 = 'filled';
                break;
            case 4:
                fill1 = 'filled';
                fill2 = 'filled';
                fill3 = 'filled';
                fill4 = 'filled';
                break;
            case 5:
                fill1 = 'filled';
                fill2 = 'filled';
                fill3 = 'filled';
                fill4 = 'filled';
                fill5 = 'filled';
                break;
        }

        card.innerHTML = `
            <h2>${service.name}</h2>
            <p>${service.description}</p>
            <p>Category: ${service.field}</p>
            <p>Price per hour: $${service.price_hour}</p>
            <div class="star-rating">
                <span class="star ${fill1}">★</span>
                <span class="star ${fill2}">★</span>
                <span class="star ${fill3}">★</span>
                <span class="star ${fill4}">★</span>
                <span class="star ${fill5}">★</span>
            </div>
            ${requestServiceLink}
        `;
        container.appendChild(card);
    });
}

function renderServicesByCategory(categoryId) {
    const container = document.getElementById('service-container');
    container.innerHTML = '';  // Clear previous content
    const filteredServices = services.filter(service => service.field === categoryId);
    if (filteredServices.length === 0) {
        const err = document.createElement('div');
        err.textContent = `No services found in ${categories.find(c => c.id === categoryId).name} category`;
        container.appendChild(err);
        return;
    }

    filteredServices.forEach(service => {
        const card = document.createElement('div');
        card.className = 'service-card';
        let requestServiceLink = `<p><strong>Posted by:</strong> ${service.company.username}</p>`;

        if (isCustomer) {
            const requestServiceUrl = `/services/request_service/${service.company.username}/${service.id}/`;
            requestServiceLink = `<a href="${requestServiceUrl}">Request Service</a>`;
        }

        // Reset fill variables before assigning new values based on rating
        let fill1 = "", fill2 = "", fill3 = "", fill4 = "", fill5 = "";

        switch (Number(service.rating)) {
            case 1:
                fill1 = 'filled';
                break;
            case 2:
                fill1 = 'filled';
                fill2 = 'filled';
                break;
            case 3:
                fill1 = 'filled';
                fill2 = 'filled';
                fill3 = 'filled';
                break;
            case 4:
                fill1 = 'filled';
                fill2 = 'filled';
                fill3 = 'filled';
                fill4 = 'filled';
                break;
            case 5:
                fill1 = 'filled';
                fill2 = 'filled';
                fill3 = 'filled';
                fill4 = 'filled';
                fill5 = 'filled';
                break;
        }

        card.innerHTML = `
            <h2>${service.name}</h2>
            <p>${service.description}</p>
            <p>Price per hour: $${service.price_hour}</p>
            <div class="star-rating">
                <span class="star ${fill1}">★</span>
                <span class="star ${fill2}">★</span>
                <span class="star ${fill3}">★</span>
                <span class="star ${fill4}">★</span>
                <span class="star ${fill5}">★</span>
            </div>
            ${requestServiceLink}
        `;
        container.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    renderCategories();
    renderAllServices();
});
