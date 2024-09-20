function createLeaves() {
    const background = document.querySelector('.animated-background');
    const numberOfLeaves = 20;
    
    for (let i = 0; i < numberOfLeaves; i++) {
      const leaf = document.createElement('div');
      leaf.classList.add('leaf');
      leaf.style.left = `${Math.random() * 100}%`;
      leaf.style.top = `${Math.random() * 100}%`;
      const size = Math.random() * 30 + 20;
      leaf.style.width = `${size}px`;
      leaf.style.height = `${size}px`;
      leaf.style.animationDuration = `${Math.random() * 10 + 10}s`;
      leaf.style.animationDelay = `${Math.random() * 5}s`;
      leaf.style.animation = `float ${leaf.style.animationDuration} ease-in-out infinite`;
      background.appendChild(leaf);
    }
  }
  
  
  window.addEventListener('load', () => {
    createLeaves();
  });