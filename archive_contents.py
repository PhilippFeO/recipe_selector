import os
import shutil
import logging
from datetime import datetime
from pathlib import Path


def archive_contents(shopping_list_file: str, recipe_paths: list[str]):
    """
    Save shopping list to yyyy/yyyy-mm-dd-recipes[0]-...-recipes[n]/yyyy-mm-dd-recipes[0]-...-recipes[n].txt.
    Create hard links of the used recipes next to it to have all resources close at hand.
    """
    # TODO: Remove following line <31-01-2024>
    print()
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_year = datetime.now().strftime('%Y')

    # Create subdirectory with the specified scheme
    recipe_names = [Path(recipe).stem for recipe in recipe_paths]
    subdir_name = f'{current_date}-{"-".join(recipe_names)}'
    subdir_path = os.path.join(current_year, subdir_name)
    os.makedirs(subdir_path, exist_ok=True)

    # Copy shopping list into archive folder
    shopping_list_dst = os.path.join(subdir_path, f'{subdir_name}.txt')
    shutil.copy(shopping_list_file, shopping_list_dst)
    logging.info(f"File '{shopping_list_file}' copied to '{shopping_list_dst}' successfully.")

    # Generate hard links for each specified file
    # recipe_file scheme: file.ext
    for recipe_file, recipe_path in zip((Path(recipe_path).name for recipe_path in recipe_paths), recipe_paths):
        dst_yaml = os.path.join(subdir_path, recipe_file)
        recipe_file_pdf = recipe_file.replace('yaml', 'pdf')
        dst_pdf = os.path.join(subdir_path, recipe_file_pdf)
        try:
            os.link(recipe_path, dst_yaml)
            os.link(f'recipes/pdf/{recipe_file_pdf}', dst_pdf)
        except FileExistsError as fee:
            logging.error(f'Error Message: {fee}')

    # Create symlink to folder containing shopping list and recipes
    link_name = 'Selection'
    temp_link = link_name + ".new"
    try:
        os.remove(link_name)
    except FileNotFoundError as fnfe:
        logging.error(f'Error while removing link "{link_name}":\n\t{fnfe}')
    os.symlink(f'{subdir_path}', temp_link)
    os.rename(temp_link, link_name)
    # TODO: Remove following line <31-01-2024>
    print()


if __name__ == "__main__":
    lines = ["Line 1", "Line 2", "Line 3"]
    archive_contents(lines, "recipes/Pesto_alla_Trapanese.yaml", "recipes/Rührei.yaml")
