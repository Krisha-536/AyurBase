const QUESTIONS = [
    {
        text: "How would you describe your body frame?",
        options: [
            { label: "Thin & light",      desc: "I find it hard to gain weight. Bony frame, prominent joints.", dosha: "Vata",  scores: { vata:3, pitta:0, kapha:0 } },
            { label: "Medium & muscular", desc: "Moderate build, well-proportioned, gains and loses weight easily.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "Large & sturdy",    desc: "Broad frame, tends to gain weight easily and keep it.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    },
    {
        text: "How is your skin typically?",
        options: [
            { label: "Dry, rough or flaky",        desc: "Skin cracks easily, gets dehydrated fast.", dosha: "Vata",  scores: { vata:3, pitta:0, kapha:0 } },
            { label: "Warm, oily or prone to redness", desc: "Sensitive skin, acne or rashes sometimes.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "Thick, smooth and moist",    desc: "Rarely gets dry, generally soft and hydrated.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    },
    {
        text: "How would you describe your appetite and digestion?",
        options: [
            { label: "Irregular — sometimes hungry, sometimes not", desc: "Digestion varies, can get bloated or gassy.", dosha: "Vata",  scores: { vata:3, pitta:1, kapha:0 } },
            { label: "Strong — I get irritable if I skip meals",    desc: "Sharp appetite, good digestion but can get acid reflux.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "Slow but steady",                            desc: "Can skip meals easily, digestion is slow but consistent.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    },
    {
        text: "How do you handle stress?",
        options: [
            { label: "Anxiety and worry",      desc: "I overthink and feel nervous under pressure.", dosha: "Vata",  scores: { vata:3, pitta:0, kapha:0 } },
            { label: "Anger and frustration",  desc: "I get irritated and need to solve things immediately.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "Withdrawal and silence", desc: "I go quiet and avoid confrontation when stressed.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    },
    {
        text: "What is your typical sleep pattern?",
        options: [
            { label: "Light sleeper, often wake up",         desc: "Mind races at night, hard to fall asleep.", dosha: "Vata",  scores: { vata:3, pitta:0, kapha:0 } },
            { label: "Moderate — 6–7 hrs, wake up refreshed", desc: "Fall asleep reasonably well, don't need too much.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "Deep, long sleeper — 8+ hours",        desc: "Love sleep, hard to wake up, feel groggy sometimes.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    },
    {
        text: "How do you prefer the weather?",
        options: [
            { label: "Warm and humid",  desc: "I dislike cold and wind, always reaching for a blanket.", dosha: "Vata",  scores: { vata:3, pitta:0, kapha:0 } },
            { label: "Cool and breezy", desc: "Heat bothers me, I love cooler climates.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "Warm and dry",    desc: "I dislike cold and damp, prefer sunny dry days.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    },
    {
        text: "How would you describe your mind and thinking style?",
        options: [
            { label: "Creative and quick but scattered",  desc: "Many ideas, but hard to focus. Learn fast, forget fast.", dosha: "Vata",  scores: { vata:3, pitta:0, kapha:0 } },
            { label: "Sharp, analytical and decisive",   desc: "Good problem-solver, strong opinions.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "Calm, steady and slow to decide",  desc: "Think before acting, good long-term memory.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    },
    {
        text: "What is your energy level like through the day?",
        options: [
            { label: "Bursts of energy followed by fatigue", desc: "I go hard then crash. Inconsistent throughout the day.", dosha: "Vata",  scores: { vata:3, pitta:0, kapha:0 } },
            { label: "High, focused energy most of the day", desc: "Sustained drive, especially towards goals.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "Steady but slow — takes time to get going", desc: "Low in the morning, builds up gradually.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    },
    {
        text: "How do you approach exercise?",
        options: [
            { label: "I enjoy light activities — yoga, walking",  desc: "High-intensity tires me quickly.", dosha: "Vata",  scores: { vata:3, pitta:0, kapha:0 } },
            { label: "I love intensity — running, competition",   desc: "Competitive, motivated by challenge.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "I need motivation to exercise consistently", desc: "Once started I enjoy it, but getting started is hard.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    },
    {
        text: "Which best describes your emotional nature?",
        options: [
            { label: "Enthusiastic but anxious",    desc: "Excited easily, but also worried easily.", dosha: "Vata",  scores: { vata:3, pitta:0, kapha:0 } },
            { label: "Passionate and determined",   desc: "Strong feelings, strong opinions. Natural leader.", dosha: "Pitta", scores: { vata:0, pitta:3, kapha:0 } },
            { label: "Calm, loving and nurturing",  desc: "Patient, empathetic, takes a lot to upset me.", dosha: "Kapha", scores: { vata:0, pitta:0, kapha:3 } }
        ]
    }
];

const DOSHA_INFO = {
    Vata: {
        icon: "💨",
        desc: "You are governed by air & space. You're creative, energetic and adaptable — but tend towards anxiety and irregular routines when imbalanced. Warming, grounding foods and herbs like Ashwagandha will serve you well."
    },
    Pitta: {
        icon: "🔥",
        desc: "You are governed by fire & water. You're sharp, driven and confident — but can tip into inflammation or anger when out of balance. Cooling, calming herbs like Amla and Brahmi are your allies."
    },
    Kapha: {
        icon: "🌊",
        desc: "You are governed by earth & water. You're steady, compassionate and strong — but may struggle with sluggishness or weight gain when imbalanced. Stimulating herbs like Neem and Tulsi help keep you vibrant."
    }
};

let current  = 0;
let answers  = new Array(QUESTIONS.length).fill(null); 

const questionArea  = document.getElementById('questionArea');
const progressFill  = document.getElementById('progressFill');
const progressLabel = document.getElementById('progressLabel');
const btnPrev       = document.getElementById('btnPrev');
const btnNext       = document.getElementById('btnNext');

function renderQuestion(idx) {
    const q = QUESTIONS[idx];
    const selected = answers[idx];

    const pct = Math.round(((idx + 1) / QUESTIONS.length) * 100);
    progressFill.style.width  = pct + '%';
    progressLabel.textContent = `Question ${idx + 1} of ${QUESTIONS.length}`;

    btnPrev.disabled = idx === 0;
    btnNext.disabled = selected === null;
    btnNext.textContent = idx === QUESTIONS.length - 1 ? 'See My Dosha ✦' : 'Next →';

    const letters = ['A', 'B', 'C'];
    const optionsHTML = q.options.map((opt, oi) => `
        <button class="option-btn ${selected === oi ? 'selected' : ''}" data-idx="${oi}">
            <div class="option-letter">${letters[oi]}</div>
            <div class="option-content">
                <div class="option-label">${opt.label}</div>
                <div class="option-desc">${opt.desc}</div>
            </div>
        </button>
    `).join('');

    questionArea.innerHTML = `
        <div class="question-card">
            <div class="q-number">Question ${idx + 1}</div>
            <div class="q-text">${q.text}</div>
            <div class="options-grid">${optionsHTML}</div>
        </div>
    `;

    questionArea.querySelectorAll('.option-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            answers[idx] = parseInt(btn.dataset.idx);
            renderQuestion(idx);
        });
    });
}

btnPrev.addEventListener('click', () => {
    if (current > 0) { current--; renderQuestion(current); }
});

btnNext.addEventListener('click', () => {
    if (answers[current] === null) return;
    if (current < QUESTIONS.length - 1) {
        current++;
        renderQuestion(current);
    } else {
        showResult();
    }
});

function showResult() {
    const scores = { vata: 0, pitta: 0, kapha: 0 };
    answers.forEach((ansIdx, qIdx) => {
        if (ansIdx !== null) {
            const s = QUESTIONS[qIdx].options[ansIdx].scores;
            scores.vata  += s.vata;
            scores.pitta += s.pitta;
            scores.kapha += s.kapha;
        }
    });

    const total = scores.vata + scores.pitta + scores.kapha || 1;
    const pcts  = {
        Vata:  Math.round((scores.vata  / total) * 100),
        Pitta: Math.round((scores.pitta / total) * 100),
        Kapha: Math.round((scores.kapha / total) * 100),
    };

    const dominant = Object.entries(pcts).sort((a,b) => b[1]-a[1])[0][0];
    const info = DOSHA_INFO[dominant];

    document.getElementById('resultIcon').textContent      = info.icon;
    document.getElementById('resultDoshaName').textContent = dominant;
    document.getElementById('resultDesc').textContent      = info.desc;

    const barsHTML = Object.entries(pcts).map(([name, pct]) => `
        <div class="dosha-bar-row">
            <div class="dosha-bar-label">${name}</div>
            <div class="dosha-bar-track">
                <div class="dosha-bar-fill" style="width:0%" data-target="${pct}"></div>
            </div>
            <div class="dosha-bar-pct">${pct}%</div>
        </div>
    `).join('');
    document.getElementById('doshaBars').innerHTML = barsHTML;

    const overlay = document.getElementById('resultOverlay');
    overlay.style.display = 'flex';
    setTimeout(() => {
        overlay.querySelectorAll('.dosha-bar-fill').forEach(el => {
            el.style.width = el.dataset.target + '%';
        });
    }, 150);

    document.getElementById('btnProceed').addEventListener('click', () => saveAndProceed(dominant));
}

async function saveAndProceed(dosha) {
    const btn     = document.getElementById('btnProceed');
    const msg     = document.getElementById('savingMsg');
    btn.disabled  = true;
    btn.textContent = 'Saving...';
    msg.textContent = 'Saving your Prakriti profile...';

    try {
        const res = await fetch('/api/auth/save-dosha', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dosha })
        });
        const data = await res.json();

        if (res.ok && data.success) {
            msg.textContent = '✦ Dosha saved! Taking you to the checker...';
            setTimeout(() => { window.location.href = '/checker'; }, 900);
        } else {
            msg.textContent = data.error || 'Could not save. Please try again.';
            btn.disabled    = false;
            btn.textContent = 'Begin Symptom Check →';
        }
    } catch (err) {
        msg.textContent = 'Network error. Is the server running?';
        btn.disabled    = false;
        btn.textContent = 'Begin Symptom Check →';
    }
}

(function init() {
    // Particles
    const container = document.getElementById('particles');
    for (let i = 0; i < 30; i++) {
        const p = document.createElement('div');
        p.classList.add('particle');
        const size = Math.random() * 3 + 1;
        p.style.cssText = `width:${size}px;height:${size}px;left:${Math.random()*100}%;animation-duration:${12+Math.random()*20}s;animation-delay:${Math.random()*15}s`;
        container.appendChild(p);
    }

    document.getElementById('themeToggle').addEventListener('click', () => {
        document.body.classList.toggle('light');
        const icon = document.querySelector('#themeToggle i');
        icon.className = document.body.classList.contains('light') ? 'fas fa-sun' : 'fas fa-moon';
    });

    document.getElementById('logoutBtn').addEventListener('click', async () => {
        await fetch('/api/auth/logout', { method: 'POST' });
        window.location.href = '/';
    });

    window.addEventListener('scroll', () => {
        document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
    });

    renderQuestion(0);
})();
