let video;
let canvas;
let context;
let counter = 0;
let isVideoPlaying = false;

function startVideo() {
  if (!isVideoPlaying) {
    video = document.createElement('video');
    video.setAttribute('autoplay', '');
    video.setAttribute('playsinline', '');
    video.style.display = 'none';
    document.body.appendChild(video);
    
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
        video.play();
        isVideoPlaying = true;
        canvas = document.getElementById('videoCanvas');
        context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        detectVehicles();
      })
      .catch(err => console.error('Error accessing camera:', err));
  }
}

function stopVideo() {
  if (isVideoPlaying) {
    video.pause();
    isVideoPlaying = false;
    video.srcObject.getTracks().forEach(track => track.stop());
    document.body.removeChild(video);
  }
}

function detectVehicles() {
  if (isVideoPlaying) {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    // Send frame to server for processing (Flask + OpenCV)
    // Example AJAX request to Flask server
    let imageData = canvas.toDataURL('image/jpeg');
    fetch('/process_frame', {
      method: 'POST',
      body: JSON.stringify({ image_data: imageData }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      counter = data.vehicle_count;
      document.getElementById('counter').innerText = counter;
      detectVehicles(); // Recursive call for continuous processing
    })
    .catch(error => console.error('Error processing frame:', error));
  }
}
