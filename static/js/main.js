const herbs = [
    {
        name: "Amla",
        sanskrit: "Āmalakī",
        benefit: "Immunity",
        dosha: "Tri-doshic",
        svg: `<svg class="herb-svg" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M24 12 L28 20 L34 22 L28 28 L30 36 L24 32 L18 36 L20 28 L14 22 L20 20 Z" stroke-linecap="round"/>
                <circle cx="24" cy="24" r="2.5" fill="currentColor" fill-opacity="0.2"/>
              </svg>`
    },
    {
        name: "Neem",
        sanskrit: "Nimba",
        benefit: "Skin purifier",
        dosha: "Kapha-Pitta",
        svg: `<svg class="herb-svg" viewBox="0 0 48 48" fill="none" stroke="currentColor">
                <path d="M24 10 L28 18 L36 20 L30 26 L32 34 L24 30 L16 34 L18 26 L12 20 L20 18 Z"/>
                <path d="M24 24 L24 30" stroke-width="1.5"/>
              </svg>`
    },
    {
        name: "Ashwagandha",
        sanskrit: "Aśvagandhā",
        benefit: "Stress relief",
        dosha: "Vata",
        svg: `<svg class="herb-svg" viewBox="0 0 48 48" stroke="currentColor">
                <path d="M24 14 L26 22 L34 22 L28 28 L30 36 L24 32 L18 36 L20 28 L14 22 L22 22 Z"/>
                <line x1="24" y1="36" x2="24" y2="42"/>
              </svg>`
    },
    {
        name: "Turmeric",
        sanskrit: "Haridrā",
        benefit: "Anti-inflammatory",
        dosha: "All",
        svg: `<svg class="herb-svg" viewBox="0 0 48 48" stroke="currentColor">
                <path d="M24 12 L28 20 L36 20 L30 26 L32 34 L24 28 L16 34 L18 26 L12 20 L20 20 Z"/>
                <circle cx="24" cy="22" r="2.2"/>
              </svg>`
    },
    {
        name: "Tulsi",
        sanskrit: "Tulasī",
        benefit: "Respiratory",
        dosha: "Kapha",
        svg: `<svg class="herb-svg" viewBox="0 0 48 48" stroke="currentColor">
                <path d="M24 10 L26 18 L34 18 L28 24 L30 32 L24 26 L18 32 L20 24 L14 18 L22 18 Z"/>
                <path d="M24 32 L24 40"/>
              </svg>`
    },
    {
        name: "Licorice",
        sanskrit: "Yashtimadhu",
        benefit: "Digestion",
        dosha: "Vata-Pitta",
        svg: `<svg class="herb-svg" viewBox="0 0 48 48" stroke="currentColor">
                <path d="M20 20 L28 20 L30 28 L24 32 L18 28 L20 20 Z"/>
                <path d="M24 14 L24 20"/>
              </svg>`
    },
    {
        name: "Brahmi",
        sanskrit: "Brahmi",
        benefit: "Cognitive",
        dosha: "Pitta",
        svg: `<svg class="herb-svg" viewBox="0 0 48 48" stroke="currentColor">
                <path d="M24 12 L28 20 L36 20 L30 26 L32 34 L24 28 L16 34 L18 26 L12 20 L20 20 Z"/>
                <circle cx="24" cy="22" r="1.8"/>
              </svg>`
    },
    {
        name: "Sandalwood",
        sanskrit: "Chandana",
        benefit: "Cooling",
        dosha: "Pitta",
        svg: `<svg class="herb-svg" viewBox="0 0 48 48" stroke="currentColor">
                <path d="M20 16 L28 16 L32 24 L24 32 L16 24 L20 16 Z"/>
                <path d="M24 32 L24 40"/>
              </svg>`
    },
    {
        name: "Gotu Kola",
        sanskrit: "Mandūkaparṇī",
        benefit: "Longevity",
        dosha: "Tri-doshic",
        svg: `<svg class="herb-svg" viewBox="0 0 48 48" stroke="currentColor">
                <path d="M24 14 L28 20 L34 20 L28 26 L30 32 L24 26 L18 32 L20 26 L14 20 L20 20 Z"/>
                <line x1="24" y1="32" x2="24" y2="38"/>
              </svg>`
    }
];

function renderHerbs() {
    const herbGrid = document.getElementById('herbGrid');
    herbs.forEach((h, idx) => {
        const card = document.createElement('div');
        card.className = 'herb-card';
        card.style.animationDelay = `${idx * 0.04}s`;
        card.innerHTML = `
            ${h.svg}
            <div class="herb-name">${h.name}</div>
            <div class="sanskrit">${h.sanskrit}</div>
            <div class="benefit-badge">${h.benefit}</div>
            <div class="dosha-tag">${h.dosha}</div>
        `;
        herbGrid.appendChild(card);
    });
}

function generateParticles() {
    const container = document.getElementById('particles');
    for (let i = 0; i < 45; i++) {
        const p = document.createElement('div');
        p.classList.add('particle');
        const size = Math.random() * 3 + 1;
        p.style.width  = size + 'px';
        p.style.height = size + 'px';
        p.style.left   = Math.random() * 100 + '%';
        p.style.animationDuration = 12 + Math.random() * 20 + 's';
        p.style.animationDelay    = Math.random() * 15 + 's';
        container.appendChild(p);
    }
}

function initHeadline() {
    document.querySelectorAll('.word').forEach((w, i) => {
        w.style.animationDelay = `${i * 0.1}s`;
    });
}

function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light');
        const icon = themeToggle.querySelector('i');
        icon.className = document.body.classList.contains('light')
            ? 'fas fa-sun'
            : 'fas fa-moon';
    });
}

function initModal() {
    const modal       = document.getElementById('authModal');
    const openLogin   = document.getElementById('openLoginBtn');
    const openSignup  = document.getElementById('openSignupBtn');
    const closeBtn    = document.querySelector('.close-modal');
    const loginTab    = document.querySelector('[data-tab="login"]');
    const regTab      = document.querySelector('[data-tab="register"]');
    const loginDiv    = document.getElementById('loginForm');
    const regDiv      = document.getElementById('registerForm');

    const showModal = () => { modal.style.display = 'flex'; };
    const hideModal = () => { modal.style.display = 'none'; };

    const switchToLogin = () => {
        loginDiv.style.display = 'block';
        regDiv.style.display   = 'none';
        loginTab.classList.add('active-tab');
        regTab.classList.remove('active-tab');
    };

    const switchToRegister = () => {
        regDiv.style.display   = 'block';
        loginDiv.style.display = 'none';
        regTab.classList.add('active-tab');
        loginTab.classList.remove('active-tab');
    };

    openLogin.addEventListener('click',  () => { showModal(); switchToLogin(); });
    openSignup.addEventListener('click', () => { showModal(); switchToRegister(); });
    closeBtn.addEventListener('click', hideModal);
    modal.addEventListener('click', (e) => { if (e.target === modal) hideModal(); });
    loginTab.addEventListener('click', switchToLogin);
    regTab.addEventListener('click',   switchToRegister);

    function showModalMsg(msg, isError = false) {
        let el = document.getElementById('modalMsg');
        if (!el) {
            el = document.createElement('div');
            el.id = 'modalMsg';
            el.style.cssText = [
                'margin-top:0.8rem', 'padding:0.6rem 1rem',
                'border-radius:40px', 'font-size:0.85rem',
                'text-align:center', 'font-weight:500'
            ].join(';');
            document.querySelector('.modal-card').appendChild(el);
        }
        el.textContent = msg;
        el.style.background = isError ? 'rgba(220,50,50,0.15)' : 'rgba(45,106,79,0.2)';
        el.style.color      = isError ? '#ff6b6b'             : 'var(--accent-gold)';
        el.style.border     = isError
            ? '1px solid rgba(220,50,50,0.3)'
            : '1px solid rgba(230,200,122,0.3)';
    }

    function setLoading(btnId, loading) {
        const btn = document.getElementById(btnId);
        btn.disabled    = loading;
        btn.textContent = loading
            ? 'Please wait...'
            : (btnId === 'doLogin' ? 'Login' : 'Sign Up →');
    }

    document.getElementById('doLogin').addEventListener('click', async () => {
        const email    = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;
        if (!email || !password) { showModalMsg('Please fill in all fields.', true); return; }

        setLoading('doLogin', true);
        try {
            const res  = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();
            if (res.ok && data.success) {
                showModalMsg('Login successful! Redirecting...');
                setTimeout(() => { window.location.href = data.redirect || '/checker'; }, 800);
            } else {
                showModalMsg(data.error || 'Login failed. Try again.', true);
            }
        } catch (err) {
            showModalMsg('Network error. Is the server running?', true);
        } finally {
            setLoading('doLogin', false);
        }
    });

    document.getElementById('doRegister').addEventListener('click', async () => {
        const name     = document.getElementById('regName').value.trim();
        const email    = document.getElementById('regEmail').value.trim();
        const password = document.getElementById('regPassword').value;
        const age      = document.getElementById('regAge').value;
        const gender   = document.getElementById('regGender').value;
        const district = document.getElementById('regDistrict').value.trim();

        if (!name || !email || !password) {
            showModalMsg('Name, email and password are required.', true); return;
        }

        setLoading('doRegister', true);
        try {
            const res  = await fetch('/api/auth/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password, age, gender, district })
            });
            const data = await res.json();
            if (res.ok && data.success) {
                showModalMsg('\u2728 Welcome ' + name + '! Discovering your dosha...');
                setTimeout(() => { window.location.href = '/dosha-quiz'; }, 800);
            } else {
                showModalMsg(data.error || 'Signup failed. Try again.', true);
            }
        } catch (err) {
            showModalMsg('Network error. Is the server running?', true);
        } finally {
            setLoading('doRegister', false);
        }
    });

    [loginTab, regTab].forEach(t => t.addEventListener('click', () => {
        const el = document.getElementById('modalMsg'); if (el) el.textContent = '';
    }));

    // Expose for CTA buttons
    window._hideModal        = hideModal;
    window._showModal        = showModal;
    window._switchToRegister = switchToRegister;
}

function initSmoothScroll() {
    document.querySelectorAll('.nav-link').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const offsetPosition =
                    target.getBoundingClientRect().top + window.pageYOffset - navbarHeight - 15;
                window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
            }
            document.getElementById('navLinks')?.classList.remove('mobile-open');
        });
    });
}

function initActiveLinks() {
    const sections = document.querySelectorAll('#home, #features, #howitworks, #herbarium');
    const navLinks = document.querySelectorAll('.nav-link');

    const update = () => {
        let current = '';
        const navbarHeight = document.querySelector('.navbar').offsetHeight;
        sections.forEach(section => {
            const top    = section.offsetTop - navbarHeight - 80;
            const bottom = top + section.offsetHeight;
            if (window.scrollY >= top && window.scrollY < bottom) {
                current = section.getAttribute('id');
            }
        });
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').substring(1) === current) {
                link.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', update);
    window.addEventListener('load',   update);
}

function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    });
}

function initHamburger() {
    document.getElementById('hamburger').addEventListener('click', () => {
        document.getElementById('navLinks').classList.toggle('mobile-open');
    });
}

function initCTAButtons() {
    document.getElementById('ctaMain').addEventListener('click', () => {
        window._showModal();
        window._switchToRegister();
    });
    document.getElementById('ctaFooterBtn').addEventListener('click', () => {
        window._showModal();
        window._switchToRegister();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    renderHerbs();
    generateParticles();
    initHeadline();
    initThemeToggle();
    initModal();
    initSmoothScroll();
    initActiveLinks();
    initNavbarScroll();
    initHamburger();
    initCTAButtons();
});

