
from Bio import SeqIO
import os

def selected_fasta(input_file, selected_ids, output_dir=None):

    records = list(SeqIO.parse(input_file, "fasta"))

    # Identify matching records
    found_records = [
        record for record in records
        if record.id in selected_ids
    ]

    if not found_records:
        print("FASTA ID not found!")
        return

    # Print selected sequences
    print("\nSelected FASTA sequence(s):")

    for record in found_records:
        print(record.format("fasta"))

    # Remove selected records from working copy
    remaining_records = [
        record for record in records
        if record.id not in selected_ids
    ]

    print(f"\nFound: {len(found_records)} sequence(s)")
    print(f"Remaining: {len(remaining_records)} sequence(s)")

    # Ask for confirmation before saving
    confirm = input(
        "\nDo you want to save the FASTA file without the selected ID(s)? (y/n): "
    ).strip().lower()

    if confirm == "y":

        # Use current working directory if no output directory is provided
        if not output_dir:
            output_dir = os.getcwd()

        output_dir = os.path.expanduser(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        # Generate output filename
        filename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, filename + "_cleaned.fasta")

        SeqIO.write(remaining_records, output_file, "fasta")

        print(f"\nSuccessfully saved: {output_file}")

    else:
        print("\nOperation cancelled. Original FASTA file remains unchanged.")


# Ask user to provide the FASTA file path
input_file = input("Enter the path to your FASTA file: ").strip()
input_file = os.path.expanduser(input_file)

# Validate input file
while not os.path.isfile(input_file):
    print("Error: File not found. Please provide a valid FASTA file path.")
    input_file = input("Enter the path to your FASTA file: ").strip()
    input_file = os.path.expanduser(input_file)

print(f"\nFASTA file loaded: {input_file}")

# Ask for FASTA ID
fasta_id = ""

while not fasta_id:
    fasta_id = input("Enter FASTA ID to remove: ").strip()

selected_ids = [fasta_id]

# Ask for output directory (optional)
output_dir = input(
    "\nEnter output directory (press Enter for current working directory): "
).strip()

# Execute
selected_fasta(input_file, selected_ids, output_dir)
