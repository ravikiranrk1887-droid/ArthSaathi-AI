/**
 * FinBot AI — Main JavaScript
 * Utility functions shared across all pages.
 */

'use strict';

// ---------------------------------------------------------------------------
// Number formatting helpers (INR)
// ---------------------------------------------------------------------------

/**
 * Format a number as Indian Rupee currency string.
 * e.g. 1500000 → "₹15,00,000"
 */
function formatINR(amount, decimals = 0) {
  if (amount === null || amount === undefined || isNaN(amount)) return '₹—';
  return '₹' + Number(amount).toLocaleString('en-IN', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

/**
 * Format large numbers with suffixes: Lakh, Crore.
 * e.g. 1500000 → "₹15 Lakh"
 */
function formatINRShort(amount) {
  if (amount >= 1e7) return '₹' + (amount / 1e7).toFixed(2) + ' Cr';
  if (amount >= 1e5) return '₹' + (amount / 1e5).toFixed(2) + ' L';
  return formatINR(amount);
}

// ---------------------------------------------------------------------------
// API helper
// ---------------------------------------------------------------------------

/**
 * POST JSON to a URL and return parsed response.
 * @param {string} url
 * @param {object} body
 * @returns {Promise<object>}
 */
async function postJSON(url, body) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return response.json();
}

// ---------------------------------------------------------------------------
// Toast notification
// ---------------------------------------------------------------------------

/**
 * Show a Bootstrap-style toast notification.
 * @param {string} message
 * @param {'success'|'danger'|'warning'|'info'} type
 */
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container') || createToastContainer();
  const id = 'toast-' + Date.now();
  const html = `
    <div id="${id}" class="toast align-items-center text-bg-${type} border-0 show" role="alert">
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto"
                data-bs-dismiss="toast"></button>
      </div>
    </div>`;
  container.insertAdjacentHTML('beforeend', html);
  const el = document.getElementById(id);
  setTimeout(() => el && el.remove(), 4000);
}

function createToastContainer() {
  const div = document.createElement('div');
  div.id = 'toast-container';
  div.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;display:flex;flex-direction:column;gap:.5rem;';
  document.body.appendChild(div);
  return div;
}

// ---------------------------------------------------------------------------
// Active nav link highlighting
// ---------------------------------------------------------------------------
(function highlightActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-icon-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && path.startsWith(href)) {
      link.classList.add('active');
    } else if (href === '/' && path === '/') {
      link.classList.add('active');
    }
  });
})();

// ---------------------------------------------------------------------------
// Scroll-to-calculator helper (used on calculators index)
// ---------------------------------------------------------------------------
function scrollToCalc(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ---------------------------------------------------------------------------
// Expose to global scope
// ---------------------------------------------------------------------------
window.FinBot = {
  formatINR,
  formatINRShort,
  postJSON,
  showToast,
};
