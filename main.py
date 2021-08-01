import scrape_schema_recipe
import sqlite3

def main():
    url = input("Enter a recipe URL:")
    recipe_list = scrape_schema_recipe.scrape_url(url, python_objects=True)
    if (len(recipe_list) > 0):
        recipe = recipe_list[0]
        print(recipe)
    else:
        print("No compatible recipes found on that page.")

main()