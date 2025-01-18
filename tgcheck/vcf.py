import random
import names

def generate_random_name():
    """Generate a random international name"""
    name_styles = [
        lambda: names.get_full_name(),                    # Western name (e.g., "John Smith")
        lambda: f"{names.get_first_name()} {names.get_last_name()}"  # Mixed style
    ]
    return random.choice(name_styles)()

def generate_vcf(phone_numbers, output_file="contacts.vcf"):
    """
    Generate a VCF file from a list of phone numbers with random names
    
    Args:
        phone_numbers (list): List of phone numbers
        output_file (str): Output VCF filename (default: contacts.vcf)
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for number in phone_numbers:
            # Format the number to remove any spaces or special characters
            clean_number = ''.join(filter(str.isdigit, str(number)))
            # Generate random name
            random_name = generate_random_name()
            
            # Write vCard format
            f.write("BEGIN:VCARD\n")
            f.write("VERSION:3.0\n")
            f.write(f"FN:{random_name}\n")  # Full Name
            f.write(f"TEL;TYPE=CELL:{clean_number}\n")
            f.write("END:VCARD\n")
            f.write("\n")

def main():
    numbers = []
    with open("ctusmr6p2jvlleut3oc0.txt", "r") as f:
        for _ in f.readlines():
            numbers.append(_.strip())
    # Randomly select 1000 numbers (or all if less than 1000)
    numbers = random.sample(numbers, min(1000, len(numbers)))
    generate_vcf(numbers)
    print("VCF file has been generated successfully!")

if __name__ == "__main__":
    main()
