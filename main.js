// main.js

const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const CHART_SIZE = 300;

const evolution = new Evolution(50, 4, 6, 1);
let dinos = [];
let obstacles = [];
let bestScores = [];
let frameCount = 0;


function resetGame() {
  dinos = evolution.population.map(genome => new Dino(genome));
  obstacles = [];
}

function updateGame() {
  if (obstacles.length === 0 || obstacles[obstacles.length - 1].x < 400) {
    obstacles.push(new Obstacle());
  }

  obstacles.forEach(o => o.update());
  obstacles = obstacles.filter(o => !o.offscreen());

  dinos.forEach(d => {
    if (!d.alive) return;
    d.think(obstacles);
    d.update();

    // Colisão
    for (let obs of obstacles) {
      if (obs.x < d.x + 40 &&
          obs.x + obs.width > d.x &&
          d.y + 40 > obs.y) {
        d.alive = false;
        d.genome.fitness = d.score;
      }
    }
  });

  const aliveCount = dinos.filter(d => d.alive).length;

  if (aliveCount === 0) {
    evolution.evolve();
    const best = evolution.population[0].fitness;
    console.log(`Geração ${evolution.generation} - Melhor pontuação: ${best}`);
    bestScores.push(best);
    updateChart();
    resetGame();
  }
}

function drawGame() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  obstacles.forEach(o => o.draw(ctx));
  dinos.forEach(d => {
    if (d.alive) d.draw(ctx);
  });
}

function loop() {
    frameCount++;
    updateGame();
    drawGame();
    requestAnimationFrame(loop);
  }
  

function updateChart() {
  const chart = document.getElementById('score-chart').getContext('2d');
  chart.clearRect(0, 0, CHART_SIZE, CHART_SIZE);

  chart.beginPath();
  chart.strokeStyle = 'blue';

  bestScores.forEach((score, i) => {
    const x = (i / bestScores.length) * CHART_SIZE;
    const y = CHART_SIZE - (score / Math.max(...bestScores)) * CHART_SIZE;
    chart.lineTo(x, y);
  });

  chart.stroke();
}

resetGame();
loop();
