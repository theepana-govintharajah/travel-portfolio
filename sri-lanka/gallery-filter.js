(() => {
  const gallery = document.querySelector('#district-gallery');
  const categories = document.querySelector('#district-gallery-filters');
  if (!gallery || !categories) return;

  const categoryButtons = [...categories.querySelectorAll('button[data-gallery-category]')];
  const groups = [...document.querySelectorAll('[data-gallery-parent]')];
  const photos = [...gallery.querySelectorAll('figure')];
  const count = document.querySelector('#district-gallery-count');
  const empty = document.querySelector('#district-gallery-empty');
  let category = 'all';
  let subcategory = 'all';
  let detail = 'all';
  let shown = [];
  let index = 0;
  let opener;
  const pressed = (button, active) => button.setAttribute('aria-pressed', String(active));

  function update() {
    categoryButtons.forEach(button => pressed(button, button.dataset.galleryCategory === category));
    groups.forEach(group => {
      const isDetailGroup = Boolean(group.dataset.galleryChild);
      group.hidden = group.dataset.galleryParent !== category ||
        (isDetailGroup && group.dataset.galleryChild !== subcategory);
      const key = isDetailGroup ? 'galleryDetail' : 'gallerySubcategory';
      const active = group.hidden ? 'all' : isDetailGroup ? detail : subcategory;
      const selector = isDetailGroup ? 'button[data-gallery-detail]' : 'button[data-gallery-subcategory]';
      group.querySelectorAll(selector).forEach(button => pressed(button, button.dataset[key] === active));
    });
    shown = [];
    photos.forEach(photo => {
      photo.hidden = !((category === 'all' || photo.dataset.category === category) &&
        (subcategory === 'all' || photo.dataset.subcategory === subcategory) &&
        (detail === 'all' || photo.dataset.detail === detail));
      if (!photo.hidden) shown.push(photo.querySelector('[data-gallery]'));
    });
    count.textContent = `${shown.length} ${shown.length === 1 ? 'photo' : 'photos'}`;
    empty.hidden = shown.length > 0;
  }

  categoryButtons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.galleryCategory;
    subcategory = 'all';
    detail = 'all';
    update();
  }));
  groups.forEach(group => {
    group.querySelectorAll('button[data-gallery-subcategory]').forEach(button =>
      button.addEventListener('click', () => {
        if (group.hidden) return;
        subcategory = button.dataset.gallerySubcategory;
        detail = 'all';
        update();
      }));
    group.querySelectorAll('button[data-gallery-detail]').forEach(button =>
      button.addEventListener('click', () => {
        if (group.hidden) return;
        detail = button.dataset.galleryDetail;
        update();
      }));
  });
  categories.hidden = false;
  update();

  const dialog = document.querySelector('#lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const next = dialog.querySelector('.lightbox-next');
  const prev = dialog.querySelector('.lightbox-prev');
  const image = dialog.querySelector('img');
  const caption = dialog.querySelector('figcaption');

  function render(nextIndex) {
    index = (nextIndex + shown.length) % shown.length;
    const link = shown[index];
    image.src = link.href;
    image.alt = link.querySelector('img').alt;
    caption.textContent = `${image.alt} · ${index + 1} of ${shown.length}`;
    prev.disabled = next.disabled = shown.length < 2;
  }

  gallery.addEventListener('click', event => {
    const link = event.target.closest('[data-gallery]');
    if (!link || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    const target = shown.indexOf(link);
    if (target < 0) return;
    event.preventDefault();
    opener = link;
    render(target);
    dialog.showModal();
  });
  dialog.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
  prev.addEventListener('click', () => render(index - 1));
  next.addEventListener('click', () => render(index + 1));
  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('keydown', event => {
    if (shown.length < 2 || !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    render(index + (event.key === 'ArrowLeft' ? -1 : 1));
  });
  dialog.addEventListener('close', () => opener?.focus());
})();
