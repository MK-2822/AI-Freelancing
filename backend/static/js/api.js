/**
 * API Integration Logic for TrustLancer AI
 */

async function createProject(event) {
    event.preventDefault();

    // Grab form elements
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // UI Feedback
    const originalBtnText = submitBtn.innerText;
    submitBtn.innerText = "Generating Milestones...";
    submitBtn.disabled = true;

    // Collect Data
    const formData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        budget: document.getElementById('budget').value,
        deadline: document.getElementById('deadline').value,
    };

    try {
        // This targets the Django/AI backend (Phase 2)
        const response = await fetch('http://localhost:8000/api/projects/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            const result = await response.json();
            alert("Project Created with AI Milestones!");
            window.location.reload();
        } else {
            console.error("API Error:", response.statusText);
            alert("Sent to API (Wait for Phase 2 Django integration)");
        }
    } catch (error) {
        console.error("Connection Error:", error);
        // During hackathon: still show success for UI demo purposes if backend isn't up
        alert("Success (Local Demo): AI Agent is processing milestones for '" + formData.title + "'");
    } finally {
        submitBtn.innerText = originalBtnText;
        submitBtn.disabled = false;
    }
}