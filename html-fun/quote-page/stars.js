document.addEventListener('mousemove', function(e) {
    createStar(e.pageX, e.pageY);
});

function createStar(x, y) {
    const star = document.createElement('div');
    star.className = 'star';
    star.style.left = `${x}px`;
    star.style.top = `${y}px`;
    document.body.appendChild(star);

    setTimeout(() => {
        star.remove();
    }, 3000);
}
