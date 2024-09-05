new Vue({
    el: '#app',
    data: {
      activeView: 'browse',
      showMobileMenu: false,
      searchQuery: '',
      services: [
        { id: 1, name: 'Plumbing', description: 'Professional plumbing services for all your needs.', image: 'https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cGx1bWJpbmd8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60' },
        { id: 2, name: 'Electrical', description: 'Expert electrical work for your home or business.', image: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8ZWxlY3RyaWNhbHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60' },
        { id: 3, name: 'Carpentry', description: 'Custom woodwork and repairs by skilled carpenters.', image: 'https://images.unsplash.com/photo-1617104424032-b9bd6972d0e4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8Y2FycGVudHJ5fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60' },
        { id: 4, name: 'Landscaping', description: 'Transform your outdoor space with our landscaping services.', image: 'https://images.unsplash.com/photo-1600715723712-d2967b17cae9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8bGFuZHNjYXBpbmd8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60' },
        { id: 5, name: 'Painting', description: 'Interior and exterior painting services for your home.', image: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8cGFpbnRpbmclMjBob3VzZXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60' },
        { id: 6, name: 'Cleaning', description: 'Professional cleaning services for homes and offices.', image: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8Y2xlYW5pbmd8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60' }
      ],
      requestForm: {
        serviceType: '',
        description: '',
        location: ''
      },
      offerForm: {
        serviceName: '',
        serviceDescription: '',
        serviceArea: '',
        pricing: ''
      },
      showNotification: false,
      notificationMessage: '',
      newsletter: {
        email: ''
      },
      isLoggedIn: false,
      loginForm: {
        email: '',
        password: ''
      },
      signupForm: {
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    },
    computed: {
      filteredServices() {
        return this.services.filter(service =>
          service.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          service.description.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
    },
    methods: {
      toggleMobileMenu() {
        this.showMobileMenu = !this.showMobileMenu;
      },
      requestService(service) {
        this.activeView = 'request';
        this.requestForm.serviceType = service.name;
      },
      submitRequest() {
        // Here you would typically send the form data to a server
        console.log('Service request submitted:', this.requestForm);
        this.showNotification = true;
        this.notificationMessage = 'Service request submitted successfully!';
        setTimeout(() => {
          this.showNotification = false;
        }, 3000);
        this.requestForm = { serviceType: '', description: '', location: '' };
      },
      submitOffer() {
        // Here you would typically send the form data to a server
        console.log('Service offer submitted:', this.offerForm);
        this.showNotification = true;
        this.notificationMessage = 'Service offer submitted successfully!';
        setTimeout(() => {
          this.showNotification = false;
        }, 3000);
        this.offerForm = { serviceName: '', serviceDescription: '', serviceArea: '', pricing: '' };
      },
      subscribeNewsletter() {
        // Here you would typically send the email to a server for newsletter subscription
        console.log('Newsletter subscription:', this.newsletter.email);
        this.showNotification = true;
        this.notificationMessage = 'Thank you for subscribing to our newsletter!';
        setTimeout(() => {
          this.showNotification = false;
        }, 3000);
        this.newsletter.email = '';
      },
      login() {
        // Here you would typically send the login credentials to a server for authentication
        console.log('Login attempt:', this.loginForm);
        this.isLoggedIn = true;
        this.showNotification = true;
        this.notificationMessage = 'Logged in successfully!';
        setTimeout(() => {
          this.showNotification = false;
        }, 3000);
        this.activeView = 'browse';
        this.loginForm = { email: '', password: '' };
      },
      signup() {
        // Here you would typically send the signup information to a server
        if (this.signupForm.password !== this.signupForm.confirmPassword) {
          this.showNotification = true;
          this.notificationMessage = 'Passwords do not match!';
          setTimeout(() => {
            this.showNotification = false;
          }, 3000);
          return;
        }
        console.log('Signup attempt:', this.signupForm);
        this.isLoggedIn = true;
        this.showNotification = true;
        this.notificationMessage = 'Signed up successfully!';
        setTimeout(() => {
          this.showNotification = false;
        }, 3000);
        this.activeView = 'browse';
        this.signupForm = { name: '', email: '', password: '', confirmPassword: '' };
      },
      logout() {
        this.isLoggedIn = false;
        this.showNotification = true;
        this.notificationMessage = 'Logged out successfully!';
        setTimeout(() => {
          this.showNotification = false;
        }, 3000);
        this.activeView = 'browse';
      }
    }
  });