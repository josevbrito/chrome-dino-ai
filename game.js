// game.js

// Imagens carregadas

const smallCactusImages = [
  'assets/cactus/SmallCactus1.png',
  'assets/cactus/SmallCactus2.png',
  'assets/cactus/SmallCactus3.png'
].map(src => {
  const img = new Image();
  img.src = src;
  return img;
});

const dinoRun1 = new Image();
dinoRun1.src = './assets/dino/DinoRun1.png';

const dinoRun2 = new Image();
dinoRun2.src = './assets/dino/DinoRun2.png';

const dinoJump = new Image();
dinoJump.src = './assets/dino/DinoJump.png';


let frameCount = 0;

class Dino {
  constructor(genome) {
    this.genome = genome;
    this.x = 50;
    this.y = 500;
    this.velocityY = 0;
    this.gravity = 1.5;
    this.score = 0;
    this.alive = true;
    this.width = 44;
    this.height = 47;
  }

  jump() {
    if (this.y >= 500) {
      this.velocityY = -20;
    }
  }

  update() {
    this.velocityY += this.gravity;
    this.y += this.velocityY;

    if (this.y > 500) {
      this.y = 500;
      this.velocityY = 0;
    }

    this.score++;
  }

  think(obstacles) {
    let closest = null;
    let minDist = Infinity;

    for (let obs of obstacles) {
      let dist = obs.x - this.x;
      if (dist > 0 && dist < minDist) {
        minDist = dist;
        closest = obs;
      }
    }

    if (closest) {
      const inputs = [
        closest.x / 800,
        closest.width / 50,
        closest.speed / 10,
        this.y / 600
      ];
      const [output] = this.genome.network.activate(inputs);
      if (output > 0.5) this.jump();
    }
  }


  draw(ctx) {
    const isOnGround = this.y >= 500;
    const sprite = isOnGround
      ? (Math.floor(frameCount / 5) % 2 === 0 ? dinoRun1 : dinoRun2)
      : dinoJump;
  
    ctx.drawImage(sprite, this.x, this.y, 44, 47);
  }  

}

class Obstacle {
  constructor() {
    this.x = 800;
    this.y = 500 + 30;
    this.speed = 10;

    // Seleciona um cactus aleatório
    const imgIndex = Math.floor(Math.random() * smallCactusImages.length);
    this.image = smallCactusImages[imgIndex];
    this.width = 34;
    this.height = 40;
  }

  update() {
    this.x -= this.speed;
  }

  offscreen() {
    return this.x + this.width < 0;
  }

  draw(ctx) {
    ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
  }
}
