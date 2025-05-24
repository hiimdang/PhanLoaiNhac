document.addEventListener('DOMContentLoaded', function () {
  // Xử lý các nút phân trang
  const paginationButtons = document.querySelectorAll('.pagination-button');
  paginationButtons.forEach(button => {
    if (!button.querySelector('i')) {
      button.addEventListener('click', function () {
        document.querySelectorAll('.pagination-button').forEach(btn => {
          btn.classList.remove('active');
        });
        this.classList.add('active');
      });
    }
  });

  // Xử lý thanh âm lượng
  document.querySelectorAll('.volume-bar').forEach(volumeBar => {
    volumeBar.addEventListener('click', function (e) {
      const width = this.clientWidth;
      const clickX = e.offsetX;
      const volume = this.querySelector('.volume');
      const handle = this.querySelector('.volume-handle');

      const percentage = (clickX / width) * 100;
      volume.style.width = percentage + '%';

      if (handle) {
        handle.style.left = `calc(${percentage}% - 6px)`;
      }
    });
  });
});

//Progress bar
const progressBar = document.querySelector('.progress-bar');
const progress = document.querySelector('.progress');
const progressHandle = document.querySelector('.progress-handle');
const currentTimeElem = document.querySelector('.progress-container span.time:first-child');
const durationElem = document.querySelector('.progress-container span.time:last-child');

const audioPlayer = document.getElementById('audio-player');  // bạn phải có <audio id="audio-player" hidden></audio>

audioPlayer.addEventListener('timeupdate', () => {
  const currentTime = audioPlayer.currentTime;
  const duration = audioPlayer.duration;

  console.log('currentTime:', currentTime, 'duration:', duration);

  if (!duration) return;

  const percent = (currentTime / duration) * 100;
  console.log('percent:', percent);

  progress.style.width = percent + '%';
  progressHandle.style.left = (progressBar.clientWidth * percent / 100) + 'px';
});
// Click progress bar
progressBar.addEventListener('click', (e) => {
  const rect = progressBar.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const width = rect.width;

  const clickPercent = clickX / width;
  const newTime = clickPercent * audioPlayer.duration;

  audioPlayer.currentTime = newTime;
});
//Drag progress bar
let isDragging = false;

progressHandle.addEventListener('mousedown', () => {
  isDragging = true;
});

document.addEventListener('mouseup', () => {
  if (isDragging) isDragging = false;
});

document.addEventListener('mousemove', (e) => {
  if (!isDragging) return;

  const rect = progressBar.getBoundingClientRect();
  let moveX = e.clientX - rect.left;

  if (moveX < 0) moveX = 0;
  if (moveX > rect.width) moveX = rect.width;

  const movePercent = moveX / rect.width;

  audioPlayer.currentTime = movePercent * audioPlayer.duration;
});

// Hàm format số giây thành mm:ss
function formatTime(seconds) {
  if (isNaN(seconds)) return "00:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m < 10 ? '0' + m : m}:${s < 10 ? '0' + s : s}`;
}

document.addEventListener('DOMContentLoaded', () => {
  function cleanLyrics(lyrics) {
    if (!lyrics) return '';

    lyrics = lyrics.normalize('NFC');

    lyrics = lyrics.replace(/[\r\n]+|\\u000D\\u000A|\\u000D|\\u000A/g, '\n');
    lyrics = lyrics.replace(/\\u0027/g, "'");
    lyrics = lyrics.replace(/\\u0022/g, '"');
    lyrics = lyrics.replace(/\\u002D/g, '-');
    lyrics = lyrics.replace(/\\u002C/g, ',');
    lyrics = lyrics.replace(/\\u002E/g, '.');
    lyrics = lyrics.replace(/\\u0021/g, '!');
    lyrics = lyrics.replace(/\\u003F/g, '?');

    return lyrics;
  }
  const audioPlayer = document.getElementById('audio-player');

  // Lấy tất cả nút play trong danh sách bài hát
  const playButtons = document.querySelectorAll('.song-card .song-play');

  const lyricsBox = document.getElementById('lyrics-box').querySelector('textarea');

  playButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const songCard = btn.closest('.song-card');
      const title = songCard.dataset.title;
      const artist = songCard.dataset.artist;
      const duration = songCard.dataset.duration;
      console.log('Duration từ songCard:', duration);
      const audioUrl = songCard.dataset.audioUrl;

      const playerTitle = document.querySelector('.player-bar .song-title');
      const playerArtist = document.querySelector('.player-bar .song-artist');
      const times = document.querySelectorAll('.player-bar .progress-container .time');
      const playerDuration = times[1];
      const lyrics = cleanLyrics(songCard.dataset.lyrics);


      lyricsBox.value = lyrics;

      const genreDisplay = document.querySelector('.player-bar .genre-display span');

      playerTitle.textContent = title;
      playerArtist.textContent = artist;
      playerDuration.textContent = duration;

      audioPlayer.src = audioUrl;
      audioPlayer.play();

      const playButton = document.querySelector('.player-bar .play-button i');
      playButton.classList.remove('fa-play');
      playButton.classList.add('fa-pause');

      //------------------------
      const genreIcon = genreDisplay.previousElementSibling;
      const confidenceTextEl = document.querySelector('.player-bar .genre-display .confidence-text');
      genreDisplay.textContent = 'Đang dự đoán...';
      confidenceTextEl.textContent = '';
      genreIcon.classList.add('fa-spinner', 'genre-loading');
      genreIcon.classList.remove('fa-music');

      fetch('/predict-genre/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
          audio_path: audioUrl,
          lyrics: lyrics
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.genre) {
            genreDisplay.textContent = `Thể loại: ${data.genre}`;

            confidenceTextEl.textContent = ` (Độ tin cậy: ${(data.confidence * 100).toFixed(1)}%)`;
          } else {
            genreDisplay.textContent = 'Thể loại: Không xác định';
          }
        })
        .catch(() => {
          genreDisplay.textContent = 'Thể loại: Lỗi kết nối';
        })
        .finally(() => {
          genreIcon.classList.remove('fa-spinner', 'genre-loading');
          genreIcon.classList.add('fa-music');
        });
      //------------------------
    });
  });

  // Xử lý nút play/pause ở player-bar
  const playerPlayButton = document.querySelector('.player-bar .play-button');
  playerPlayButton.addEventListener('click', () => {
    if (audioPlayer.paused) {
      audioPlayer.play();
      playerPlayButton.querySelector('i').classList.replace('fa-play', 'fa-pause');
    } else {
      audioPlayer.pause();
      playerPlayButton.querySelector('i').classList.replace('fa-pause', 'fa-play');
    }
  });

  audioPlayer.addEventListener('ended', () => {
    const playerPlayIcon = document.querySelector('.player-bar .play-button i');
    playerPlayIcon.classList.replace('fa-pause', 'fa-play');
  });
});

document.addEventListener('DOMContentLoaded', function () {
  updatePagination();
  showCurrentPageSongs();
});


// Music upload
const musicUploadInput = document.getElementById('music-upload');
const uploadButton = document.querySelector('.upload-button');

musicUploadInput.addEventListener('change', handleMusicUpload);

function handleMusicUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  if (!file.type.startsWith('audio/')) {
    alert('Vui lòng chọn file âm thanh (MP3, WAV, OGG)');
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    alert('File quá lớn! Vui lòng chọn file nhỏ hơn 10MB');
    return;
  }
  const formData = new FormData();
  formData.append('music_file', file);
  fetch('/upload-music/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Tải lên thành công!');
      } else {
        alert('Lỗi: ' + data.error);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Đã xảy ra lỗi khi tải lên');
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}