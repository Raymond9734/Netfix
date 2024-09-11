document.getElementById('sort-select').addEventListener('change', function () {
    const sortBy = this.value;
    const serviceContainer = document.getElementById('services-container');
    const serviceCards = Array.from(serviceContainer.children);

    serviceCards.sort((a, b) => {
        if (sortBy === 'newest') {
            // Sort by the newest date
            return new Date(b.querySelector('p:nth-of-type(4)').textContent.split('Posted on: ')[1]) - new Date(a.querySelector('p:nth-of-type(4)').textContent.split('Posted on: ')[1]);
        } else if (sortBy === 'oldest') {
            // Sort by the oldest date
            return new Date(a.querySelector('p:nth-of-type(4)').textContent.split('Posted on: ')[1]) - new Date(b.querySelector('p:nth-of-type(4)').textContent.split('Posted on: ')[1]);
        } else if (sortBy === 'name') {
            // Sort by service name
            return a.querySelector('h3').textContent.localeCompare(b.querySelector('h3').textContent);
        } else if (sortBy === 'category') {
            // Sort by category
            const getCategoryText = (element) => {
                const categoryText = element.querySelector('p:nth-of-type(1)').textContent;
                return categoryText.split('Category: ')[1]; // Extract text after "Category: "
            };

            return getCategoryText(a).localeCompare(getCategoryText(b));
        }
    });

    // Clear and re-insert sorted services
    serviceContainer.innerHTML = '';
    serviceCards.forEach(card => serviceContainer.appendChild(card));
});
