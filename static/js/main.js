/* ═══════════════════════════════════════════════════════════════════════
   Faculty Information System — Main JS
   ═══════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── Sidebar toggle ─────────────────────────────────────────────────
  const sidebar      = document.getElementById('sidebar');
  const mainWrapper  = document.getElementById('mainWrapper');
  const overlay      = document.getElementById('sidebarOverlay');
  const toggleBtn    = document.getElementById('sidebarToggle');
  const closeBtn     = document.getElementById('sidebarClose');

  function openSidebar() {
    sidebar?.classList.add('open');
    overlay?.classList.add('show');
  }

  function closeSidebar() {
    sidebar?.classList.remove('open');
    overlay?.classList.remove('show');
  }

  toggleBtn?.addEventListener('click', () => {
    if (window.innerWidth >= 992) {
      // Desktop: collapse/expand
      const collapsed = mainWrapper.style.marginLeft === '0px';
      mainWrapper.style.marginLeft = collapsed ? 'var(--sidebar-width)' : '0px';
      sidebar.style.transform      = collapsed ? 'none' : 'translateX(-100%)';
    } else {
      openSidebar();
    }
  });

  closeBtn?.addEventListener('click', closeSidebar);
  overlay?.addEventListener('click', closeSidebar);

  // Close sidebar on resize to desktop
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 992) closeSidebar();
  });

  // ── Auto-dismiss flash alerts after 5s ─────────────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert?.close();
    }, 5000);
  });

  // ── Confirm on delete forms (fallback) ─────────────────────────────
  document.querySelectorAll('form[data-confirm]').forEach(form => {
    form.addEventListener('submit', e => {
      if (!confirm(form.dataset.confirm)) e.preventDefault();
    });
  });

  // ── Salary net calculator (on any page that may have it) ───────────
  function calcSalaryNet() {
    const basic  = parseFloat(document.getElementById('basic')?.value) || 0;
    const allow  = parseFloat(document.getElementById('allowances')?.value) || 0;
    const deduct = parseFloat(document.getElementById('deductions')?.value) || 0;
    const el     = document.getElementById('netDisplay');
    if (el) el.textContent = '₹' + (basic + allow - deduct).toFixed(2);
  }

  ['basic', 'allowances', 'deductions'].forEach(id => {
    document.getElementById(id)?.addEventListener('input', calcSalaryNet);
  });

  // ── Uppercase codes ─────────────────────────────────────────────────
  document.querySelectorAll('[name="department_code"], [name="employee_code"]').forEach(el => {
    el.addEventListener('input', function () {
      const pos = this.selectionStart;
      this.value = this.value.toUpperCase();
      this.setSelectionRange(pos, pos);
    });
  });

  // ── Table search (client-side quick filter) ─────────────────────────
  const quickSearch = document.getElementById('quickTableSearch');
  if (quickSearch) {
    quickSearch.addEventListener('input', function () {
      const term = this.value.toLowerCase();
      document.querySelectorAll('tbody tr').forEach(row => {
        row.style.display = row.textContent.toLowerCase().includes(term) ? '' : 'none';
      });
    });
  }

  // ── Tooltip init ────────────────────────────────────────────────────
  document.querySelectorAll('[title]').forEach(el => {
    new bootstrap.Tooltip(el, { trigger: 'hover', placement: 'top' });
  });

  // ── Form submit loading state ───────────────────────────────────────
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function () {
      const btn = this.querySelector('button[type="submit"]');
      if (btn && !btn.classList.contains('no-load')) {
        btn.disabled = true;
        const original = btn.innerHTML;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Processing…';
        setTimeout(() => {
          btn.disabled = false;
          btn.innerHTML = original;
        }, 8000);
      }
    });
  });

  // ── Active nav highlight (fallback for Jinja) ───────────────────────
  const currentPath = window.location.pathname.split('/')[1];
  document.querySelectorAll('.sidebar-nav .nav-link').forEach(link => {
    const href = link.getAttribute('href') || '';
    if (href.includes(currentPath) && currentPath) {
      link.classList.add('active');
    }
  });

  // ── Sortable table columns ──────────────────────────────────────────
  document.querySelectorAll('table').forEach(table => {
    const headers = table.querySelectorAll('thead th');
    headers.forEach((th, colIndex) => {
      th.setAttribute('data-sort', colIndex);
      th.style.cursor = 'pointer';
      th.addEventListener('click', () => {
        const tbody = table.querySelector('tbody');
        const rows  = Array.from(tbody.querySelectorAll('tr'));
        const asc   = th.dataset.order !== 'asc';
        th.dataset.order = asc ? 'asc' : 'desc';
        // Reset other headers
        headers.forEach(h => { if (h !== th) delete h.dataset.order; });
        rows.sort((a, b) => {
          const av = a.cells[colIndex]?.textContent.trim() || '';
          const bv = b.cells[colIndex]?.textContent.trim() || '';
          const an = parseFloat(av.replace(/[₹,]/g, ''));
          const bn = parseFloat(bv.replace(/[₹,]/g, ''));
          const compare = isNaN(an) || isNaN(bn) ? av.localeCompare(bv) : an - bn;
          return asc ? compare : -compare;
        });
        rows.forEach(r => tbody.appendChild(r));
        // visual indicator
        headers.forEach(h => h.querySelector('.sort-icon')?.remove());
        const icon = document.createElement('i');
        icon.className = `bi bi-chevron-${asc ? 'up' : 'down'} sort-icon ms-1`;
        icon.style.fontSize = '.7rem';
        th.appendChild(icon);
      });
    });
  });

  // ── Date input — prevent future dates where needed ─────────────────
  document.querySelectorAll('input[name="date_of_birth"]').forEach(el => {
    el.max = new Date().toISOString().split('T')[0];
  });

  // ── Auto-uppercase employee/dept codes ─────────────────────────────
  document.querySelectorAll('[name="department_code"], [name="employee_code"]').forEach(el => {
    el.addEventListener('input', function () {
      const pos = this.selectionStart;
      this.value = this.value.toUpperCase();
      this.setSelectionRange(pos, pos);
    });
  });

  // ── Pincode — digits only ───────────────────────────────────────────
  document.querySelectorAll('[name="pincode"]').forEach(el => {
    el.addEventListener('input', function () {
      this.value = this.value.replace(/\D/g, '');
    });
  });

  console.log('%cFacultyIS loaded ✓', 'color:#6366f1;font-weight:700;font-size:13px');
})();
