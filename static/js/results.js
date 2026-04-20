
const container = document.getElementById('resultsContent');

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
    const c = document.getElementById('particles');
    for (let i = 0; i < 30; i++) {
        const p = document.createElement('div');
        p.classList.add('particle');
        const size = Math.random() * 3 + 1;
        p.style.cssText = `width:${size}px;height:${size}px;left:${Math.random()*100}%;animation-duration:${12+Math.random()*20}s;animation-delay:${Math.random()*15}s`;
        c.appendChild(p);
    }
})();

window.addEventListener('scroll', () => {
    document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
});

function card(label, icon, content) {
    return `
        <div class="remedy-card">
            <div class="card-label"><i class="fas ${icon}"></i> ${label}</div>
            ${content}
        </div>`;
}

function renderSevere(data) {
    let doctorsHTML = '';
    if (data.doctors && data.doctors.length > 0) {
        const rows = data.doctors.map(d => `
            <div class="doctor-row">
                <div class="doctor-name"><i class="fas fa-user-md" style="color:var(--accent-gold);margin-right:0.4rem;"></i>${d.name}</div>
                <div class="doctor-detail">${d.address}</div>
                <div class="doctor-contact"><i class="fas fa-phone" style="margin-right:0.3rem;"></i>${d.contact}</div>
            </div>`).join('');
        doctorsHTML = card('Nearby Ayurvedic Doctors', 'fa-map-marker-alt', `<div class="doctors-section">${rows}</div>`);
    }

    container.innerHTML = `
        <div class="severe-card">
            <div class="severe-badge"><i class="fas fa-exclamation-triangle"></i> Critical Warning</div>
            <div class="severe-title">${data.disease}</div>
            <p class="severe-msg">${data.message}</p>
        </div>
        ${doctorsHTML}
        ${data.doctors && data.doctors.length === 0
            ? `<p style="color:var(--text-secondary);font-size:0.88rem;margin-top:0.5rem;">
                 No nearby doctors found for your registered district. Please visit your nearest hospital immediately.
               </p>`
            : ''}
    `;
}

function renderRemedy(data) {
    const meds = (data.medicines || '').split(',').map(m => m.trim()).filter(Boolean);
    const medPills = meds.length > 0
        ? `<div class="medicines-list">${meds.map(m => `<span class="med-pill">${m}</span>`).join('')}</div>`
        : '<p class="remedy-text">See remedy instructions above.</p>';

    container.innerHTML = `
        ${card('Identified Condition', 'fa-stethoscope', `
            <div class="disease-name">${data.disease}</div>
            <p class="reasoning-text">${data.reasoning}</p>
        `)}

        ${card('Recommended Remedy', 'fa-leaf', `
            <p class="remedy-text">${data.remedy}</p>
        `)}

        ${card('Ayurvedic Medicines', 'fa-mortar-pestle', medPills)}

        ${card('Preventive Advice', 'fa-shield-alt', `
            <p class="remedy-text">${data.preventive_advice}</p>
        `)}
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    const raw = sessionStorage.getItem('ayurResult');

    if (!raw) {
        container.innerHTML = `
            <div class="remedy-card" style="text-align:center;padding:3rem;">
                <p style="color:var(--text-secondary);margin-bottom:1rem;">No results found. Please run the symptom checker first.</p>
                <a href="/checker" class="btn-back"><i class="fas fa-arrow-left"></i> Go to Checker</a>
            </div>`;
        return;
    }

    const data = JSON.parse(raw);
    sessionStorage.removeItem('ayurResult'); // clean up

    if (data.is_severe) {
        renderSevere(data);
    } else {
        renderRemedy(data);
    }
});