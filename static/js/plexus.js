(function() {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) {
        console.error("Hero canvas not found");
        return;
    }
    const ctx = canvas.getContext('2d');
    let W = canvas.offsetWidth;
    let H = canvas.offsetHeight;
    canvas.width = W;
    canvas.height = H;
    const maxParticles = 50;
    const particleColor = "rgba(255, 255, 255, 0.5)"; 
    const lineColor = "rgba(255, 255, 255, 0.1)"; 
    const maxLineDist = 120; 
    let particles = [];
    function Particle() {
        this.x = Math.random() * W;
        this.y = Math.random() * H;
        this.vx = (Math.random() - 0.5) * 0.5; 
        this.vy = (Math.random() - 0.5) * 0.5;
        this.radius = 2 + Math.random() * 2;
    }
    for (let i = 0; i < maxParticles; i++) {
        particles.push(new Particle());
    }
    function draw() {
        ctx.clearRect(0, 0, W, H);
        for (let i = 0; i < particles.length; i++) {
            let p1 = particles[i];
            p1.x += p1.vx;
            p1.y += p1.vy;
            if (p1.x < 0) p1.x = W;
            if (p1.x > W) p1.x = 0;
            if (p1.y < 0) p1.y = H;
            if (p1.y > H) p1.y = 0;
            ctx.beginPath();
            ctx.fillStyle = particleColor;
            ctx.arc(p1.x, p1.y, p1.radius, 0, Math.PI * 2);
            ctx.fill();
            for (let j = i + 1; j < particles.length; j++) {
                let p2 = particles[j];
                let dist = Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
                if (dist < maxLineDist) {
                    ctx.beginPath();
                    ctx.strokeStyle = lineColor;
                    ctx.globalAlpha = 1 - (dist / maxLineDist); 
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                }
            }
        }
        ctx.globalAlpha = 1; 
        requestAnimationFrame(draw);
    }
    window.addEventListener('resize', function() {
        W = canvas.offsetWidth;
        H = canvas.offsetHeight;
        canvas.width = W;
        canvas.height = H;
    });
    draw();
})();