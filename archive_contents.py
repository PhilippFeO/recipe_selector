import os
import shutil
import logging
from datetime import datetime
from pathlib import Path


def archive_contents(shopping_list_file: str, recipes: list[str]):
    """
    Save shopping list to yyyy/yyyy-mm-dd-recipes[0]-...-recipes[n]/yyyy-mm-dd-recipes[0]-...-recipes[n].txt.
    Create hard links of the used recipes next to it, to have all resources close at hand.
    """
    # TODO: Remove following line <31-01-2024>
    print()
    # Get the current date in the format 'yyyy-mm-dd'
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Create the directory for the current year
    current_year = datetime.now().strftime('%Y')
    # year_directory = os.path.join(os.getcwd(), current_year)
    year_dir = current_year
    os.makedirs(year_dir, exist_ok=True)

    # Create the subdirectory with the specified scheme
    recipe_names = [Path(recipe).stem for recipe in recipes]
    subdir_name = f'{current_date}-{"-".join(recipe_names)}'
    subdir_path = os.path.join(year_dir, subdir_name)
    os.makedirs(subdir_path, exist_ok=True)

    # Copy shopping list into archive folder
    shopping_list_dst = os.path.join(subdir_path, f'{subdir_name}.txt')
    shutil.copy(shopping_list_file, shopping_list_dst)
    logging.info(f"File '{shopping_list_file}' copied to '{shopping_list_dst}' successfully.")

    # Generate hard links for each specified file
    for recipe in recipes:
        dst = os.path.join(subdir_path, os.path.basename(recipe))  # Only filename & extension
        os.link(recipe, dst)
        logging.info(f"Hard link created for {recipe} at {dst}")

    # TODO: Remove following line <31-01-2024>
    print()


if __name__ == "__main__":
    lines = ["Line 1", "Line 2", "Line 3"]
    archive_contents(lines, "recipes/Pesto_alla_Trapanese.yaml", "recipes/Rührei.yaml")
