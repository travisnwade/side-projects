document.addEventListener('DOMContentLoaded', function() {
    const bgMusic = document.getElementById('bgMusic');
    const volumeSlider = document.getElementById('volumeSlider');

    function updateVolume() {
        bgMusic.volume = volumeSlider.value;
        volumeSlider.style.setProperty('--volume', volumeSlider.value);
    }

    volumeSlider.addEventListener('input', updateVolume);

    // Set initial volume
    bgMusic.volume = volumeSlider.value = 0.25;
    updateVolume();
});
