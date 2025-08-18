// 初始化地图
const map = L.map('map').setView([40.69149268636249, 100.39499837692665], 8);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 聊天相关
const chatLog = document.getElementById('chat-log');
const inputBox = document.getElementById('input-box');

async function sendMessage() {
    const msg = inputBox.value.trim();
    if (!msg) return;
    appendMessage('user', msg);
    inputBox.value = '';
    try {
        const res = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();
        appendMessage('bot', data.reply);
    } catch (err) {
        appendMessage('bot', '后端服务请求失败');
    }
}

function appendMessage(sender, text) {
    const div = document.createElement('div');
    div.className = sender;
    div.innerHTML = text;
    chatLog.appendChild(div);
    chatLog.scrollTop = chatLog.scrollHeight;
}

// 地图点击事件，捕捉坐标
map.on('click', function(e) {
    const { lat, lng } = e.latlng;
    const coordText = `<span class="coord-cursor">捕捉到坐标: ${lng.toFixed(8)}, ${lat.toFixed(8)}</span>`;
    appendMessage('system', coordText);
    inputBox.value = `请判断坐标${lng}, ${lat}是不是戈壁？`;
});
