#!/bin/bash

# Specify the number of files to choose via command line
N=$1

# Specify the directory path
recipes="recipes"

# Check if the directory exists
if [ -d "$recipes" ]; then
    # Get a list of files in the directory
    files=("$recipes"/*)

    # Check if there are files in the directory, an empty recipe directory makes no sense
    num_files=$(ls $recipes | wc -w)
    if [ $num_files -eq 0 ]; then
        echo "Error: No files found in the directory '$recipes'."
        exit 1
    fi

    # Get the number of files in the directory
    if [ $# -ne 1 ]; then
        echo "Usage: ./recipe_selector.sh N"
        echo -e "\twhere 0 < N <= $num_files (Number of Recipes)"
        exit 1
    fi

    # Check if N is greater than the number of files
    if [ "$N" -gt "$num_files" ]; then
        echo "Error: $N is greater than the number of files in the directory ($num_files)."
        exit 1
    fi

    # Generate an array of random indices within the range of the number of files
    indices=($(shuf -i 0-$(($num_files-1)) -n $N))

    # Loop through the randomly chosen indices and get the corresponding files
    selected_files=()
    for index in "${indices[@]}"; do
        selected_files+=("${files[index]}")
    done

    # Retrieve ingredients of selected files
    python3 main.py "${selected_files[@]}"

    # Deprecation warning
    sleep 3 # Get users attention (hopefully)
    echo "This repository is depracted in favor of 'https://github.com/PhilippFeO/grocery-shopper'. It will be deleted in the middle distant future. If you like the repository, consider switching. You can keep your recipes and res/ingredient_category_url.csv file. If any questions arise, feel free to open an issue!"
else
    echo "Error: Directory '$recipes' not found."
    exit 1
fi
