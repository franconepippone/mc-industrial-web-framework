const versionsJava = JSON.parse(document.getElementById('versions-java-data').textContent);
const versionsBedrock = JSON.parse(document.getElementById('versions-bedrock-data').textContent);

const filterForm = document.getElementById('filter-form');
const editionSelect = document.getElementById('edition-select');
const versionFrom = document.getElementById('version-from');
const versionTo = document.getElementById('version-to');
const deviceClassSelect = document.getElementById('device-class-select');
const filterPanels = document.querySelectorAll('.device-filter-panel');
const resultsContent = document.getElementById('results-content');
let autoRefreshHandle = null;

function setOptions(select, options) {
    select.innerHTML = '<option value="">Any</option>';
    options.forEach((value) => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });
}

function syncVersions() {
    const edition = editionSelect.value;
    if (edition === 'Java') {
        setOptions(versionFrom, versionsJava);
        setOptions(versionTo, versionsJava);
    } else if (edition === 'Bedrock') {
        setOptions(versionFrom, versionsBedrock);
        setOptions(versionTo, versionsBedrock);
    } else {
        setOptions(versionFrom, []);
        setOptions(versionTo, []);
    }
}

function syncDevicePanels() {
    const selectedClass = deviceClassSelect.value;
    filterPanels.forEach((panel) => {
        panel.classList.toggle('d-none', panel.dataset.deviceClass !== selectedClass);
    });
}

function parseOptionalNumber(id) {
    const field = document.getElementById(id);
    if (!field) return null;

    const value = field.value.trim();
    if (!value) return null;

    const parsed = Number(value);
    return Number.isNaN(parsed) ? null : parsed;
}

function collectFilters() {
    const selectedClass = deviceClassSelect.value;
    const filters = {
        device_class: selectedClass,
        edition: editionSelect.value || null,
        version_from: versionFrom.value || null,
        version_to: versionTo.value || null,
    };

    if (selectedClass === 'rds-router') {
        Object.assign(filters, {
            protocol: document.getElementById('router-protocol')?.value || null,
            package_tech: document.getElementById('router-package-tech')?.value || null,
            min_throughput: parseOptionalNumber('router-min-throughput'),
            min_physical_input: parseOptionalNumber('router-min-physical-input'),
            min_physical_output: parseOptionalNumber('router-min-physical-output'),
            max_length: parseOptionalNumber('router-max-length'),
            max_width: parseOptionalNumber('router-max-width'),
            max_height: parseOptionalNumber('router-max-height'),
            survival_friendliness: document.getElementById('router-survival')?.value || null,
            works_in_nether: document.getElementById('nether')?.checked ? true : null,
            queue_included: document.getElementById('queue')?.checked ? true : null,
            chunkloading_included: document.getElementById('chunk')?.checked ? true : null,
            hierarchical_routing: document.getElementById('hierarchical-routing')?.checked ? true : null,
            non_directional: document.getElementById('directional')?.checked ? true : null,
            non_locational: document.getElementById('locational')?.checked ? true : null,
        });
    }

    return filters;
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

async function applyFilters() {
    const filters = collectFilters();
    resultsContent.classList.add('opacity-50');

    try {
        const response = await fetch('/filter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters),
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        resultsContent.innerHTML = await response.text();
    } catch (error) {
        resultsContent.innerHTML = `
            <div class="alert alert-danger small mb-0">
                Could not load filtered results: ${escapeHtml(error.message)}
            </div>
        `;
    } finally {
        resultsContent.classList.remove('opacity-50');
    }
}

function startAutoRefresh() {
    if (autoRefreshHandle) {
        window.clearInterval(autoRefreshHandle);
    }

    autoRefreshHandle = window.setInterval(() => {
        applyFilters();
    }, 1500);
}

filterForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    await applyFilters();
});

filterForm.addEventListener('reset', () => {
    window.setTimeout(() => {
        syncVersions();
        syncDevicePanels();
    }, 0);
});

editionSelect.addEventListener('change', () => {
    syncVersions();
});

deviceClassSelect.addEventListener('change', () => {
    syncDevicePanels();
    applyFilters();
});

document.addEventListener('DOMContentLoaded', () => {
    syncVersions();
    syncDevicePanels();
    startAutoRefresh();

    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((element) => {
        new bootstrap.Tooltip(element);
    });
});
