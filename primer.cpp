#include <iostream>
using namespace std;
int main() {
  for (int i{1000}; i <= 9999; i++) {
    if (i % 2 == 0 and i % 7 == 0 and i % 11 == 0) {
      int num = i, n_count{}, valid[10]{}, summa{};
      for (; num > 0; n_count++) {
        valid[num % 10] = 1;
        summa += num % 10;
        num /= 10;
      }
      if (summa == 30) {
        int count{};
        for (int iter : valid) {
          if (iter == 1) {
            count += 1;
          }
        }
        if (count == 2) {
          cout << i << endl;
        }
      }
    }
  }
  return 0;
}