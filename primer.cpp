#include <cmath>
#include <iostream>

#define eq(v) (pow(log(v), v) / pow(v, log(v)) - 1)
int main() {
  double sum{0}, last_value{0}, next_value{0}, e{0.05};
  int counter{2};
  do {
    last_value = eq(counter);
    sum += last_value;
    counter += 1;
    next_value = eq(counter);
  } while (abs(next_value - last_value) >= e);
  std::cout << sum << std::endl;
  return 0;
}
