# Odrive Register cpp
this is header library of odrive register of each firmware version.
## usage
``` main.cpp
// include only specific version
#include <odrive_reg/odrive_reg_0_6_11.hpp>

int main(){
    // registers in odrive_reg::endpoints::/*any_registers*/
    using namespace odrive_reg::endpoints;

    // you can access member like this
    std::cout << "ID: " << vbus_voltage::id << "\n";
    std::cout << "Type: " << static_cast<int>(vbus_voltage::type) << "\n";
    std::cout << "Readable: " << vbus_voltage::readable << "\n";
    std::cout << "Writable: " << vbus_voltage::writable << "\n";
    std::cout << "Value type: " << typeid(vbus_voltage::value_type).name() << "\n";
    std::cout << "Size: " << vbus_voltage::size << "\n";

    return 0;
}