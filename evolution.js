class Genome {
    constructor(network) {
      this.network = network;
      this.fitness = 0;
    }
  
    mutate(rate) {
      // Mutação dos pesos com uma determinada taxa
      const mutateMatrix = matrix => {
        return matrix.map(row =>
          row.map(value => (Math.random() < rate ? value + (Math.random() * 2 - 1) * 0.1 : value))
        );
      };
  
      this.network.weightsInputHidden = mutateMatrix(this.network.weightsInputHidden);
      this.network.weightsHiddenOutput = mutateMatrix(this.network.weightsHiddenOutput);
    }
  
    crossover(partner) {
      // Crossover simples entre dois genomas
      const crossoverMatrix = (m1, m2) => {
        return m1.map((row, i) =>
          row.map((val, j) => (Math.random() < 0.5 ? val : m2[i][j]))
        );
      };
  
      let childNetwork = new NeuralNetwork(
        this.network.inputSize,
        this.network.hiddenSize,
        this.network.outputSize
      );
  
      childNetwork.weightsInputHidden = crossoverMatrix(
        this.network.weightsInputHidden,
        partner.network.weightsInputHidden
      );
      childNetwork.weightsHiddenOutput = crossoverMatrix(
        this.network.weightsHiddenOutput,
        partner.network.weightsHiddenOutput
      );
  
      return new Genome(childNetwork);
    }
  }
  
  class Evolution {
    constructor(populationSize, inputSize, hiddenSize, outputSize) {
      this.populationSize = populationSize;
      this.inputSize = inputSize;
      this.hiddenSize = hiddenSize;
      this.outputSize = outputSize;
      this.generation = 0;
      this.population = this.createInitialPopulation();
    }
  
    createInitialPopulation() {
      let population = [];
      for (let i = 0; i < this.populationSize; i++) {
        let network = new NeuralNetwork(this.inputSize, this.hiddenSize, this.outputSize);
        population.push(new Genome(network));
      }
      return population;
    }
  
    evolve() {
      // Ordenar por fitness
      this.population.sort((a, b) => b.fitness - a.fitness);
  
      // Selecionar os melhores indivíduos (metade)
      let survivors = this.population.slice(0, this.populationSize / 2);
  
      // Gerar nova população por crossover e mutação
      let newPopulation = [];
      for (let i = 0; i < this.populationSize; i++) {
        let parentA = survivors[Math.floor(Math.random() * survivors.length)];
        let parentB = survivors[Math.floor(Math.random() * survivors.length)];
  
        let child = parentA.crossover(parentB);
        child.mutate(0.1); // Taxa de mutação de 10%
        newPopulation.push(child);
      }
  
      this.population = newPopulation;
      this.generation++;
    }
  }
  