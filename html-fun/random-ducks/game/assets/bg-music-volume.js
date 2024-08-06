document.addEventListener('DOMContentLoaded', function() {
    const bgMusic = document.getElementById('bgMusic');
    const volumeSlider = document.getElementById('volumeSlider');

    volumeSlider.addEventListener('input', function() {
        bgMusic.volume = volumeSlider.value;
    });

    // Set initial volume
    bgMusic.volume = volumeSlider.value = 0.25;
});
