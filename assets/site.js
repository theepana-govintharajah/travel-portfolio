(() => {
  const filters = document.querySelector('.filters');
  if (filters) {
    const buttons = [...filters.querySelectorAll('[data-filter]')];
    const cards = [...document.querySelectorAll('.trip-card')];
    const status = document.querySelector('#filter-status');
    filters.hidden = false;
    filters.addEventListener('click', (event) => {
      const button = event.target.closest('button[data-filter]');
      if (!button) return;
      const year = button.dataset.filter;
      let matches = 0;
      for (const other of buttons) other.setAttribute('aria-pressed', String(other === button));
      for (const card of cards) {
        card.hidden = year !== 'all' && card.dataset.year !== year;
        if (!card.hidden) matches++;
      }
      status.textContent = `${matches} ${matches === 1 ? 'trip' : 'trips'} shown.`;
    });
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
