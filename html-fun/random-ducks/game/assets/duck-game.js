const cursorDuck = document.getElementById('cursorDuck');
const miniDucks = [
    document.getElementById('miniDuck1'),
    document.getElementById('miniDuck2'),
    document.getElementById('miniDuck3'),
    document.getElementById('miniDuck4'),
    document.getElementById('miniDuck5')
];
const counter = document.getElementById('counter');
const popSound = document.getElementById('popSound');
const bgMusic = document.getElementById('bgMusic');
const bird = document.getElementById('bird');
const birdSound = document.getElementById('birdSound');
let eggCount = 0;
let mouseTimeout;
let wanderingInterval;

bgMusic.play();
birdSound.volume = 0.5; // Set bird sound to 50%

document.addEventListener('mousemove', (e) => {
    cursorDuck.style.left = `${e.pageX}px`;
    cursorDuck.style.top = `${e.pageY}px`;

    miniDucks.forEach((duck, index) => {
        setTimeout(() => {
            duck.style.left = `${e.pageX + (index + 1) * 60}px`;
            duck.style.top = `${e.pageY + (index + 1) * 60}px`;
        }, index * 100);
    });

    clearTimeout(mouseTimeout);
    clearInterval(wanderingInterval);
    mouseTimeout = setTimeout(startWandering, 3000);
});

function startWandering() {
    wanderingInterval = setInterval(() => {
        miniDucks.forEach((duck) => {
            const randomX = Math.random() * 100 - 50; // Random movement within 50px
            const randomY = Math.random() * 100 - 50;
            const currentX = parseFloat(duck.style.left);
            const currentY = parseFloat(duck.style.top);
            duck.style.left = `${currentX + randomX}px`;
            duck.style.top = `${currentY + randomY}px`;
        });
    }, 3000);
}

function placeEgg() {
    const egg = document.createElement('div');
    egg.classList.add('egg');
    document.body.appendChild(egg);

    const randomX = Math.random() * window.innerWidth;
    const randomY = Math.random() * window.innerHeight;

    egg.style.left = `${randomX}px`;
    egg.style.top = `${randomY}px`;

    egg.addEventListener('mouseenter', () => {
        egg.remove();
        eggCount++;
        counter.textContent = `Eggs: ${eggCount}`;
        popSound.currentTime = 0; // Rewind to the start
        popSound.play();
    });

    setTimeout(placeEgg, Math.random() * 12000 + 3000);
}

setTimeout(placeEgg, Math.random() * 12000 + 3000);
startWandering();

function moveBird() {
    const startPosition = Math.random() * window.innerHeight / 2;
    const direction = Math.random() > 0.5 ? 'leftToRight' : 'rightToLeft';

    bird.style.top = `${startPosition}px`;
    bird.style.display = 'block';

    const duration = Math.random() * 5000 + 5000; // Random duration between 5 and 10 seconds

    if (direction === 'leftToRight') {
        bird.style.left = '-100px';
        bird.style.transform = 'scaleX(1)'; // Ensure bird faces right

        bird.animate([
            { left: '-100px' },
            { left: `${window.innerWidth + 100}px` }
        ], {
            duration: duration,
            easing: 'linear',
            iterations: 1
        });

        setTimeout(() => birdSound.play(), 250);
        setTimeout(() => {
            bird.style.display = 'none';
            setTimeout(moveBird, Math.random() * 5000 + 15000); // Schedule next flight
        }, duration);
    } else {
        bird.style.left = `${window.innerWidth + 100}px`;
        bird.style.transform = 'scaleX(-1)'; // Ensure bird faces left

        bird.animate([
            { left: `${window.innerWidth + 100}px` },
            { left: '-100px' }
        ], {
            duration: duration,
            easing: 'linear',
            iterations: 1
        });

        setTimeout(() => birdSound.play(), 250);
        setTimeout(() => {
            bird.style.display = 'none';
            setTimeout(moveBird, Math.random() * 5000 + 15000); // Schedule next flight
        }, duration);
    }
}

setTimeout(moveBird, Math.random() * 5000 + 15000);
