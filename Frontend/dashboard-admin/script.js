const counters = document.querySelectorAll('.stat-value');

counters.forEach(counter => {
  const updateCount = () => {
    const target = +counter.getAttribute('data-target');
    const current = +counter.innerText.replace(/,/g, '') || 0;
    const remaining = target - current;

    // Rumus 
    const increment = Math.ceil(remaining / 10);

    if (current < target) {
      counter.innerText = (current + increment).toLocaleString('id-ID');
      setTimeout(updateCount, 100); // interval 40ms antar update
    } else {
      counter.innerText = target.toLocaleString('id-ID');
    }
  };

  updateCount();
});
