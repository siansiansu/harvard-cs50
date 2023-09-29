import csv
import sys


def read_csv(file):
    with open(file, newline="") as f:
        data = csv.DictReader(f)
        res = dict()
        for r in data:
            res.update(r)
        return res


def read_txt(file):
    with open(file, newline="") as f:
        return csv.reader(f)


def main():
    # Check for command-line usage
    n = len(sys.argv) - 1
    if n != 2:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(0)

    if "csv" not in sys.argv[1] or "txt" not in sys.argv[2]:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(0)

    # Read database file into a variable
    file1 = open(sys.argv[1], newline="")
    database = list()
    data1 = csv.DictReader(file1)
    for row in data1:
        database.append(row)

    # Read DNA sequence file into a variable
    file2 = open(sys.argv[2], newline="")
    data2 = csv.reader(file2)
    seq = ""
    for i in data2:
        seq = i[0]
        break

    # Find longest match of each STR in DNA sequence
    for i in database:
        columns = [key for key in i]
        count = 0
        match = len(columns) - 1
        for j in columns[1:]:
            if int(i[j]) == longest_match(seq, j):
                count += 1
            if count == match:
                print(i["name"])
                return
    print("No match")
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
