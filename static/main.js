/**
 * RRCHNM Hugo Site - Global JavaScript
 * Handles mobile menu toggle, header scroll effects, and other UI behaviors.
 */

// Global image fallback
function applyImgFallback(img) {
  if (img.dataset.fallback) return;
  img.dataset.fallback = '1';
  var isPersonImg = img.closest('.staff-card') || img.id === 'staff-modal-photo';
  img.src = isPersonImg ? '/img/person-placeholder.svg' : '/img/image-placeholder.svg';
}

// Catch errors on images that fail after JS loads
document.addEventListener('error', function (e) {
  if (e.target.tagName === 'IMG') applyImgFallback(e.target);
}, true);

// Catch images that already failed before JS loaded
document.addEventListener('DOMContentLoaded', function () {
  var imgs = document.querySelectorAll('img');
  for (var i = 0; i < imgs.length; i++) {
    if (imgs[i].complete && imgs[i].naturalWidth === 0) applyImgFallback(imgs[i]);
  }
});

(function () {
  'use strict';

  // Mobile menu toggle
  var opener = document.querySelector('.mobile-menu-toggle');
  var mobileNav = document.querySelector('.mobile-nav');

  if (opener && mobileNav) {
    opener.addEventListener('click', function (e) {
      e.preventDefault();
      mobileNav.classList.toggle('is-open');
      opener.classList.toggle('is-open');
    });

    // Close mobile menu when clicking a link
    var mobileLinks = mobileNav.querySelectorAll('a');
    for (var i = 0; i < mobileLinks.length; i++) {
      mobileLinks[i].addEventListener('click', function () {
        mobileNav.classList.remove('is-open');
        opener.classList.remove('is-open');
      });
    }
  }

  // Mobile sub-menu toggle (expand children on tap)
  var parentItems = document.querySelectorAll('#site-header-mobile .menu-item-has-children > a');
  for (var j = 0; j < parentItems.length; j++) {
    parentItems[j].addEventListener('click', function (e) {
      var subMenu = this.nextElementSibling;
      if (subMenu && subMenu.classList.contains('sub-menu')) {
        // If on mobile and sub-menu exists, toggle it
        if (window.innerWidth <= 1024) {
          e.preventDefault();
          subMenu.style.display = subMenu.style.display === 'block' ? 'none' : 'block';
        }
      }
    });
  }

  // Staff profile modal
  var modal = document.getElementById('staff-modal');
  if (modal) {
    var modalPhoto    = document.getElementById('staff-modal-photo');
    var modalName     = document.getElementById('staff-modal-name');
    var modalJobTitle = document.getElementById('staff-modal-job-title');
    var modalBio      = document.getElementById('staff-modal-bio');
    var modalClose    = modal.querySelector('.staff-modal-close');

    function openStaffModal(card) {
      var bioDiv = card.querySelector('.staff-bio-data');
      modalName.textContent     = card.dataset.modalName    || '';
      modalJobTitle.textContent = card.dataset.modalTitle   || '';
      modalPhoto.src            = card.dataset.modalPicture || '';
      modalPhoto.alt            = card.dataset.modalName    || '';
      modalBio.innerHTML        = bioDiv ? bioDiv.innerHTML : '';
      modal.showModal();
    }

    // Delegate clicks on any .staff-card-trigger
    document.addEventListener('click', function (e) {
      var trigger = e.target.closest('.staff-card-trigger');
      if (trigger) {
        var card = trigger.closest('.staff-card');
        if (card) openStaffModal(card);
      }
    });

    // Close button
    modalClose.addEventListener('click', function () {
      modal.close();
    });

    // Close on backdrop click
    modal.addEventListener('click', function (e) {
      if (e.target === modal) modal.close();
    });

    // Close on Escape (built-in for <dialog>, but belt-and-suspenders)
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.open) modal.close();
    });
  }

  // Header scroll shrink effect
  var header = document.getElementById('site-header');
  if (header) {
    var headerInner = document.getElementById('site-header-inner');
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        header.classList.add('is-shrunk');
        if (headerInner) {
          headerInner.style.height = '70px';
        }
      } else {
        header.classList.remove('is-shrunk');
        if (headerInner) {
          headerInner.style.height = '';
        }
      }
    });
  }
})();
