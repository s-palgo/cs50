import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    csv_file_name = sys.argv[1]
    dna_file_name = sys.argv[2]

    # TODO: Read database file into a variable
    # TODO: Read DNA sequence file into a variable
    with open(csv_file_name, "r") as csv_file, open(dna_file_name, "r") as dna_file:
        csv_reader = csv.reader(csv_file)

        # Store header of CSV file in a string
        header = next(csv_file).rstrip()
        # Store STRs as a string by removing the first five letters from the
        # header string, e.g. "Name,"
        strs_as_string = header[5:]
        # Store STRs in a list
        strs = strs_as_string.split(',')

        # Store DNA sequence in a string by reading the DNA file
        dna = dna_file.read().rstrip()

        # A dictionary to store longest matches for each STR
        # E.g. the key is the STR and the corresponding value is the longest match
        # of that specific STR found in the DNA file.
        longest_matches = {}

        # TODO: Find longest match of each STR in DNA sequence
        for str in strs:
            longest_matches[str] = longest_match(dna, str)

        # TODO: Check database for matching profiles
        individual_is_found = False
        correct_individual = "No match"

        for individual in csv_reader:
            individual_is_potentially_a_match = True

            if individual_is_found:
                break
            else:
                for i in range(len(strs)):
                    if longest_matches[strs[i]] != int(individual[i + 1]):
                        individual_is_potentially_a_match = False
                        break
                if individual_is_potentially_a_match:
                    individual_is_found = True
                    correct_individual = individual[0]
                    break

        print(correct_individual)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()