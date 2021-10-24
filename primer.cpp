#include <iostream>
#define maxi(a, b) ((a) > (b)) ? (a) : (b)
using namespace std;

int main() {
  double x{}, y{}, z{};
  cout << "Введите x y z:" << endl;
  cin >> x >> y >> z;
  if ((z >= x) and (z <= y)) {
    x = y = z = maxi(x, maxi(y, z));
  } else if (not((z >= y) and (z <= x))) {
    x *= x;
    y *= y;
    z *= z;
  }
  cout << "x: " << x << "\ny: " << y << "\nz: " << z << endl;
  return 0;
}