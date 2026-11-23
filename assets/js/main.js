/* Progressive enhancement: paper text, figures, links and tables work without JS. */
(() => {
  const dialog = document.querySelector('#figure-dialog');
  const enlarged = document.querySelector('#enlarged-figure');
  const zoom = document.querySelector('#zoom-figure');
  const imageContainer = document.querySelector('.dialog-image');
  let figureTrigger;
  if (dialog && typeof dialog.showModal === 'function') {
    document.querySelectorAll('.figure-zoom').forEach(link => {
      link.addEventListener('click', event => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        figureTrigger = link;
        const figure = link.closest('figure');
        const caption = figure.querySelector('figcaption').textContent;
        enlarged.src = link.href;
        enlarged.alt = link.querySelector('img').alt;
        imageContainer.classList.remove('is-zoomed');
        imageContainer.scrollTo(0, 0);
        zoom.setAttribute('aria-pressed', 'false');
        zoom.textContent = 'Zoom in';
        document.querySelector('#dialog-title').textContent = `Figure ${link.dataset.figure}`;
        document.querySelector('#dialog-caption').textContent = caption;
        document.querySelector('#figure-pdf').href = `assets/figures/figure-${link.dataset.figure}.pdf`;
        document.body.classList.add('dialog-open');
        dialog.showModal();
      });
    });
    document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
    zoom.addEventListener('click', () => {
      const zoomed = imageContainer.classList.toggle('is-zoomed');
      zoom.setAttribute('aria-pressed', String(zoomed));
      zoom.textContent = zoomed ? 'Fit image' : 'Zoom in';
    });
    dialog.addEventListener('click', event => {
      const box = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('dialog-open');
      figureTrigger?.focus({preventScroll: true});
    });
  }

  const copy = document.querySelector('#copy-citation');
  const citation = document.querySelector('#bibtex');
  const status = document.querySelector('#copy-status');
  copy.hidden = false;
  let resetCopy;
  copy.addEventListener('click', async () => {
    clearTimeout(resetCopy);
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(citation.textContent.trim() + '\n');
      copy.querySelector('span').textContent = 'Copied!';
      status.textContent = 'BibTeX copied to clipboard.';
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(citation);
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Citation selected. Press Ctrl+C (Windows/Linux) or ⌘C (Mac) to copy.';
    }
    resetCopy = setTimeout(() => {
      copy.querySelector('span').textContent = 'Copy BibTeX';
      status.textContent = '';
    }, 6000);
  });

  if ('IntersectionObserver' in window) {
    const links = [...document.querySelectorAll('.nav-links a')];
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        links.forEach(link => {
          if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      }
    }, {rootMargin: '-10% 0px -65% 0px'});
    links.forEach(link => observer.observe(document.querySelector(link.hash)));
    observer.observe(document.querySelector('.hero'));
  }
})();
