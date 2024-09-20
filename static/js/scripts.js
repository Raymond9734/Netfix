document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('mobile-menu');
    const navbar = document.querySelector('.navbar');
    const icon = menuToggle.querySelector('i'); // Icon inside the toggle
    menuToggle.addEventListener('click', function() {
        // Toggle the menu visibility
        if (navbar.classList.contains('menu-active')) {
            // Slide up the menu and change the icon back to bars
            navbar.classList.remove('menu-active');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        } else {
            // Slide down the menu and change the icon to times (close)
            navbar.classList.add('menu-active');
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        }
    });
});
