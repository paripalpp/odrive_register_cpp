import os, sys
import json
import requests

def odrive_reg_type_from_string(type_str) -> str:
    # Convert the type string to a OdriveRegType
    if type_str == "bool":
        return "OdriveRegType::Bool"
    elif type_str == "uint8":
        return "OdriveRegType::UInt8"
    elif type_str == "uint16":
        return "OdriveRegType::UInt16"
    elif type_str == "uint32":
        return "OdriveRegType::UInt32"
    elif type_str == "uint64":
        return "OdriveRegType::UInt64"
    elif type_str == "int32":
        return "OdriveRegType::Int32"
    elif type_str == "int64":
        return "OdriveRegType::Int64"
    elif type_str == "float":
        return "OdriveRegType::Float"
    elif type_str == "function":
        return "OdriveRegType::Function"
    elif type_str == "endpoint_ref":
        return "OdriveRegType::EndpointRef"
    else:
        raise ValueError(f"Unknown type: {type_str}")

def generate_enums_from_json_endpoints(json_endpoint) -> str:
    # json endpoint is a dictionary
    # key is the name of the enum
    # value has id, type, and access type
    hpp_content = ""
    # Iterate through the JSON endpoint
    for name, value in json_endpoint.items():
        id = value['id']
        type = value['type']
        print(f"Generating enum for {name} with id {id} and type {type}")
        name = name.replace('.', '__')
        hpp_content += "    "  # indent for the namespace
        if type != "function":
            # access type is active after 6.11.0. default is read only
            access_type = value.get('access_type', 'r')
            hpp_content += f"using {name} = OdriveReg<{value['id']}, {odrive_reg_type_from_string(value['type'])}, "
            if access_type == "r":
                hpp_content += "true, false>;\n"
            elif access_type == "rw":
                hpp_content += "true, true>;\n"
        elif type == "function":
            hpp_content += f"using {name} = OdriveReg<{value['id']}, {odrive_reg_type_from_string(value['type'])}, false, false>;\n"
        else:
            raise ValueError(f"Unknown type: {type}")
    return hpp_content


def generate_hpp(json, output_dir, url=None):
    # Extract the name and description
    fw_version = json.get('fw_version', '0.0.0')
    hw_version = json.get('hw_version', '0.0.0')

    # generate the name from fw_version x.x.x -> x_x_x
    name = "odrive_reg_" + fw_version.replace('.', '_')

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate the .hpp file content
    hpp_content = ""
    hpp_content += f"// {name}.hpp\n"
    hpp_content += f"// Odrive firmware version: {fw_version}\n"
    hpp_content += f"// Odrive hardware version: {hw_version}\n"
    hpp_content += f"// Generated from {url}\n"
    hpp_content += f"#ifndef {name.upper()}_HPP\n"
    hpp_content += f"#define {name.upper()}_HPP\n"
    hpp_content += f"#include <string_view>\n"
    hpp_content += f"#include \"odrive_reg_type.hpp\"\n"
    hpp_content += f"\n"
    hpp_content += f"namespace odrive_reg {{\n"
    hpp_content += f"    constexpr std::string_view fw_version = \"{fw_version}\";\n"
    hpp_content += f"    constexpr std::string_view hw_version = \"{hw_version}\";\n"
    hpp_content += f"}} // namespace odrive_reg\n"
    hpp_content += f"\n"
    hpp_content += f"namespace odrive_reg::endpoints {{\n"
    hpp_content += f"\n"
    hpp_content += generate_enums_from_json_endpoints(json['endpoints'])
    hpp_content += f"\n"
    hpp_content += f"}} // namespace odrive_reg::endpoints\n"
    hpp_content += f"\n"
    hpp_content += f"#endif // {name.upper()}_HPP\n"

    # Write the content to a .hpp file
    hpp_file_path = os.path.join(output_dir, f"{name}.hpp")
    with open(hpp_file_path, 'w') as hpp_file:
        hpp_file.write(hpp_content)

    print(f"Generated {hpp_file_path}")


if __name__ == "__main__":
    with open("flat_endpoint_url.json", "r") as f:
        config = json.load(f)
    
    # Get the JSON file from listed URLs
    urls = config
    output_dir = "include"
    for url in urls:
        print(f"Fetching {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully fetched {url}")
            json_file = response.json()
            generate_hpp(json_file, output_dir, url)
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
    # Generate the .hpp file for the local JSON file
    local_json_file = "local_file.json"
    if os.path.exists(local_json_file):
        generate_hpp(local_json_file, output_dir)
    else:
        print(f"Local JSON file {local_json_file} does not exist.")

