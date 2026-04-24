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

function renderSevere(data) {
    let doctorsHtml = '';
    if (data.doctors && data.doctors.length > 0) {
        doctorsHtml = `
            <div class="remedy-card" style="margin-top:1.2rem;">
                <div class="card-label"><i class="fas fa-user-md"></i> Nearby Ayurvedic Doctors</div>
                <div class="doctors-section">
                    ${data.doctors.map(d => `
                        <div class="doctor-row">
                            <div class="doctor-name">${d.name}</div>
                            <div class="doctor-detail">${d.address}</div>
                            <div class="doctor-contact"><i class="fas fa-phone"></i> ${d.contact}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    } else {
        doctorsHtml = `<p style="color:var(--text-secondary);font-size:0.88rem;margin-top:0.8rem;">No nearby doctors found for your district. Please visit your nearest hospital immediately.</p>`;
    }

    return `
        <div class="severe-card">
            <div class="severe-badge"><i class="fas fa-exclamation-triangle"></i> Critical Warning</div>
            <div class="severe-title">${data.disease}</div>
            <div class="severe-msg">${data.message}</div>
        </div>
        ${doctorsHtml}
    `;
}

function renderRemedy(data) {
    const medicines = data.medicines && data.medicines !== 'N/A'
        ? data.medicines.split(',').map(m => `<span class="med-pill">${m.trim()}</span>`).join('')
        : '<span style="color:var(--text-secondary);font-size:0.85rem;">Consult a practitioner for specific medicines.</span>';

    return `
        <div class="remedy-card">
            <div class="card-label"><i class="fas fa-diagnoses"></i> Predicted Condition</div>
            <div class="disease-name">${data.disease}</div>
            <div class="reasoning-text">${data.reasoning}</div>
        </div>

        <div class="remedy-card">
            <div class="card-label"><i class="fas fa-mortar-pestle"></i> Ayurvedic Remedy</div>
            <div class="remedy-text">${data.remedy}</div>
        </div>

        <div class="remedy-card">
            <div class="card-label"><i class="fas fa-pills"></i> Recommended Medicines</div>
            <div class="medicines-list">${medicines}</div>
        </div>

        <div class="remedy-card">
            <div class="card-label"><i class="fas fa-shield-alt"></i> Preventive Advice</div>
            <div class="remedy-text">${data.preventive_advice}</div>
        </div>
    `;
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

    const raw = sessionStorage.getItem('ayursense_result');
    const container = document.getElementById('resultsContent');

    if (!raw) {
        container.innerHTML = `
            <div class="remedy-card" style="text-align:center;padding:3rem 2rem;">
                <i class="fas fa-exclamation-circle" style="font-size:2rem;color:var(--accent-gold);margin-bottom:1rem;display:block;"></i>
                <div style="color:var(--text-secondary);font-size:0.95rem;">No results found. Please go back and analyse your symptoms first.</div>
            </div>
        `;
        return;
    }

    const data = JSON.parse(raw);
    container.innerHTML = data.is_severe ? renderSevere(data) : renderRemedy(data);
    sessionStorage.removeItem('ayursense_result');
});
