/**
 * RRCHNM Hugo Site - Global JavaScript
 */

// Global image fallback
function applyImgFallback(img) {
  if (img.dataset.fallback) return;
  img.dataset.fallback = '1';
  var isPersonImg = img.closest('.staff-card') || img.id === 'staff-modal-photo';
  img.src = isPersonImg ? '/img/person-placeholder.svg' : '/img/image-placeholder.svg';
}

document.addEventListener('error', function (e) {
  if (e.target.tagName === 'IMG') applyImgFallback(e.target);
}, true);

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
      var isOpen = !mobileNav.classList.contains('hidden');
      mobileNav.classList.toggle('hidden');
      opener.setAttribute('aria-expanded', String(!isOpen));
    });

    var mobileLinks = mobileNav.querySelectorAll('a');
    for (var i = 0; i < mobileLinks.length; i++) {
      mobileLinks[i].addEventListener('click', function () {
        mobileNav.classList.add('hidden');
        opener.setAttribute('aria-expanded', 'false');
      });
    }
  }

  // Mobile sub-menu toggle
  var parentItems = document.querySelectorAll('#site-header-mobile .menu-item-has-children > a');
  for (var j = 0; j < parentItems.length; j++) {
    parentItems[j].addEventListener('click', function (e) {
      var subMenu = this.nextElementSibling;
      if (subMenu && subMenu.tagName === 'UL') {
        e.preventDefault();
        subMenu.classList.toggle('hidden');
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
    var modalClose    = modal.querySelector('button[aria-label="Close"]');

    function openStaffModal(card) {
      var bioDiv = card.querySelector('.staff-bio-data');
      modalName.textContent     = card.dataset.modalName    || '';
      modalJobTitle.textContent = card.dataset.modalTitle   || '';
      modalPhoto.src            = card.dataset.modalPicture || '';
      modalPhoto.alt            = card.dataset.modalName ? 'Photo of ' + card.dataset.modalName : '';
      modalBio.innerHTML        = bioDiv ? bioDiv.innerHTML : '';
      modal.showModal();
    }

    document.addEventListener('click', function (e) {
      var trigger = e.target.closest('.staff-card-trigger');
      if (trigger) {
        var card = trigger.closest('.staff-card');
        if (card) openStaffModal(card);
      }
    });

    if (modalClose) {
      modalClose.addEventListener('click', function () {
        modal.close();
      });
    }

    modal.addEventListener('click', function (e) {
      if (e.target === modal) modal.close();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.open) modal.close();
    });
  }

  // Back to top button
  var backToTop = document.getElementById('back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 400) {
        backToTop.classList.remove('opacity-0', 'translate-y-4', 'pointer-events-none');
        backToTop.classList.add('opacity-100', 'translate-y-0');
      } else {
        backToTop.classList.add('opacity-0', 'translate-y-4', 'pointer-events-none');
        backToTop.classList.remove('opacity-100', 'translate-y-0');
      }
    });
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
})();
