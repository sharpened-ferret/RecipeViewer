# RecipeViewer 

RecipeViewer is a Python tool for downloading, storing, and viewing [schema-compliant](https://schema.org/Recipe) recipes.  
  
It uses [Django](https://www.djangoproject.com/) to provide a GUI for managing recipes, and to serve stored recipes from a local server. 

## Prerequisites 
Python (3.7 or higher)  
Django

## Required Libraries
[python-dateutil](https://dateutil.readthedocs.io/en/stable/)  
[scrape-schema-recipe](https://pypi.org/project/scrape-schema-recipe/)

  
## Installation & Setup
1. Make sure you have Python & Django installed.  
2. Use the package manager to install the required libraries.
```bash
pip install python-dateutil  
pip install scrape-schema-recipe
```  
3. Download the latest release archive and uncompress it where you want it.
4. To start the server on your LAN, navigate to the root directory of the uncompressed archive and run:
```bash
python manage.py runserver 0.0.0.0:8000
```
5. You should now be able to access the tool, at '[your-device-ip]:8000/viewer'. From here you can add, search, and view recipes.  
You can also access the admin menu, at '[your-device-ip]:8000/admin' to delete or modify stored recipes.  
The default admin account credentials are username = "admin" & password = "admin". It is **highly** recommended that you change these via the admin menu.


*Note: By default this tool is using the Django development server.  
This server is not designed to be secure in a production environment. So if you're planning on running this on the wider internet, you should probably [migrate it to Apache](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/modwsgi/) (or another server of your choice). 

---
## Styling & Customisation
The page styling is pretty minimal and basic, and sadly there's no darkmode (yet).  
You're more than welcome to customise the styling to your taste.

There are currently two stylesheets used for the front-end, 'recipe-style.css' for the recipe layout, and 'style.css' for everything else.  
These are located at '[RootDirectory]/viewer/static/viewer/~'