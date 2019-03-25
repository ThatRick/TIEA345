const socket = io();

console.log('Client running');
const title = document.getElementById('header');
title.textContent = 'Status: Connecting...';

socket.on('connect', () => title.textContent = 'Status: Online');
socket.on('disconnect', () => title.textContent = 'Status: Offline');

// position slider input
const sliderPos = document.getElementById('slider_pos');

// slider label
const sliderLabel = document.getElementById('label_pos');
sliderLabel.textContent = sliderPos.value;

// Receive new slider value from server
socket.on('position', value => {
    sliderPos.value = value;
    sliderLabel.textContent = value;
});

// Receive new slider value from UI
sliderPos.addEventListener('input', e => {
    const value = e.target.value;
    sliderLabel.textContent = value;
    // send new slider value to server
    socket.emit('position', value);
});


// position throttle input
const sliderThrottle = document.getElementById('slider_throttle');
sliderThrottle.max = 100;
sliderThrottle.step = 1;

// throttle label
const throttleLabel = document.getElementById('label_throttle');
throttleLabel.textContent = sliderThrottle.value;

// Receive new throttle value from server
socket.on('throttle', value => {
    sliderThrottle.value = value;
    throttleLabel.textContent = value;
});

// Receive new throttle value from UI
sliderThrottle.addEventListener('input', e => {
    const value = e.target.value;
    throttleLabel.textContent = value;
    // send new throttle value to server
    socket.emit('throttle', value);
});


// command input field
const commandInput = document.getElementById('input_command');
const form = document.getElementById('form_command');

// text log
const log = document.getElementById('serial_log');
// text log container
const box = document.getElementById('serial_container');

// Submit new command
form.addEventListener('submit', e => {
    e.preventDefault();
    const text = commandInput.value;
    socket.emit('command', text);
    commandInput.value = '';
    addLogLine(`<span class='commandLine'>&gt;${text}</span>`);
});

// Receive new serial data line
socket.on('monitor', line => {
    addLogLine(line);
})

function addLogLine(line) {
    log.insertAdjacentHTML('beforeend', line + '<br/>');
    box.scrollTop = box.scrollHeight;
}
