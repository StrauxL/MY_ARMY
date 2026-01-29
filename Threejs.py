%%javascript
// 1. Setup the Canvas Environment
// We use a dark background to make the colors pop
element.html(`
  <div id="canvas-container" style="width: 100%; height: 400px; background: #0f0f1f; position: relative; overflow: hidden; border-radius: 8px;">
    <canvas id="particleCanvas" style="display: block;"></canvas>
    <div style="position: absolute; bottom: 10px; right: 10px; color: rgba(255,255,255,0.5); font-family: sans-serif; font-size: 12px; pointer-events: none;">
      Interactive Particle Network
    </div>
  </div>
`);

// 2. Initialize Canvas
const canvas = element.find("#particleCanvas")[0];
const ctx = canvas.getContext('2d');
const container = element.find("#canvas-container");

// Set canvas size to match container
let w = canvas.width = container.width();
let h = canvas.height = container.height();

// 3. Particle Configuration
const particleCount = 80;
const connectionDistance = 100;
const mouseDistance = 150;
const particles = [];

// Mouse interaction object
const mouse = { x: null, y: null };

// Track mouse movement inside the specific element
element.on('mousemove', function(e) {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
});

element.on('mouseleave', function() {
    mouse.x = null;
    mouse.y = null;
});

// 4. Particle Class
class Particle {
    constructor() {
        this.x = Math.random() * w;
        this.y = Math.random() * h;
        this.vx = (Math.random() - 0.5) * 1.5; // Random horizontal velocity
        this.vy = (Math.random() - 0.5) * 1.5; // Random vertical velocity
        this.size = Math.random() * 2 + 1;
        // Random HSL Color (Pastel/Neon vibes)
        this.color = `hsl(${Math.random() * 360}, 70%, 60%)`;
    }

    update() {
        // Move
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off walls
        if (this.x < 0 || this.x > w) this.vx *= -1;
        if (this.y < 0 || this.y > h) this.vy *= -1;

        // Mouse Interaction: Flee from mouse
        if (mouse.x != null) {
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < mouseDistance) {
                const forceDirectionX = dx / distance;
                const forceDirectionY = dy / distance;
                const force = (mouseDistance - distance) / mouseDistance;
                // Push particle away
                this.vx -= forceDirectionX * force * 0.5;
                this.vy -= forceDirectionY * force * 0.5;
            }
        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

// Create initial particles
for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

// 5. The Animation Loop
function animate() {
    // Check if canvas is still in DOM (stops loop if cell is deleted/re-run)
    if (!document.body.contains(canvas)) return;

    // Clear screen (with slight fade effect for trails? No, lets keep it clean)
    ctx.clearRect(0, 0, w, h);

    // Update and Draw Particles
    for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();

        // Draw connections (The "Network" effect)
        for (let j = i; j < particles.length; j++) {
            let dx = particles[i].x - particles[j].x;
            let dy = particles[i].y - particles[j].y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < connectionDistance) {
                ctx.beginPath();
                // Line opacity based on distance (closer = brighter)
                let opacity = 1 - (distance / connectionDistance);
                ctx.strokeStyle = `rgba(255, 255, 255, ${opacity * 0.2})`;
                ctx.lineWidth = 1;
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();
            }
        }
    }
    
    requestAnimationFrame(animate);
}

// Handle window resize (optional robustness)
window.addEventListener('resize', function() {
    if (document.body.contains(canvas)) {
        w = canvas.width = container.width();
        h = canvas.height = container.height();
    }
});

animate();