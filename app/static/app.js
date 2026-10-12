* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Inter, Arial, sans-serif;
  background: #091522;
  color: #edf4ff;
}
button, input, select {
  font: inherit;
}
.app-shell {
  display: grid;
  grid-template-columns: 320px 1fr;
  min-height: 100vh;
}
.sidebar {
  background: linear-gradient(180deg, #0f1d2d 0%, #0a1220 100%);
  border-right: 1px solid rgba(255,255,255,0.08);
  padding: 16px;
}
.brand-block {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.brand-block h1 {
  margin: 0 0 4px;
  font-size: 2rem;
}
.brand-block p {
  margin: 0;
  color: #8fb0d5;
}
.panel {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 12px;
}
.panel h2 {
  margin: 0 0 10px;
  font-size: 1rem;
}
.toolbar-row, .topbar-actions, .tool-panel {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
input, select, button {
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(13,20,31,0.96);
  color: #edf4ff;
  border-radius: 8px;
  padding: 10px 12px;
}
button {
  cursor: pointer;
  transition: 0.15s ease;
}
button:hover {
  filter: brightness(1.1);
}
button.danger {
  background: #5c1d2b;
}
.list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.list li {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  padding: 8px 10px;
  cursor: pointer;
}
.list li.active {
  border-color: #76adff;
  background: rgba(77,140,255,0.14);
}
.workspace {
  padding: 16px;
}
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.topbar h2 { margin: 0; }
.status-badge {
  display: inline-block;
  margin-left: 8px;
  background: rgba(38, 208, 125, 0.18);
  color: #82f0b8;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 0.8rem;
}
.tool-panel {
  margin-bottom: 14px;
}
.tool-btn.active {
  background: #1755b8;
  border-color: #7bb0ff;
}
.pitch-shell {
  background: linear-gradient(180deg, #1ba25e, #0d7d47);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 36px rgba(0,0,0,0.22);
}
#pitchSvg {
  display: block;
  width: 100%;
  min-height: 620px;
  background: rgba(19,94,51,0.8);
}
.file-upload {
  position: relative;
  display: block;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  background: rgba(255,255,255,0.02);
  padding: 10px 12px;
  text-align: center;
  cursor: pointer;
}
.file-upload input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}
.small-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
@media (max-width: 980px) {
  .app-shell {
    grid-template-columns: 1fr;
  }
  .sidebar {
    border-right: none;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
}
