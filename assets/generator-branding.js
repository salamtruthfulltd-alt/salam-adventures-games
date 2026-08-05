(() => {
  'use strict';

  const LOGO = '/assets/salam-adventures-official-logo.svg';
  const COPYRIGHT = '© 2026 Salam Adventures. All rights reserved.';
  const FOOTER_ID = 'salam-generator-copyright';
  const OLD_INJECTED_ID = 'salam-generator-branding';

  function addStyles() {
    if (document.getElementById('salam-generator-branding-styles')) return;
    const style = document.createElement('style');
    style.id = 'salam-generator-branding-styles';
    style.textContent = `
      .salam-official-logo-wrap {
        width: 75px !important;
        height: 75px !important;
        min-width: 75px !important;
        border-radius: 50% !important;
        background: transparent !important;
        overflow: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        box-shadow: none !important;
      }
      .salam-official-logo {
        width: 75px !important;
        height: 75px !important;
        object-fit: contain !important;
        display: block !important;
        border-radius: 50% !important;
      }
      #${FOOTER_ID} {
        margin: 20px auto 8px;
        padding: 12px 16px;
        width: min(100%, 920px);
        text-align: center;
        font: 600 12px/1.4 Arial, sans-serif;
        color: #334155;
        border-top: 1px solid rgba(51,65,85,.18);
      }
      @media print {
        .salam-official-logo-wrap,
        .salam-official-logo {
          width: 25mm !important;
          height: 25mm !important;
          min-width: 25mm !important;
        }
        #${FOOTER_ID} {
          display: block !important;
          margin: 8mm auto 0;
          padding-top: 3mm;
          font-size: 9pt;
          color: #000;
          border-top: .2mm solid #777;
          break-inside: avoid;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function removeDuplicateTopLogo() {
    document.getElementById(OLD_INJECTED_ID)?.remove();
  }

  function findBrandArea() {
    return document.querySelector(
      '.logo-container, .brand-logo, .logo-wrap, .header-logo, .worksheet-logo, .brand .logo, header .logo'
    );
  }

  function createOfficialLogo() {
    const img = document.createElement('img');
    img.src = LOGO;
    img.alt = 'Salam Adventures logo';
    img.className = 'salam-official-logo';
    img.setAttribute('data-official-salam-logo', 'true');
    return img;
  }

  function placeLogoInHeader() {
    removeDuplicateTopLogo();

    let holder = findBrandArea();

    if (!holder) {
      const brand = document.querySelector('.header .brand, header .brand, .worksheet-header .brand');
      if (!brand) return;
      holder = document.createElement('div');
      brand.insertBefore(holder, brand.firstChild);
    }

    holder.classList.add('salam-official-logo-wrap');

    const existingOfficial = holder.querySelector('[data-official-salam-logo="true"]');
    if (existingOfficial && holder.children.length === 1) return;

    holder.replaceChildren(createOfficialLogo());
  }

  function ensureFooter() {
    if (document.getElementById(FOOTER_ID)) return;
    const target = document.querySelector('.worksheet, .container, main, .app, .worksheet-container') || document.body;
    const footer = document.createElement('footer');
    footer.id = FOOTER_ID;
    footer.textContent = COPYRIGHT;
    target.appendChild(footer);
  }

  function applyBranding() {
    addStyles();
    placeLogoInHeader();
    ensureFooter();
  }

  let scheduled = false;
  function scheduleApply() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      applyBranding();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyBranding, { once: true });
  } else {
    applyBranding();
  }

  new MutationObserver(scheduleApply).observe(document.documentElement, {
    childList: true,
    subtree: true
  });

  window.addEventListener('beforeprint', applyBranding);
})();
