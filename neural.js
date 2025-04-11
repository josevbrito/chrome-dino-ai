// neural.js

class NeuralNetwork {
    constructor(inputSize, hiddenSize, outputSize) {
      this.inputSize = inputSize;
      this.hiddenSize = hiddenSize;
      this.outputSize = outputSize;
  
      // Inicialização aleatória dos pesos
      this.weightsInputHidden = this.randomMatrix(this.inputSize, this.hiddenSize);
      this.weightsHiddenOutput = this.randomMatrix(this.hiddenSize, this.outputSize);
    }
  
    randomMatrix(rows, cols) {
      let matrix = [];
      for (let i = 0; i < rows; i++) {
        matrix[i] = [];
        for (let j = 0; j < cols; j++) {
          matrix[i][j] = Math.random() * 2 - 1; // Valores entre -1 e 1
        }
      }
      return matrix;
    }
  
    activate(inputs) {
      // Função de ativação sigmoide
      const sigmoid = x => 1 / (1 + Math.exp(-x));
  
      // Propagação para a camada oculta
      let hidden = [];
      for (let i = 0; i < this.hiddenSize; i++) {
        let sum = 0;
        for (let j = 0; j < this.inputSize; j++) {
          sum += inputs[j] * this.weightsInputHidden[j][i];
        }
        hidden[i] = sigmoid(sum);
      }
  
      // Propagação para a camada de saída
      let outputs = [];
      for (let i = 0; i < this.outputSize; i++) {
        let sum = 0;
        for (let j = 0; j < this.hiddenSize; j++) {
          sum += hidden[j] * this.weightsHiddenOutput[j][i];
        }
        outputs[i] = sigmoid(sum);
      }
  
      return outputs;
    }

  }
  