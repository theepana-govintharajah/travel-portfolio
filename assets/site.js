(() => {
  const yearFilters = document.querySelector('#year-filters');
  const countryFilters = document.querySelector('#country-filters');
  if (yearFilters && countryFilters) {
    const yearButtons = [...yearFilters.querySelectorAll('[data-filter]')];
    const countryButtons = [...countryFilters.querySelectorAll('[data-country]')];
    const cards = [...document.querySelectorAll('.trip-card')];
    const status = document.querySelector('#filter-status');
    let year = 'all';
    let country = 'all';
    function update() {
      yearButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === year)));
      countryButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.country === country)));
      let count = 0;
      cards.forEach(card => {
        card.hidden = !((year === 'all' || card.dataset.year === year) &&
                        (country === 'all' || card.dataset.country === country));
        if (!card.hidden) count++;
      });
      if (status) status.textContent = `${count} ${count === 1 ? 'trip' : 'trips'} shown.`;
    }
    yearFilters.hidden = false;
    countryFilters.hidden = false;
    yearFilters.addEventListener('click', event => {
      const button = event.target.closest('button[data-filter]');
      if (!button || !yearFilters.contains(button)) return;
      year = button.dataset.filter;
      update();
    });
    countryFilters.addEventListener('click', event => {
      const button = event.target.closest('button[data-country]');
      if (!button || !countryFilters.contains(button)) return;
      country = button.dataset.country;
      update();
    });
    update();
  }

  const photos = [...document.querySelectorAll('[data-gallery]')];
  const dialog = document.querySelector('#lightbox');
  if (!photos.length || !dialog || typeof dialog.showModal !== 'function') return;
  const close = dialog.querySelector('.lightbox-close');
  const prev = dialog.querySelector('.lightbox-prev');
  const next = dialog.querySelector('.lightbox-next');
  const image = dialog.querySelector('img');
  const caption = dialog.querySelector('figcaption');
  let index = 0;
  let opener;
  const render = (target) => {
    index = (target + photos.length) % photos.length;
    const link = photos[index];
    image.src = link.href;
    image.alt = link.querySelector('img').alt;
    caption.textContent = `${image.alt} · ${index + 1} of ${photos.length}`;
  };
  prev.disabled = next.disabled = photos.length < 2;
  photos.forEach((link, i) => link.addEventListener('click', (event) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = link;
    render(i);
    dialog.showModal();
  }));
  close.addEventListener('click', () => dialog.close());
  prev.addEventListener('click', () => render(index - 1));
  next.addEventListener('click', () => render(index + 1));
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('keydown', (event) => {
    if (photos.length < 2) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      render(index + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });
  dialog.addEventListener('close', () => opener?.focus());
})();
