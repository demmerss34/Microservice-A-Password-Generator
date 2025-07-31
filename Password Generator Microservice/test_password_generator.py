import requests

# Define valid types
valid_types = ["PIN", "Medium", "Strong", "Custom"]

# Prompt for password type until valid
while True:
    password_type = input("Enter password type (PIN, Medium, "
                          "Strong, Custom): ").strip()
    if password_type in valid_types:
        break
    print("Invalid type. Please enter one of:", ", ".join(valid_types))

# Prompt for length (optional)
while True:
    length_input = input("Enter password length "
                         "(press Enter to use default): ").strip()
    if not length_input:
        length = None
        break
    if length_input.isdigit():
        length = int(length_input)
        break
    print("Invalid input. Please enter a number.")

# Prompt for symbols if needed
symbols = False
if password_type in ["Strong", "Custom"]:
    while True:
        symbols_input = input("Include symbols? (true/false): ").strip().lower()
        if symbols_input == "true":
            symbols = True
            break
        elif symbols_input == "false":
            symbols = False
            break
        else:
            print("Please enter 'true' or 'false'.")


# Build request parameters
params = {"type": password_type}
if length is not None:
    params["length"] = length
if password_type in ["Strong", "Custom"]:
    params["symbols"] = symbols

# Send request to microservice
response = requests.get("http://localhost:8000/generate_password",
                        params=params)

# Display result
print("\n✅ Password Generator Response")
print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Failed to parse JSON:", e)


