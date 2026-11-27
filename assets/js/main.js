(function () {
  'use strict';

  var header = document.getElementById('header');
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');

  /* Хедер: плотный фон после прокрутки */
  var onScroll = function () {
    if (window.scrollY > 40) {
      header.classList.add('is-solid');
    } else {
      header.classList.remove('is-solid');
    }
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Мобильное меню */
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      burger.setAttribute('aria-label', open ? 'Открыть меню' : 'Закрыть меню');
      nav.classList.toggle('is-open', !open);
      document.body.style.overflow = open ? '' : 'hidden';
    });

    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && window.innerWidth <= 900) {
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-label', 'Открыть меню');
        nav.classList.remove('is-open');
        document.body.style.overflow = '';
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 900 && nav.classList.contains('is-open')) {
        burger.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        document.body.style.overflow = '';
      }
    });
  }

  /* Появление блоков */
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    revealEls.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i % 4, 3) * 70 + 'ms';
      io.observe(el);
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* FAQ */
  var faqItems = document.querySelectorAll('.faq__item');
  faqItems.forEach(function (item) {
    var btn = item.querySelector('.faq__q');
    var panel = item.querySelector('.faq__a');
    if (!btn || !panel) return;

    btn.addEventListener('click', function () {
      var isOpen = btn.getAttribute('aria-expanded') === 'true';

      faqItems.forEach(function (other) {
        var oBtn = other.querySelector('.faq__q');
        var oPanel = other.querySelector('.faq__a');
        if (oBtn !== btn && oBtn.getAttribute('aria-expanded') === 'true') {
          oBtn.setAttribute('aria-expanded', 'false');
          oPanel.style.maxHeight = '0px';
        }
      });

      btn.setAttribute('aria-expanded', String(!isOpen));
      panel.style.maxHeight = isOpen ? '0px' : panel.scrollHeight + 'px';
    });
  });

  window.addEventListener('resize', function () {
    faqItems.forEach(function (item) {
      var btn = item.querySelector('.faq__q');
      var panel = item.querySelector('.faq__a');
      if (btn && panel && btn.getAttribute('aria-expanded') === 'true') {
        panel.style.maxHeight = panel.scrollHeight + 'px';
      }
    });
  });

  /* Форма: без бэкенда, готовим текст заявки локально */
  var form = document.getElementById('lead-form');
  var result = document.getElementById('form-result');
  var preview = document.getElementById('form-preview');
  var tgLink = document.getElementById('tg-link');
  var mailLink = document.getElementById('mail-link');
  var copyBtn = document.getElementById('copy-btn');
  var againBtn = document.getElementById('form-again');

  var TG = 'vtoroe_dyhanie';
  var MAIL = 'vtoroedyhanie2@yandex.ru';

  if (form && result) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var name = form.elements.name;
      var contact = form.elements.contact;
      var consent = document.getElementById('consent');
      var ok = true;

      [name, contact].forEach(function (input) {
        var field = input.closest('.form__field');
        if (!input.value.trim()) {
          field.classList.add('has-error');
          ok = false;
        } else {
          field.classList.remove('has-error');
        }
      });

      var checkWrap = consent.closest('.form__check');
      if (!consent.checked) {
        checkWrap.classList.add('has-error');
        ok = false;
      } else {
        checkWrap.classList.remove('has-error');
      }

      if (!ok) {
        var firstError = form.querySelector('.has-error input, .has-error textarea');
        if (firstError) firstError.focus();
        return;
      }

      var text = [
        'Заявка с сайта ВИТОК',
        '',
        'Имя: ' + name.value.trim(),
        'Контакт: ' + contact.value.trim(),
        'Формат: ' + form.elements.format.value,
        'Ситуация: ' + (form.elements.message.value.trim() || '—')
      ].join('\n');

      preview.textContent = text;
      tgLink.href = 'https://t.me/' + TG + '?text=' + encodeURIComponent(text);
      mailLink.href = 'mailto:' + MAIL
        + '?subject=' + encodeURIComponent('Заявка с сайта ВИТОК')
        + '&body=' + encodeURIComponent(text);

      form.hidden = true;
      result.hidden = false;
      result.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    form.addEventListener('input', function (e) {
      var field = e.target.closest('.form__field');
      if (field) field.classList.remove('has-error');
      if (e.target.id === 'consent') {
        e.target.closest('.form__check').classList.remove('has-error');
      }
    });

    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        var text = preview.textContent;
        var done = function () {
          copyBtn.textContent = 'Скопировано';
          setTimeout(function () { copyBtn.textContent = 'Скопировать'; }, 2200);
        };

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, fallback);
        } else {
          fallback();
        }

        function fallback() {
          var ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand('copy'); done(); } catch (err) { /* noop */ }
          document.body.removeChild(ta);
        }
      });
    }

    if (againBtn) {
      againBtn.addEventListener('click', function () {
        form.reset();
        form.hidden = false;
        result.hidden = true;
        form.elements.name.focus();
      });
    }
  }

  /* Плавный переход по якорям с учётом фиксированного хедера */
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var id = link.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      var offset = 78;
      var top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
  });
})();
