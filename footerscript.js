document.querySelectorAll('.footer-item').forEach(item => {
    item.addEventListener('click', function () {
      document.querySelectorAll('.footer-item').forEach(el => el.classList.remove('active'));
      this.classList.add('active');
    });
  });