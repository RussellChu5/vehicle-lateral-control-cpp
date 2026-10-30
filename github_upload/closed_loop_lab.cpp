#include <fstream>
#include <iostream>
#include <cmath>
#include "PID_controller.h"

struct Vehicle {
    double x = 0.0;
    double y = 0.0;
    double psi = 0.0;
    double v = 5.0;

    void updateState(double a, double delta, double L, double dt) {
        x = x + v * std::cos(psi) * dt;
        y = y + v * std::sin(psi) * dt;
        psi = psi + v / L * std::tan(delta) * dt;
        v = v + a * dt;
    }
};

int main() {
    Vehicle car;
    car.x = 0.0;
    car.y = 1.0;
    car.psi = 0.0;
    car.v = 5.0;

    double L = 2.8;
    double dt = 0.05;

    PID_controller pid(0.15, 0.0, 4.0, 0.0, 0.35, -0.35);

    std::ofstream csv(
        R"(C:\Users\16601\auto_vehicle_control\cpp_practice\closed_loop_lab\pd_tracking.csv)"
    );

    if (!csv.is_open()) {
        std::cerr << "Cannot open CSV file\n";
        return 1;
    }

    csv.precision(15);
    csv << "t,x,y,psi,v,delta\n";
    csv << "0," << car.x << ","
        << car.y << ","
        << car.psi << ","
        << car.v << ",0\n";

    for (int i = 0; i < 240; i++) {
        double delta = pid.calOutput(car.y);

        car.updateState(0.0, delta, L, dt);

        csv << (i + 1) * dt << ","
            << car.x << ","
            << car.y << ","
            << car.psi << ","
            << car.v << ","
            << delta << '\n';

        if ((i + 1) % 20 == 0) {
            std::cout << "t = " << (i + 1) * dt
                << " s, y = " << car.y
                << " m, delta = " << delta << '\n';
        }
    }

    return 0;
}