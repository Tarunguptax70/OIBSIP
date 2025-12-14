document.addEventListener('DOMContentLoaded', () => {
    const scene = document.querySelector('.default-animation--scene');
    if (!scene) return;

    // --- Configuration from React component props ---
    const gridSize = 20;
    const maxAngle = 45;
    const radius = 3;
    const easing = 'power3.out';
    const duration = { enter: 0.3, leave: 0.6 };
    const faceColor = '#060010';
    const autoAnimate = true;
    const rippleOnClick = false;
    const rippleColor = '#fff';
    const rippleSpeed = 2;
    // --- End Configuration ---

    let userActive = false;
    let idleTimer = null;
    let raf = null;
    let simRAF = null;
    const simPos = { x: Math.random() * gridSize, y: Math.random() * gridSize };
    const simTarget = { x: Math.random() * gridSize, y: Math.random() * gridSize };

    // 1. Generate the grid
    function generateGrid() {
        scene.innerHTML = ''; // Clear existing content
        for (let r = 0; r < gridSize; r++) {
            for (let c = 0; c < gridSize; c++) {
                const cube = document.createElement('div');
                cube.classList.add('cube');
                cube.dataset.row = r;
                cube.dataset.col = c;
                cube.innerHTML = `
                    <div class="cube-face cube-face--top"></div>
                    <div class="cube-face cube-face--bottom"></div>
                    <div class="cube-face cube-face--left"></div>
                    <div class="cube-face cube-face--right"></div>
                    <div class="cube-face cube-face--front"></div>
                    <div class="cube-face cube-face--back"></div>
                `;
                scene.appendChild(cube);
            }
        }
    }

    // 2. Tilt animation logic
    const tiltAt = (rowCenter, colCenter) => {
        scene.querySelectorAll('.cube').forEach(cube => {
            const r = +cube.dataset.row;
            const c = +cube.dataset.col;
            const dist = Math.hypot(r - rowCenter, c - colCenter);

            if (dist <= radius) {
                const pct = 1 - dist / radius;
                const angle = pct * maxAngle;
                gsap.to(cube, {
                    duration: duration.enter,
                    ease: easing,
                    overwrite: true,
                    rotateX: -angle,
                    rotateY: angle
                });
            } else {
                gsap.to(cube, {
                    duration: duration.leave,
                    ease: 'power3.out',
                    overwrite: true,
                    rotateX: 0,
                    rotateY: 0
                });
            }
        });
    };

    // 3. Reset logic
    const resetAll = () => {
        scene.querySelectorAll('.cube').forEach(cube =>
            gsap.to(cube, {
                duration: duration.leave,
                rotateX: 0,
                rotateY: 0,
                ease: 'power3.out'
            })
        );
    };
    
    // 4. Pointer move handler
    const onPointerMove = (e) => {
        userActive = true;
        if (idleTimer) clearTimeout(idleTimer);

        const rect = scene.getBoundingClientRect();
        const cellW = rect.width / gridSize;
        const cellH = rect.height / gridSize;
        const colCenter = (e.clientX - rect.left) / cellW;
        const rowCenter = (e.clientY - rect.top) / cellH;

        if (raf) cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => tiltAt(rowCenter, colCenter));

        idleTimer = setTimeout(() => {
            userActive = false;
        }, 3000);
    };

    // 5. Click ripple handler
    const onClick = (e) => {
        if (!rippleOnClick) return;
        const rect = scene.getBoundingClientRect();
        const cellW = rect.width / gridSize;
        const cellH = rect.height / gridSize;

        const clientX = e.clientX || (e.touches && e.touches[0].clientX);
        const clientY = e.clientY || (e.touches && e.touches[0].clientY);

        const colHit = Math.floor((clientX - rect.left) / cellW);
        const rowHit = Math.floor((clientY - rect.top) / cellH);

        const baseRingDelay = 0.15;
        const baseAnimDur = 0.3;
        const baseHold = 0.6;

        const spreadDelay = baseRingDelay / rippleSpeed;
        const animDuration = baseAnimDur / rippleSpeed;
        const holdTime = baseHold / rippleSpeed;

        const rings = {};
        scene.querySelectorAll('.cube').forEach(cube => {
            const r = +cube.dataset.row;
            const c = +cube.dataset.col;
            const dist = Math.hypot(r - rowHit, c - colHit);
            const ring = Math.round(dist);
            if (!rings[ring]) rings[ring] = [];
            rings[ring].push(cube);
        });

        Object.keys(rings)
            .map(Number)
            .sort((a, b) => a - b)
            .forEach(ring => {
                const delay = ring * spreadDelay;
                const faces = rings[ring].flatMap(cube => Array.from(cube.querySelectorAll('.cube-face')));

                gsap.to(faces, {
                    backgroundColor: rippleColor,
                    duration: animDuration,
                    delay,
                    ease: 'power3.out'
                });
                gsap.to(faces, {
                    backgroundColor: faceColor,
                    duration: animDuration,
                    delay: delay + animDuration + holdTime,
                    ease: 'power3.out'
                });
            });
    };
    
    // 6. Auto-animation (idle) loop
    const autoAnimateLoop = () => {
        if (!userActive) {
            const pos = simPos;
            const tgt = simTarget;
            const speed = 0.02;

            pos.x += (tgt.x - pos.x) * speed;
            pos.y += (tgt.y - pos.y) * speed;
            tiltAt(pos.y, pos.x);
            
            if (Math.hypot(pos.x - tgt.x, pos.y - tgt.y) < 0.1) {
                simTarget.x = Math.random() * gridSize;
                simTarget.y = Math.random() * gridSize;
            }
        }
        simRAF = requestAnimationFrame(autoAnimateLoop);
    };

    // 7. Initialize
    generateGrid();
    scene.addEventListener('pointermove', onPointerMove);
    scene.addEventListener('pointerleave', resetAll);
    scene.addEventListener('click', onClick);

    if (autoAnimate) {
        simRAF = requestAnimationFrame(autoAnimateLoop);
    }
});
