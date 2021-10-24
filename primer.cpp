#include <iostream>
using namespace std;
int main() {
  double x{}, y{};
  cout << "Enter x and y (separated by space)" << endl;
  cin >> x >> y;
  if (x < 0 || y < 0) {
    x = abs(x);
    y = abs(y);
  }
  cout << "x: &&&" << x << " y: " << y << endl;
  return 0;
}