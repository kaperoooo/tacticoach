const formationMap = {
  '4-3-3': [
    [0.16, 0.50], [0.35, 0.20], [0.35, 0.50], [0.35, 0.80],
    [0.52, 0.26], [0.52, 0.50], [0.52, 0.74], [0.69, 0.20],
    [0.69, 0.50], [0.69, 0.80], [0.85, 0.50]
  ],
  '4-4-2': [
    [0.16, 0.50], [0.35, 0.18], [0.35, 0.50], [0.35, 0.82],
    [0.50, 0.18], [0.50, 0.50], [0.50, 0.82], [0.65, 0.18],
    [0.65, 0.50], [0.65, 0.82], [0.84, 0.50]
  ],
  '4-2-3-1': [
    [0.16, 0.50], [0.35, 0.22], [0.35, 0.50], [0.35, 0.78],
    [0.52, 0.30], [0.52, 0.72], [0.64, 0.18], [0.64, 0.50],
    [0.64, 0.82], [0.78, 0.50], [0.86, 0.50]
  ],
  '3-5-2': [
    [0.16, 0.50], [0.30, 0.22], [0.30, 0.50], [0.30, 0.78],
    [0.50, 0.18], [0.50, 0.35], [0.50, 0.65], [0.50, 0.82],
    [0.70, 0.25], [0.70, 0.50], [0.70, 0.75]
  ],
  '3-4-3': [
    [0.16, 0.50], [0.30, 0.25], [0.30, 0.50], [0.30, 0.75],
    [0.48, 0.18], [0.48, 0.38], [0.48, 0.62], [0.48, 0.82],
    [0.72, 0.25], [0.72, 0.50], [0.72, 0.75]
  ],
  '4-1-4-1': [
    [0.16, 0.50], [0.34, 0.20], [0.34, 0.50], [0.34, 0.80],
    [0.50, 0.50], [0.58, 0.18], [0.58, 0.38], [0.58, 0.62],
    [0.58, 0.82], [0.75, 0.50], [0.86, 0.50]
  ]
};

const state = {
  projects: [],
  selectedProjectId: null,
  selectedSchemeId: null,
  currentField: { players: [], ball: null, markers: [], arrows: [], lines: [] },
  activeTool: 'select',
  dragPlayerId: null,
  dragOffset: { x: 0, y: 0 },
  scenarioSteps: [],
};

const projectList = document.getElementById('projectList');
const projectNameInput = document.getElementById('projectName');
const schemeNameInput = document.getElementById('schemeName');
const scenarioNameInput = document.getElementById('scenarioName');
const formationSelect = document.getElementById('formationSelect');
const activeProjectTitle = document.getElementById('activeProjectTitle');
const statusBadge = document.getElementById('statusBadge');
const pitchSvg = document.getElementById('pitchSvg');

function setStatus(text, tone = 'ok') {
  statusBadge.textContent = text;
  if (tone === 'error') {
    statusBadge.style.background = 'rgba(255,98,98,0.18)';
    statusBadge.style.color = '#ffb8b8';
  } else if (tone === 'warn') {
    statusBadge.style.background = 'rgba(255,182,77,0.18)';
    statusBadge.style.color = '#ffdba0';
  } else {
    statusBadge.style.background = 'rgba(38,208,125,0.18)';
    statusBadge.style.color = '#7ef0bc';
  }
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || `Request failed: ${response.status}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

function buildFormationOptions() {
  formationSelect.innerHTML = '';
  Object.keys(formationMap).forEach((name) => {
    const option = document.createElement('option');
    option.value = name;
    option.textContent = name;
    formationSelect.appendChild(option);
  });
  formationSelect.value = '4-3-3';
}

function renderProjectList() {
  projectList.innerHTML = '';
  state.projects.forEach((project) => {
    const item = document.createElement('li');
    item.textContent = project.name;
    item.className = project.id === state.selectedProjectId ? 'active' : '';
    item.addEventListener('click', () => selectProject(project.id));
    projectList.appendChild(item);
  });
}

async function loadProjects() {
  try {
    const projects = await fetchJson('/api/projects');
    state.projects = projects;
    renderProjectList();
    if (projects.length && !state.selectedProjectId) {
      await selectProject(projects[0].id);
    }
    if (!projects.length) {
      state.selectedProjectId = null;
      activeProjectTitle.textContent = 'No project selected';
    }
  } catch (error) {
    setStatus(error.message, 'error');
  }
}

async function selectProject(projectId) {
  state.selectedProjectId = projectId;
  const project = state.projects.find((item) => item.id === projectId);
  activeProjectTitle.textContent = project ? project.name : 'No project selected';
  renderProjectList();
  await loadProjectDetails(projectId);
}

async function loadProjectDetails(projectId) {
  if (!projectId) return;
  try {
    const [schemes, scenarios] = await Promise.all([
      fetchJson(`/api/projects/${projectId}/schemes`),
      fetchJson(`/api/projects/${projectId}/scenarios`),
    ]);
    state.selectedSchemeId = schemes[0]?.id || null;
    if (schemes.length) {
      const scheme = schemes[0];
      schemeNameInput.value = scheme.name;
      formationSelect.value = scheme.formation || '4-3-3';
      state.currentField = scheme.data || { players: [], ball: null, markers: [], arrows: [], lines: [] };
    } else {
      schemeNameInput.value = '';
      state.currentField = { players: [], ball: null, markers: [], arrows: [], lines: [] };
    }
    state.scenarioSteps = scenarios[0]?.steps || [];
    renderPitch();
    setStatus('Project loaded');
  } catch (error) {
    setStatus(error.message, 'error');
  }
}

async function createProject() {
  const cleaned = projectNameInput.value.trim();
  if (!cleaned) {
    setStatus('Project name is required', 'warn');
    return;
  }
  try {
    const project = await fetchJson('/api/projects', {
      method: 'POST',
      body: JSON.stringify({ name: cleaned, description: 'Created from TactiCoach', team_name: 'Home' }),
    });
    projectNameInput.value = '';
    state.projects.unshift(project);
    renderProjectList();
    await selectProject(project.id);
    setStatus('Project created');
  } catch (error) {
    setStatus(error.message, 'error');
  }
}

async function saveCurrentScheme() {
  if (!state.selectedProjectId) {
    setStatus('Select a project first', 'warn');
    return;
  }
  const name = schemeNameInput.value.trim() || 'New scheme';
  const payload = {
    name,
    formation: formationSelect.value,
    attack_direction: 'left-to-right',
    orientation: 'home-right',
    data: state.currentField,
  };
  try {
    if (state.selectedSchemeId) {
      await fetchJson(`/api/projects/${state.selectedProjectId}/schemes/${state.selectedSchemeId}`, {
        method: 'PUT',
        body: JSON.stringify(payload),
      });
    } else {
      const result = await fetchJson(`/api/projects/${state.selectedProjectId}/schemes`, {
        method: 'POST',
        body: JSON.stringify(payload),
      });
      state.selectedSchemeId = result.id;
    }
    setStatus('Scheme saved');
    await loadProjectDetails(state.selectedProjectId);
  } catch (error) {
    setStatus(error.message, 'error');
  }
}

async function saveScenario() {
  if (!state.selectedProjectId) {
    setStatus('Select a project first', 'warn');
    return;
  }
  const name = scenarioNameInput.value.trim();
  if (!name) {
    setStatus('Scenario name is required', 'warn');
    return;
  }
  try {
    await fetchJson(`/api/projects/${state.selectedProjectId}/scenarios`, {
      method: 'POST',
      body: JSON.stringify({ name, description: 'Custom scenario', steps: state.scenarioSteps }),
    });
    scenarioNameInput.value = '';
    setStatus('Scenario saved');
    await loadProjectDetails(state.selectedProjectId);
  } catch (error) {
    setStatus(error.message, 'error');
  }
}

function applyFormation() {
  const formation = formationSelect.value;
  const preset = formationMap[formation] || formationMap['4-3-3'];
  state.currentField.players = preset.map(([x, y], index) => ({
    id: `player-${Date.now()}-${index}`,
    x,
    y,
    label: String(index + 1),
    team: 'home',
  }));
  state.currentField.ball = { x: 0.5, y: 0.5 };
  renderPitch();
  setStatus(`Formation ${formation} applied`);
}

function renderPitch() {
  pitchSvg.innerHTML = '';
  const width = 1000;
  const height = 680;
  const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
  bg.setAttribute('x', 0); bg.setAttribute('y', 0); bg.setAttribute('width', width); bg.setAttribute('height', height);
  bg.setAttribute('fill', '#198b4d');
  bg.setAttribute('stroke', '#dff4e6');
  bg.setAttribute('stroke-width', 2);
  pitchSvg.appendChild(bg);

  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
  marker.setAttribute('id', 'arrow-head');
  marker.setAttribute('markerWidth', '10'); marker.setAttribute('markerHeight', '10');
  marker.setAttribute('refX', '8'); marker.setAttribute('refY', '3'); marker.setAttribute('orient', 'auto');
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', 'M0,0 L0,6 L9,3 z');
  path.setAttribute('fill', '#ffef7a');
  marker.appendChild(path);
  defs.appendChild(marker);
  pitchSvg.appendChild(defs);

  const lines = [
    { x1: 500, y1: 0, x2: 500, y2: 680 },
    { x1: 0, y1: 340, x2: 1000, y2: 340 },
    { x1: 70, y1: 70, x2: 70, y2: 610 },
    { x1: 930, y1: 70, x2: 930, y2: 610 },
    { x1: 70, y1: 0, x2: 70, y2: 680 },
    { x1: 930, y1: 0, x2: 930, y2: 680 },
  ];
  lines.forEach((line) => {
    const el = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    el.setAttribute('x1', line.x1); el.setAttribute('x2', line.x2); el.setAttribute('y1', line.y1); el.setAttribute('y2', line.y2);
    el.setAttribute('stroke', 'rgba(255,255,255,0.8)');
    el.setAttribute('stroke-width', 2);
    pitchSvg.appendChild(el);
  });

  if (state.currentField.ball) {
    const ball = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    ball.setAttribute('cx', state.currentField.ball.x * width);
    ball.setAttribute('cy', state.currentField.ball.y * height);
    ball.setAttribute('r', 8);
    ball.setAttribute('fill', '#f9f3f2');
    ball.setAttribute('stroke', '#101010');
    ball.setAttribute('stroke-width', 2);
    pitchSvg.appendChild(ball);
  }

  state.currentField.markers.forEach((marker) => {
    const shape = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    const cx = marker.x * width;
    const cy = marker.y * height;
    shape.setAttribute('points', `${cx},${cy - 18} ${cx - 12},${cy + 18} ${cx + 12},${cy + 18}`);
    shape.setAttribute('fill', '#f4af52');
    shape.setAttribute('stroke', '#fff');
    pitchSvg.appendChild(shape);
  });

  state.currentField.lines.forEach((line) => {
    const el = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    el.setAttribute('x1', line.x1 * width); el.setAttribute('y1', line.y1 * height);
    el.setAttribute('x2', line.x2 * width); el.setAttribute('y2', line.y2 * height);
    el.setAttribute('stroke', line.color || '#ffffff');
    el.setAttribute('stroke-width', 3);
    el.setAttribute('stroke-linecap', 'round');
    pitchSvg.appendChild(el);
  });

  state.currentField.arrows.forEach((arrow) => {
    const el = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    el.setAttribute('x1', arrow.x1 * width); el.setAttribute('y1', arrow.y1 * height);
    el.setAttribute('x2', arrow.x2 * width); el.setAttribute('y2', arrow.y2 * height);
    el.setAttribute('stroke', '#ffe071');
    el.setAttribute('stroke-width', 3);
    el.setAttribute('marker-end', 'url(#arrow-head)');
    pitchSvg.appendChild(el);
  });

  state.currentField.players.forEach((player) => {
    const playerGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    playerGroup.setAttribute('data-player-id', player.id);
    playerGroup.style.cursor = 'pointer';

    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', player.x * width);
    circle.setAttribute('cy', player.y * height);
    circle.setAttribute('r', 18);
    circle.setAttribute('fill', player.team === 'away' ? '#ed5c68' : '#4a9bff');
    circle.setAttribute('stroke', '#ffffff');
    circle.setAttribute('stroke-width', 2);
    circle.setAttribute('data-player-id', player.id);

    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', player.x * width);
    label.setAttribute('y', player.y * height + 5);
    label.setAttribute('fill', '#ffffff');
    label.setAttribute('text-anchor', 'middle');
    label.setAttribute('font-size', '12');
    label.setAttribute('font-weight', '700');
    label.textContent = player.label || '1';

    playerGroup.appendChild(circle);
    playerGroup.appendChild(label);
    pitchSvg.appendChild(playerGroup);
  });

  pitchSvg.onpointerdown = handlePitchPointerDown;
}

function handlePitchPointerDown(event) {
  const svgRect = pitchSvg.getBoundingClientRect();
  const x = (event.clientX - svgRect.left) / svgRect.width;
  const y = (event.clientY - svgRect.top) / svgRect.height;
  const playerTarget = event.target.closest('[data-player-id]');

  if (state.activeTool === 'select') {
    if (playerTarget) {
      const playerId = playerTarget.getAttribute('data-player-id');
      const player = state.currentField.players.find((p) => p.id === playerId);
      if (!player) return;
      state.dragPlayerId = playerId;
      const dx = x - player.x;
      const dy = y - player.y;
      state.dragOffset = { x: dx, y: dy };
    }
    return;
  }

  if (state.activeTool === 'player') {
    state.currentField.players.push({
      id: `player-${Date.now()}`,
      label: String(state.currentField.players.length + 1),
      team: 'home',
      x,
      y,
    });
    renderPitch();
    return;
  }

  if (state.activeTool === 'ball') {
    state.currentField.ball = { x, y };
    renderPitch();
    return;
  }

  if (state.activeTool === 'cone') {
    state.currentField.markers.push({ x, y });
    renderPitch();
    return;
  }

  if (state.activeTool === 'line') {
    const last = state.currentField.lines[state.currentField.lines.length - 1];
    if (last && !last.closed) {
      last.x2 = x;
      last.y2 = y;
      last.closed = true;
    } else {
      state.currentField.lines.push({ x1: x, y1: y, x2: x, y2: y, closed: false, color: '#ffffff' });
    }
    renderPitch();
    return;
  }

  if (state.activeTool === 'remove') {
    const targetId = playerTarget?.getAttribute('data-player-id');
    if (targetId) {
      state.currentField.players = state.currentField.players.filter((player) => player.id !== targetId);
    }
    renderPitch();
  }
}

window.addEventListener('pointermove', (event) => {
  if (!state.dragPlayerId) return;
  const svgRect = pitchSvg.getBoundingClientRect();
  const x = (event.clientX - svgRect.left) / svgRect.width;
  const y = (event.clientY - svgRect.top) / svgRect.height;
  const player = state.currentField.players.find((p) => p.id === state.dragPlayerId);
  if (!player) return;
  player.x = Math.min(0.95, Math.max(0.05, x - state.dragOffset.x));
  player.y = Math.min(0.92, Math.max(0.08, y - state.dragOffset.y));
  renderPitch();
});

window.addEventListener('pointerup', () => {
  state.dragPlayerId = null;
});

window.addEventListener('keydown', (event) => {
  if (event.key === 'Delete' || event.key === 'Backspace') {
    state.currentField.players = [];
    renderPitch();
  }
});

document.getElementById('createProjectBtn').addEventListener('click', createProject);
document.getElementById('applyFormationBtn').addEventListener('click', applyFormation);
document.getElementById('saveSchemeBtn').addEventListener('click', saveCurrentScheme);
document.getElementById('saveScenarioBtn').addEventListener('click', saveScenario);
document.getElementById('clearBtn').addEventListener('click', () => {
  state.currentField = { players: [], ball: null, markers: [], arrows: [], lines: [] };
  renderPitch();
});

document.getElementById('undoBtn').addEventListener('click', () => {
  if (state.currentField.players.length) {
    state.currentField.players.pop();
    renderPitch();
  }
});

document.getElementById('redoBtn').addEventListener('click', () => {
  setStatus('Redo is available in an extended edition', 'warn');
});

document.querySelectorAll('.tool-btn').forEach((button) => {
  button.addEventListener('click', () => {
    state.activeTool = button.dataset.tool;
    document.querySelectorAll('.tool-btn').forEach((btn) => btn.classList.toggle('active', btn === button));
  });
});

document.getElementById('exportJsonBtn').addEventListener('click', async () => {
  if (!state.selectedProjectId) {
    setStatus('Select a project first', 'warn');
    return;
  }
  const data = await fetchJson(`/api/projects/${state.selectedProjectId}/export`);
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'tacticoach-export.json';
  link.click();
  URL.revokeObjectURL(url);
  setStatus('JSON exported');
});

document.getElementById('importJsonInput').addEventListener('change', async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  try {
    const text = await file.text();
    const payload = JSON.parse(text);
    const project = await fetchJson('/api/projects/import', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    state.projects.unshift(project);
    renderProjectList();
    await selectProject(project.id);
    setStatus('Project imported');
  } catch (error) {
    setStatus(error.message, 'error');
  }
});

document.getElementById('exportPngBtn').addEventListener('click', () => {
  const serializer = new XMLSerializer();
  const svgString = serializer.serializeToString(pitchSvg);
  const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const image = new Image();
  image.onload = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 1000;
    canvas.height = 680;
    const context = canvas.getContext('2d');
    context.fillStyle = '#198b4d';
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.drawImage(image, 0, 0);
    const pngUrl = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.href = pngUrl;
    link.download = 'tacticoach-pitch.png';
    link.click();
    URL.revokeObjectURL(url);
    setStatus('PNG exported');
  };
  image.src = url;
});

buildFormationOptions();
loadProjects();
renderPitch();
