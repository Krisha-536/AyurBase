
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("remedyForm");

    if (form) {
        form.addEventListener("submit", function (e) {

            const concern = form.querySelector("input[name='concern']").value.trim();
            const season = form.querySelector("select[name='season']").value;
            const digestion = form.querySelector("select[name='digestion_strength']").value;

            if (!concern || !season || !digestion) {
                e.preventDefault();
                alert("Please fill all required fields!");
                return;
            }

            const btn = form.querySelector("button");
            btn.textContent = "Generating...";
            btn.disabled = true;
        });
    }
});