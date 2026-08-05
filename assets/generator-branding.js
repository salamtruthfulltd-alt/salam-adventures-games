(() => {
  'use strict';

  const LOGO = '/assets/salam-adventures-official-logo.svg';
  const COPYRIGHT = '© 2026 Salam Adventures. All rights reserved.';
  const BRAND_ID = 'salam-generator-branding';
  const FOOTER_ID = 'salam-generator-copyright';

  function addStyles() {
    if (document.getElementById('salam-generator-branding-styles')) return;
    const style = document.createElement('style');
    style.id = 'salam-generator-branding-styles';
    style.textContent = `
      #${BRAND_ID} { display:flex; align-items:center; justify-content:center; margin:12px auto 18px; width:min(100%,920px); }
      #${BRAND_ID} img { width:110px; height:110px; object-fit:contain; display:block; }
      #${FOOTER_ID} { margin:20px auto 8px; padding:12px 16px; width:min(100%,920px); text-align:center; font:600 12px/1.4 Arial,sans-serif; color:#334155; border-top:1px solid rgba(51,65,85,.18); }
      @media print {
        #${BRAND_ID} { display:flex !important; margin:0 auto 10mm; }
        #${BRAND_ID} img { width:25mm; height:25mm; }
        #${FOOTER_ID} { display:block !important; margin:8mm auto 0; padding-top:3mm; font-size:9pt; color:#000; border-top:.2mm solid #777; break-inside:avoid; }
      }
    `;
    document.head.appendChild(style);
  }

  function removeOldBrandImages() {
    document.querySelectorAll('img').forEach((img) => {
      if (img.closest(`#${BRAND_ID}`)) return;
      const src = (img.getAttribute('src') || '').toLowerCase();
      const alt = (img.getAttribute('alt') || '').toLowerCase();
      const classes = (img.className || '').toString().toLowerCase();
      const isOldBrandImage =
        src.includes('salam-adventures-home') ||
        src.includes('logo') ||
        alt.includes('salam adventures') ||
        alt.includes('logo') ||
        classes.includes('logo-img');
      if (isOldBrandImage) img.remove();
    });
  }

  function ensureBranding() {
    addStyles();
    removeOldBrandImages();

    const target = document.querySelector('.container, main, .app, .worksheet-container') || document.body;
    const header = target.querySelector('.header, header, .worksheet-header');

    if (!document.getElementById(BRAND_ID)) {
      const brand = document.createElement('div');
      brand.id = BRAND_ID;
      brand.setAttribute('aria-label', 'Salam Adventures');

      const logo = document.createElement('img');
      logo.src = LOGO;
      logo.alt = 'Salam Adventures logo';
      logo.setAttribute('data-official-salam-logo', 'true');
      brand.appendChild(logo);

      if (header) header.insertBefore(brand, header.firstChild);
      else target.insertBefore(brand, target.firstChild);
    }

    if (!document.getElementById(FOOTER_ID)) {
      const footer = document.createElement('footer');
      footer.id = FOOTER_ID;
      footer.textContent = COPYRIGHT;
      target.appendChild(footer);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureBranding, { once: true });
  } else {
    ensureBranding();
  }

  new MutationObserver(() => {
    if (!document.getElementById(BRAND_ID) || !document.getElementById(FOOTER_ID)) ensureBranding();
    else removeOldBrandImages();
  }).observe(document.documentElement, { childList: true, subtree: true });

  window.addEventListener('beforeprint', ensureBranding);
})();
