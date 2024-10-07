struct CongGenerator {
  int state;
  int modulus;
  int free_coeff;
  int lin_coeff;

  void operator init(int modulus = 1000, int free_coeff = 169, int lin_coeff = 14, real initial_value = 0.1) {
    this.modulus = modulus;
    this.state = floor(initial_value * modulus);
    this.lin_coeff = lin_coeff;
    this.free_coeff = free_coeff;
  }

  real next() {
    this.state = (this.lin_coeff * this.state + this.free_coeff) % this.modulus;
    return this.state / this.modulus;
  }
}
