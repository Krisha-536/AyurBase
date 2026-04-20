const selected = new Set();

const grid        = document.getElementById('symptomGrid');
const searchInput = document.getElementById('symptomSearch');
const selectedTags = document.getElementById('selectedTags');
const countBadge  = document.getElementById('countBadge');
const analyseBtn  = document.getElementById('analyseBtn');
const errorDiv    = document.getElementById('checkerError');

function renderPills(filter = '') {
    grid.innerHTML = '';
    const filtered = SYMPTOMS_LIST.filter(s =>
        s.toLowerCase().includes(filter.toLowerCase())
    );

    if (filtered.length === 0) {
        grid.innerHTML = '<span style="color:var(--text-secondary);font-size:0.85rem;font-style:italic;">No symptoms match your search.</span>';
        return;
    }

    filtered.forEach(symptom => {
        const pill = document.createElement('div');
        pill.className = 'symptom-pill' + (selected.has(symptom) ? ' selected' : '');
        pill.textContent = symptom.replace(/_/g, ' ');
        pill.dataset.symptom = symptom;
        pill.addEventListener('click', () => toggleSymptom(symptom));
        grid.appendChild(pill);
    });
}

function toggleSymptom(symptom) {
    if (selected.has(symptom)) {
        selected.delete(symptom);
    } else {
        selected.add(symptom);
    }
    renderPills(searchInput.value);
    updateSelectedTags();
    updateCounter();
}

function updateSelectedTags() {
    selectedTags.innerHTML = '';
    if (selected.size === 0) {
        selectedTags.innerHTML = '<span class="empty-msg">None selected yet</span>';
        return;
    }
    selected.forEach(symptom => {
        const tag = document.createElement('div');
        tag.className = 'selected-tag';
        tag.innerHTML = `
            ${symptom.replace(/_/g, ' ')}
            <span class="remove-tag" title="Remove">✕</span>
        `;
        tag.querySelector('.remove-tag').addEventListener('click', () => toggleSymptom(symptom));
        selectedTags.appendChild(tag);
    });
}

function updateCounter() {
    const n = selected.size;
    countBadge.textContent = `${n} selected`;
    countBadge.className   = 'count-badge' + (n >= 1 ? ' ready' : '');
    analyseBtn.disabled    = n < 1;
}

searchInput.addEventListener('input', () => renderPills(searchInput.value));

analyseBtn.addEventListener('click', async () => {
    errorDiv.style.display = 'none';
    analyseBtn.disabled    = true;
    analyseBtn.innerHTML   = '<span class="spinner"></span> Analysing...';

    try {
        const res  = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symptoms: [...selected] })
        });
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || 'Prediction failed.');
        }

        sessionStorage.setItem('ayurResult', JSON.stringify(data));
        window.location.href = '/results';

    } catch (err) {
        errorDiv.textContent   = err.message;
        errorDiv.style.display = 'block';
        analyseBtn.disabled    = false;
        analyseBtn.textContent = 'Analyse My Symptoms →';
    }
});


document.getElementById('logoutBtn').addEventListener('click', async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    window.location.href = '/';
});

document.getElementById('themeToggle').addEventListener('click', () => {
    document.body.classList.toggle('light');
    const icon = document.getElementById('themeToggle').querySelector('i');
    icon.className = document.body.classList.contains('light') ? 'fas fa-sun' : 'fas fa-moon';
});


(function generateParticles() {
    const container = document.getElementById('particles');
    for (let i = 0; i < 30; i++) {
        const p = document.createElement('div');
        p.classList.add('particle');
        const size = Math.random() * 3 + 1;
        p.style.cssText = `width:${size}px;height:${size}px;left:${Math.random()*100}%;animation-duration:${12+Math.random()*20}s;animation-delay:${Math.random()*15}s`;
        container.appendChild(p);
    }
})();

window.addEventListener('scroll', () => {
    document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
});

renderPills();
updateCounter();