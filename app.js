const $ = id => document.getElementById(id);
let lastScan = "";
function setMetric(id, bar, value, max) {
  $(id).innerHTML = value == null ? '--' : Number(value).toFixed(1) + '<small>' + (id==='temp'?'°C':id==='humidity'||id==='soil'?'%':'V') + '</small>';
  $(bar).style.width = value == null ? '0%' : Math.max(0,Math.min(100,Number(value)/max*100))+'%';
}
function setIR(id, value, labelId) {
  const active = value === 1 || value === true;
  $(id).classList.toggle('active', active);
  $(labelId).textContent = value == null ? '--' : (active ? 'ACTIVE' : 'INACTIVE');
}
async function refresh() {
  try {
    const res = await fetch('/api/status', {cache:'no-store'});
    const d = await res.json();
    $('connection').textContent = 'SERVER ONLINE';
    $('connection').previousElementSibling.style.background = 'var(--green)';
    $('clock').textContent = new Date().toLocaleTimeString();
    if (d.telemetry) {
      const t=d.telemetry;
      setMetric('temp','tempbar',t.temperature,50);
      setMetric('humidity','hbar',t.humidity,100);
      setMetric('soil','soilbar',t.soil_moisture,100);
      setMetric('battery','batterybar',t.battery,12);
      $('soilstate').textContent = t.soil_moisture == null ? 'No soil reading' : (t.soil_moisture < 35 ? 'LOW · Soil is dry' : t.soil_moisture < 65 ? 'MODERATE · Monitor' : 'GOOD · Moisture adequate');
      if (t.latitude != null && t.longitude != null && (t.latitude !== 0 || t.longitude !== 0)) {
        $('lat').textContent=Number(t.latitude).toFixed(6); $('lon').textContent=Number(t.longitude).toFixed(6);
        $('gpsstatus').textContent='GPS FIX'; $('gpsstatus').style.color='var(--green)';
        $('maplink').href=`https://www.google.com/maps?q=${t.latitude},${t.longitude}`;
      } else {$('gpsstatus').textContent='NO FIX';}
      $('sats').textContent='Satellites: '+(t.satellites ?? '--');
      setIR('irL',t.ir_left,'irlv'); setIR('irC',t.ir_center,'ircv'); setIR('irR',t.ir_right,'irrv');
      $('obstacle').textContent = t.obstacle == null ? '--' : (t.obstacle ? 'DETECTED' : 'CLEAR');
      $('obstacle').style.color = t.obstacle ? 'var(--orange)' : 'var(--green)';
    }
    if (d.scan && d.scan.timestamp !== lastScan) {
      lastScan=d.scan.timestamp;
      const img=$('leafimg'); img.src='/images/'+encodeURIComponent(d.scan.image_name)+'?v='+Date.now(); img.style.display='block'; $('photoempty').style.display='none';
      $('result').textContent=d.scan.result;
      $('confidence').textContent='Confidence: '+(d.scan.confidence == null ? 'Not available' : d.scan.confidence+'%');
      $('ainote').textContent=d.scan.note || 'Automatic scan completed.';
      $('scantime').textContent='Captured & analysed · '+new Date(d.scan.timestamp).toLocaleString();
      document.querySelector('.statusdot').style.background = d.scan.result==='Healthy' ? 'var(--green)' : 'var(--orange)';
    }
    $('modelstate').textContent=d.ai_ready?'AI MODEL: FILE DETECTED':'AI MODEL: NOT CONFIGURED';
    $('modelstate').style.color=d.ai_ready?'var(--green)':'var(--orange)';
  } catch(e) {
    $('connection').textContent='SERVER OFFLINE';
    $('connection').previousElementSibling.style.background='var(--orange)';
  }
}
refresh(); setInterval(refresh,2000);
