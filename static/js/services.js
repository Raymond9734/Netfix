document.getElementById('sort-select').addEventListener('change', function () {
    const sortBy = this.value;
    const serviceContainer = document.getElementById('services-container');
    const serviceCards = Array.from(serviceContainer.children);

    serviceCards.sort((a, b) => {
        if (sortBy === 'newest' || sortBy === 'oldest') {
            const dateA = new Date(a.querySelector('.posted-date').textContent.split('Posted on: ')[1]);
            const dateB = new Date(b.querySelector('.posted-date').textContent.split('Posted on: ')[1]);

            return sortBy === 'newest' ? dateB - dateA : dateA - dateB;
        } else if (sortBy === 'oldest') {
            // Sort by the oldest date
            return new Date(a.querySelector('.posted-date').textContent.split('Posted on: ')[1]) - new Date(b.querySelector('.posted-date').textContent.split('Posted on: ')[1]);
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
