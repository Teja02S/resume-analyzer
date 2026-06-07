document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('resume');
    const jobDescInput = document.getElementById('jobDesc');
    const loading = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');

    if (!fileInput.files.length) {
        alert('Please select a resume file');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('job_description', jobDescInput.value);

    loading.style.display = 'block';
    resultsDiv.style.display = 'none';

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        loading.style.display = 'none';
    }
});

function displayResults(result) {
    const resultsDiv = document.getElementById('results');

    // Update scores
    document.getElementById('skillScore').textContent = result.skill_match_score + '%';
    document.getElementById('similarityScore').textContent = result.similarity_score + '%';
    document.getElementById('overallScore').textContent = result.overall_score + '%';

    // Display skills
    let skillsHTML = '';
    for (const [category, skills] of Object.entries(result.skills)) {
        if (skills.length > 0) {
            skillsHTML += `
                <div class="skill-category">
                    <h4>${category.replace(/_/g, ' ')}</h4>
                    ${skills.map(s => `<span class="skill-tag">${s}</span>`).join('')}
                </div>
            `;
        }
    }
    document.getElementById('skillsContainer').innerHTML = skillsHTML || '<p>No skills detected</p>';

    // Display matched skills
    let matchedHTML = '';
    for (const [category, skills] of Object.entries(result.matched_skills)) {
        if (skills.length > 0) {
            matchedHTML += `
                <div class="skill-category">
                    <h4>${category.replace(/_/g, ' ')}</h4>
                    ${skills.map(s => `<span class="skill-tag matched">${s}</span>`).join('')}
                </div>
            `;
        }
    }
    document.getElementById('matchedContainer').innerHTML = matchedHTML || '<p>No matched skills</p>';

    // Display entities
    let entitiesHTML = '';
    if (result.entities.person.length > 0) {
        entitiesHTML += `<div class="entity-item"><strong>Names:</strong> ${result.entities.person.join(', ')}</div>`;
    }
    if (result.entities.org.length > 0) {
        entitiesHTML += `<div class="entity-item"><strong>Organizations:</strong> ${result.entities.org.join(', ')}</div>`;
    }
    if (result.entities.gpe.length > 0) {
        entitiesHTML += `<div class="entity-item"><strong>Locations:</strong> ${result.entities.gpe.join(', ')}</div>`;
    }
    document.getElementById('entitiesContainer').innerHTML = entitiesHTML || '<p>No entities detected</p>';

    // Insert results template
    resultsDiv.innerHTML = getResultsTemplate();
    resultsDiv.style.display = 'block';
}

function getResultsTemplate() {
    return `
        <section class="results-section">
            <h2>Analysis Results</h2>
            <div class="score-cards">
                <div class="score-card">
                    <h3>Skill Match</h3>
                    <div class="score-value" id="skillScore">0%</div>
                </div>
                <div class="score-card">
                    <h3>Text Similarity</h3>
                    <div class="score-value" id="similarityScore">0%</div>
                </div>
                <div class="score-card">
                    <h3>Overall Score</h3>
                    <div class="score-value overall" id="overallScore">0%</div>
                </div>
            </div>
            <div class="skills-section">
                <h3>Extracted Skills</h3>
                <div id="skillsContainer"></div>
            </div>
            <div class="matched-section">
                <h3>Matched Skills</h3>
                <div id="matchedContainer"></div>
            </div>
            <div class="entities-section">
                <h3>Resume Information</h3>
                <div id="entitiesContainer"></div>
            </div>
            <button class="btn-secondary" onclick="location.reload()">Analyze Another Resume</button>
        </section>
    `;
}
