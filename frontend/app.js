/**
 * VayuRakshak AI - Interactive Frontend Controller
 * Author: Bhomesh Razdan (Lead Architect)
 */

let map;
let stationLayerGroup;
let fireLayerGroup;
let routeLayerGroup;

// Initialize Lucide icons
lucide.createIcons();

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  loadStations();
  loadStubbleFires();
  setupEventListeners();
  calculateSelectedRoute();
});

function initMap() {
  // Center on DTU Delhi
  const dtuCoords = [28.7499, 77.1170];
  map = L.map('map', {
    zoomControl: true,
    attributionControl: false
  }).setView([28.70, 77.10], 10);

  // Dark Tile Layer (CartoDB Dark Matter)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 19,
    subdomains: 'abcd'
  }).addTo(map);

  stationLayerGroup = L.layerGroup().addTo(map);
  fireLayerGroup = L.layerGroup().addTo(map);
  routeLayerGroup = L.layerGroup().addTo(map);

  // Add DTU Venue Marker
  const dtuIcon = L.divIcon({
    className: 'custom-dtu-pin',
    html: `<div style="background: #06b6d4; color: #000; font-weight: bold; font-size: 11px; padding: 4px 8px; border-radius: 4px; border: 2px solid #fff; box-shadow: 0 0 10px #06b6d4; white-space: nowrap;">📍 DTU Build Venue</div>`,
    iconSize: [120, 30],
    iconAnchor: [60, 15]
  });
  L.marker(dtuCoords, { icon: dtuIcon }).addTo(map)
    .bindPopup('<b>Delhi Technological University (DTU)</b><br>Bharat Builds Tour Venue<br>Shahbad Daulatpur, Bawana Rd');
}

async function loadStations() {
  try {
    const res = await fetch('/api/stations');
    const data = await res.json();
    renderStationMarkers(data.stations);
  } catch (err) {
    // Fallback seed data if running purely offline
    const seed = [
      { name: "DTU Bawana", latitude: 28.7499, longitude: 77.1170, aqi: 388, category: "Severe", pm25: 245 },
      { name: "Jahangirpuri", latitude: 28.7328, longitude: 77.1706, aqi: 440, category: "Severe", pm25: 295 },
      { name: "Rohini Sec 16", latitude: 28.7325, longitude: 77.1199, aqi: 350, category: "Very Poor", pm25: 210 },
      { name: "Anand Vihar", latitude: 28.6469, longitude: 77.3160, aqi: 465, category: "Severe", pm25: 360 },
      { name: "Punjabi Bagh", latitude: 28.6683, longitude: 77.1167, aqi: 315, category: "Very Poor", pm25: 195 },
      { name: "Connaught Place", latitude: 28.6315, longitude: 77.2167, aqi: 280, category: "Poor", pm25: 145 },
      { name: "Dwarka Sec 8", latitude: 28.5710, longitude: 77.0710, aqi: 290, category: "Poor", pm25: 175 },
    ];
    renderStationMarkers(seed);
  }
}

function renderStationMarkers(stations) {
  stationLayerGroup.clearLayers();
  stations.forEach(s => {
    let color = '#ef4444'; // severe
    if (s.aqi <= 100) color = '#10b981';
    else if (s.aqi <= 200) color = '#eab308';
    else if (s.aqi <= 300) color = '#f97316';

    const circle = L.circleMarker([s.latitude, s.longitude], {
      radius: 9,
      fillColor: color,
      color: '#ffffff',
      weight: 1.5,
      opacity: 1,
      fillOpacity: 0.85
    });

    circle.bindPopup(`
      <div style="font-family: sans-serif; font-size: 12px; color: #111;">
        <strong>${s.name}</strong><br>
        AQI: <b style="color: ${color}">${s.aqi}</b> (${s.category})<br>
        PM2.5: ${s.pm25} µg/m³
      </div>
    `);
    stationLayerGroup.addLayer(circle);
  });
}

async function loadStubbleFires() {
  try {
    const res = await fetch('/api/stubble/fires');
    const data = await res.json();
    renderFireMarkers(data.incidents);
    if (data.regional_threat) {
      document.getElementById('kpi-sbii-score').innerText = `${data.regional_threat.stubble_impact_index_sbii} / 100`;
    }
  } catch (err) {
    const seedFires = [
      { fire_id: "FIRE-PB-081", latitude: 30.2450, longitude: 75.8420, district: "Sangrur", state: "Punjab", frp_mw: 48.2 },
      { fire_id: "FIRE-PB-082", latitude: 30.9010, longitude: 75.8573, district: "Ludhiana", state: "Punjab", frp_mw: 39.5 },
      { fire_id: "FIRE-HR-091", latitude: 29.6857, longitude: 76.9905, district: "Karnal", state: "Haryana", frp_mw: 42.6 },
    ];
    renderFireMarkers(seedFires);
  }
}

function renderFireMarkers(incidents) {
  fireLayerGroup.clearLayers();
  incidents.forEach(f => {
    const icon = L.divIcon({
      className: 'fire-icon',
      html: `<div style="font-size: 16px; text-shadow: 0 0 6px #f97316;">🔥</div>`,
      iconSize: [20, 20]
    });
    const marker = L.marker([f.latitude, f.longitude], { icon: icon });
    marker.bindPopup(`
      <div style="font-family: sans-serif; font-size: 12px; color: #111;">
        <strong>Satellite Fire: ${f.fire_id}</strong><br>
        Location: ${f.district}, ${f.state}<br>
        Radiative Power: <b>${f.frp_mw} MW</b>
      </div>
    `);
    fireLayerGroup.addLayer(marker);
  });
}

function setupEventListeners() {
  document.getElementById('btn-toggle-fires').addEventListener('click', () => {
    if (map.hasLayer(fireLayerGroup)) map.removeLayer(fireLayerGroup);
    else map.addLayer(fireLayerGroup);
  });

  document.getElementById('btn-toggle-stations').addEventListener('click', () => {
    if (map.hasLayer(stationLayerGroup)) map.removeLayer(stationLayerGroup);
    else map.addLayer(stationLayerGroup);
  });

  document.getElementById('btn-center-dtu').addEventListener('click', () => {
    map.setView([28.7499, 77.1170], 12);
  });

  document.getElementById('btn-calculate-route').addEventListener('click', () => {
    calculateSelectedRoute();
  });

  document.getElementById('btn-generate-advisory').addEventListener('click', () => {
    fetchAdvisory();
  });

  document.getElementById('btn-evaluate-cedar').addEventListener('click', () => {
    evaluateCedar();
  });
}

async function calculateSelectedRoute() {
  const preset = document.getElementById('route-preset').value;
  const mode = document.getElementById('commute-mode').value;

  let startLat = 28.7499, startLon = 77.1170, endLat = 28.6139, endLon = 77.2090;
  if (preset === 'rohini_noida') {
    startLat = 28.7325; startLon = 77.1199;
    endLat = 28.6270; endLon = 77.3620;
  } else if (preset === 'dwarka_anand') {
    startLat = 28.5710; startLon = 77.0710;
    endLat = 28.6469; endLon = 77.3160;
  }

  try {
    const res = await fetch(`/api/route/clean?start_lat=${startLat}&start_lon=${startLon}&end_lat=${endLat}&end_lon=${endLon}&mode=${mode}`);
    const data = await res.json();
    renderRoute(data);
  } catch (err) {
    console.error("Using route fallback calculation", err);
  }
}

function renderRoute(routeData) {
  routeLayerGroup.clearLayers();

  const directPts = routeData.direct_route.waypoints.map(w => [w.latitude, w.longitude]);
  const cleanPts = routeData.clean_air_corridor.waypoints.map(w => [w.latitude, w.longitude]);

  // Direct Route (Red dashed)
  const directLine = L.polyline(directPts, {
    color: '#ef4444',
    weight: 4,
    dashArray: '6, 8',
    opacity: 0.8
  }).bindPopup(`<b>Direct Route</b>: High pollution arterial path.<br>Avg AQI: ${routeData.direct_route.average_aqi}`);

  // Clean Corridor Route (Emerald/Cyan glowing solid)
  const cleanLine = L.polyline(cleanPts, {
    color: '#10b981',
    weight: 6,
    opacity: 0.95
  }).bindPopup(`<b>VayuRakshak Clean Air Corridor</b><br>Avg AQI: ${routeData.clean_air_corridor.average_aqi}<br>Dose saved: ${routeData.clean_air_corridor.dose_reduction_pct}%`);

  routeLayerGroup.addLayer(directLine);
  routeLayerGroup.addLayer(cleanLine);

  // Update UI stats
  document.getElementById('res-dose-pct').innerText = `-${routeData.clean_air_corridor.dose_reduction_pct}% PM2.5 Dose`;
  document.getElementById('kpi-dose-saved').innerText = `${routeData.clean_air_corridor.dose_reduction_pct}%`;
  
  document.getElementById('res-direct-dist').innerText = `${routeData.direct_route.distance_km} km (${routeData.direct_route.duration_mins} min)`;
  document.getElementById('res-direct-aqi').innerText = `AQI ${routeData.direct_route.average_aqi}`;
  document.getElementById('res-direct-dose').innerText = `Dose: ${routeData.direct_route.cumulative_pm25_dose_ug} µg`;

  document.getElementById('res-clean-dist').innerText = `${routeData.clean_air_corridor.distance_km} km (${routeData.clean_air_corridor.duration_mins} min)`;
  document.getElementById('res-clean-aqi').innerText = `AQI ${routeData.clean_air_corridor.average_aqi}`;
  document.getElementById('res-clean-dose').innerText = `Dose: ${routeData.clean_air_corridor.cumulative_pm25_dose_ug} µg`;

  document.getElementById('res-ppe').innerText = routeData.clean_air_corridor.recommended_ppe;
}

async function fetchAdvisory() {
  const group = document.getElementById('adv-group').value;
  const loc = encodeURIComponent(document.getElementById('adv-loc').value);

  try {
    const res = await fetch(`/api/advisory?group=${group}&location=${loc}&aqi=395`);
    const data = await res.json();
    
    document.getElementById('adv-engine-tag').innerText = data.ai_engine;
    document.getElementById('adv-school-text').innerText = data.school_safety_guidance;
    
    const list = document.getElementById('adv-actions-list');
    list.innerHTML = '';
    data.recommended_actions.forEach(act => {
      const li = document.createElement('li');
      li.innerText = act;
      list.appendChild(li);
    });
  } catch (err) {
    console.error("Advisory error", err);
  }
}

async function evaluateCedar() {
  const role = document.getElementById('cedar-role').value;
  const action = document.getElementById('cedar-action').value;
  const resource = document.getElementById('cedar-resource').value;

  try {
    const res = await fetch('/api/auth/cedar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role, action, resource })
    });
    const data = await res.json();

    const verdictElem = document.getElementById('cedar-verdict');
    const reasonElem = document.getElementById('cedar-reason');

    verdictElem.innerText = data.decision;
    if (data.decision === 'ALLOW') {
      verdictElem.className = 'font-mono text-emerald-400 font-bold text-sm';
    } else {
      verdictElem.className = 'font-mono text-red-400 font-bold text-sm';
    }
    reasonElem.innerText = data.evaluation_reason;
  } catch (err) {
    console.error("Cedar eval error", err);
  }
}
