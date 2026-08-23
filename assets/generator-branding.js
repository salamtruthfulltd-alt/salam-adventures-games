(() => {
  'use strict';

  const LOGO = '/assets/salam-adventures-official-logo.svg';
  const COPYRIGHT = '© 2026 Salam Adventures. All rights reserved.';
  const FOOTER_ID = 'salam-generator-copyright';
  const OLD_INJECTED_ID = 'salam-generator-branding';
  const PRINT_BRAND_CLASS = 'salam-print-brand';

  function disableArcadeTheme() {
    document.documentElement.classList.add('salam-generator-page');
    document.querySelectorAll('link[href*="arcade-theme.css"]').forEach(link => link.remove());
    document.querySelectorAll('style[id="salam-game-size-2026"]').forEach(style => style.remove());
  }

  function addStyles() {
    if (document.getElementById('salam-generator-branding-styles')) return;
    const style = document.createElement('style');
    style.id = 'salam-generator-branding-styles';
    style.textContent = `
      html.salam-generator-page, html.salam-generator-page body { color-scheme: light !important; }
      .salam-official-logo-wrap {
        width:86px!important;height:86px!important;min-width:86px!important;border-radius:50%!important;
        background:transparent!important;overflow:visible!important;display:flex!important;align-items:center!important;
        justify-content:center!important;padding:0!important;margin:0 auto 10px!important;box-shadow:none!important;
      }
      .salam-official-logo {
        width:86px!important;height:86px!important;object-fit:contain!important;display:block!important;border-radius:50%!important;
      }
      #${FOOTER_ID} {
        margin:24px auto 8px;padding:14px 16px;width:min(100%,980px);text-align:center;
        font:700 12px/1.4 Arial,sans-serif;color:#334155;border-top:1px solid rgba(51,65,85,.22);background:transparent!important;
      }
      .${PRINT_BRAND_CLASS} {
        display:none;
      }
      @media print {
        .salam-official-logo-wrap,.salam-official-logo {
          width:25mm!important;height:25mm!important;min-width:25mm!important;
        }
        #${FOOTER_ID} {
          display:block!important;margin:8mm auto 0;padding-top:3mm;font-size:9pt;color:#000;
          border-top:.2mm solid #777;break-inside:avoid;
        }
        .${PRINT_BRAND_CLASS} {
          display:flex!important;align-items:center!important;justify-content:center!important;
          width:100%!important;margin:0 auto 5mm!important;padding:0!important;break-inside:avoid!important;
        }
        .${PRINT_BRAND_CLASS} img {
          display:block!important;width:25mm!important;height:25mm!important;object-fit:contain!important;
          border-radius:50%!important;margin:0 auto!important;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function removeDuplicateTopLogo() {
    document.getElementById(OLD_INJECTED_ID)?.remove();
  }

  function findBrandArea() {
    return document.querySelector('.logo-container, .brand-logo, .logo-wrap, .header-logo, .worksheet-logo, .brand .logo, header .logo, .logo');
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
      const target = document.querySelector('header, .header, .panel, main, .container, .wrap');
      if (!target) return;
      holder = document.createElement('div');
      target.insertBefore(holder, target.firstChild);
    }
    holder.classList.add('salam-official-logo-wrap');
    const existingOfficial = holder.querySelector('[data-official-salam-logo="true"]');
    if (existingOfficial && holder.children.length === 1) return;
    holder.replaceChildren(createOfficialLogo());
  }

  function printableTargets() {
    const selector = [
      '.worksheet','.sheet','.worksheet-container','.printable','.print-area','.print-area-content',
      '.preview','.paper','.page','.a4','.a4-page','#worksheet','#sheet','#printArea','#print-area'
    ].join(',');
    const found = [...document.querySelectorAll(selector)].filter(el => {
      if (el.closest('.controls,.panel-controls,.toolbar,.actions,.buttons')) return false;
      return el.offsetWidth > 0 || el.offsetHeight > 0 || getComputedStyle(el).display !== 'none';
    });
    if (found.length) return found;
    const fallback = document.querySelector('main, .app, .container, .wrap') || document.body;
    return [fallback];
  }

  function ensurePrintLogoInOutputs() {
    printableTargets().forEach((target, index) => {
      let brand = target.querySelector(`:scope > .${PRINT_BRAND_CLASS}`);
      if (!brand) {
        brand = document.createElement('div');
        brand.className = PRINT_BRAND_CLASS;
        brand.setAttribute('data-salam-print-brand', String(index + 1));
        const img = document.createElement('img');
        img.src = LOGO;
        img.alt = 'Salam Adventures logo';
        img.setAttribute('data-official-salam-print-logo', 'true');
        brand.appendChild(img);
        target.insertBefore(brand, target.firstChild);
      }
    });
  }

  function ensureFooter() {
    if (document.getElementById(FOOTER_ID)) return;
    const target = document.querySelector('.worksheet, .sheet, .container, main, .app, .worksheet-container, .wrap') || document.body;
    const footer = document.createElement('footer');
    footer.id = FOOTER_ID;
    footer.textContent = COPYRIGHT;
    target.appendChild(footer);
  }

  function applyBranding() {
    disableArcadeTheme();
    addStyles();
    placeLogoInHeader();
    ensurePrintLogoInOutputs();
    ensureFooter();
  }

  disableArcadeTheme();

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

  new MutationObserver(scheduleApply).observe(document.documentElement, { childList:true, subtree:true });
  window.addEventListener('beforeprint', applyBranding);
})();
