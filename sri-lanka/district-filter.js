(() => {
  const filters = document.getElementById('sl-province-filters');
  const grid = document.getElementById('sl-district-grid');
  const status = document.getElementById('sl-district-count');
  if (!filters || !grid || !status) return;
  const buttons = [...filters.querySelectorAll('button[data-province-filter]')];
  const cards = [...grid.querySelectorAll('[data-province]')];
  filters.hidden = false;
  filters.addEventListener('click', event => {
    const selected = event.target.closest('button[data-province-filter]');
    if (!selected || !filters.contains(selected)) return;
    const province = selected.dataset.provinceFilter;
    let visibleCount = 0;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button === selected)));
    cards.forEach(card => {
      card.hidden = province !== 'all' && card.dataset.province !== province;
      if (!card.hidden) visibleCount++;
    });
    status.textContent = `${visibleCount} ${visibleCount === 1 ? 'district' : 'districts'}`;
  });
})();
