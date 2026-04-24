let selectedSymptoms = [];

function generateParticles() {
    const container = document.getElementById('particles');
    for (let i = 0; i < 30; i++) {
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

function renderSymptoms(filter = '') {
    const grid = document.getElementById('symptomGrid');
    grid.innerHTML = '';
    const filtered = SYMPTOMS_LIST.filter(s =>
        s.toLowerCase().includes(filter.toLowerCase())
    );

    filtered.forEach(symptom => {
        const pill = document.createElement('div');
        pill.className = 'symptom-pill' + (selectedSymptoms.includes(symptom) ? ' selected' : '');
        pill.textContent = symptom.replace(/_/g, ' ');
        pill.addEventListener('click', () => toggleSymptom(symptom));
        grid.appendChild(pill);
    });

    if (filtered.length === 0) {
        grid.innerHTML = '<div style="color:var(--text-secondary);font-size:0.85rem;padding:0.5rem;">No symptoms match your search.</div>';
    }
}

function toggleSymptom(symptom) {
    const idx = selectedSymptoms.indexOf(symptom);
    if (idx === -1) {
        selectedSymptoms.push(symptom);
    } else {
        selectedSymptoms.splice(idx, 1);
    }
    updateSelectedTags();
    renderSymptoms(document.getElementById('symptomSearch').value);
    updateCounter();
}

function updateSelectedTags() {
    const container = document.getElementById('selectedTags');
    if (selectedSymptoms.length === 0) {
        container.innerHTML = '<span class="empty-msg">None selected yet</span>';
        return;
    }
    container.innerHTML = selectedSymptoms.map(s => `
        <div class="selected-tag">
            ${s.replace(/_/g, ' ')}
            <span class="remove-tag" onclick="toggleSymptom('${s}')">✕</span>
        </div>
    `).join('');
}

function updateCounter() {
    const badge = document.getElementById('countBadge');
    const btn   = document.getElementById('analyseBtn');
    const count = selectedSymptoms.length;

    badge.textContent = count + (count === 1 ? ' selected' : ' selected');
    badge.classList.toggle('ready', count >= 2);
    btn.disabled = count < 2;
}

document.addEventListener('DOMContentLoaded', () => {
    generateParticles();

    document.getElementById('themeToggle').addEventListener('click', () => {
        document.body.classList.toggle('light');
        const icon = document.getElementById('themeToggle').querySelector('i');
        icon.className = document.body.classList.contains('light') ? 'fas fa-sun' : 'fas fa-moon';
    });

    document.getElementById('logoutBtn').addEventListener('click', async () => {
        await fetch('/api/auth/logout', { method: 'POST' });
        window.location.href = '/';
    });

    renderSymptoms();

    document.getElementById('symptomSearch').addEventListener('input', (e) => {
        renderSymptoms(e.target.value);
    });

    document.getElementById('analyseBtn').addEventListener('click', async () => {
        const btn = document.getElementById('analyseBtn');
        const err = document.getElementById('checkerError');
        err.style.display = 'none';
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> Analysing…';

        try {
            const res  = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symptoms: selectedSymptoms })
            });
            const data = await res.json();

            if (!res.ok) {
                err.textContent = data.error || 'Something went wrong. Please try again.';
                err.style.display = 'block';
                btn.disabled = false;
                btn.innerHTML = 'Analyse My Symptoms →';
                return;
            }

            sessionStorage.setItem('ayursense_result', JSON.stringify(data));
            window.location.href = '/results';
        } catch {
            err.textContent = 'Network error. Is the server running?';
            err.style.display = 'block';
            btn.disabled = false;
            btn.innerHTML = 'Analyse My Symptoms →';
        }
    });
});

