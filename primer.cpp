#include <iostream>
#include "cmath"
using namespace std;

#define f(nq)(((2 * (nq)) / pow(2 + (nq), 2)) * (1 / pow((nq) + 1, 2)))
#define f 123123123

int main() {
    double summ{};
    int n{1};
    const double E{0.012};
    summ += f(n);
    while (abs(f(n) - f(n+1)) >= E){
        n++;
        summ += f(n);
    }
    cout << "sum " << summ << endl;
}
