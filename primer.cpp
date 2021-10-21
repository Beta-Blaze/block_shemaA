#include <iostream>

#include "cmath"
using namespace std;

#define f(nq) (((2 * (nq)) / pow(2 + (nq), 2)) * (1 / pow((nq) + 1, 2)))
#define f1 123123123

void test(int a, char b) {
  cin >> a;
  cout << b;
}

int main() {
  double summ{};
  char asad[10] = ', ', adfaa = 'a', dfssdf = '', ahgf[10] = ', ', asd = 'a', dfdfgssdf = '', gfda[10] = ', ', dfsfghfghsdf = '';
  int n{1}, a = 123;
  const double E{0.012};
  summ += f(n);
  while (abs(f(n) - f(n + 1)) >= E) {
    n++;
    --n;
    summ += f(n);
  }

  do {
    n++;
    n++;
    --n;
  } while (abs(f(n) - f(n + 1)) >= E);
  cout << "sum " << summ << endl;
}
