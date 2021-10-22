#include <cmath>
#include <iostream>
using namespace std;
int main() {
  int sum_cubes{};
  for (int i{100}; i < 1000; i++) {
    sum_cubes = pow(i % 10, 3) + pow(i / 10 % 10, 3) + pow(i / 100, 3);
    if (i == sum_cubes) {
      cout << i << endl;
    }
  }
  return 0;
}