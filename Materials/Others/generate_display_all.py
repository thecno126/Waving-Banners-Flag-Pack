
import os
from PIL import Image

# Chemins robustes basés sur l'emplacement du script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
png_dir = os.path.abspath(os.path.join(SCRIPT_DIR, '../../Releases/Backup/all_png'))
out_path = os.path.abspath(os.path.join(SCRIPT_DIR, '../Display/display_all.png'))
template_path = os.path.abspath(os.path.join(SCRIPT_DIR, '../Display/Display template.png'))
cols = 5  # Nombre de colonnes

# Liste noire (noms de fichiers sans extension)
blacklist = {
    'hegemony',
    'hegemony_alt',
    'persean_league',
    'luddic_church',
    'luddic_path',
    'pirates',
    'neutral_traders',
    'tritachyon',
    'sindrian_diktat',
}

# Lister et trier les png hors blacklist et ne contenant pas 'crest'
all_pngs = sorted([
    f for f in os.listdir(png_dir)
    if (f.lower().endswith('.png') 
        and os.path.splitext(f)[0] not in blacklist 
        and 'crest' not in f.lower())  # Nouvelle condition d'exclusion
])

# Largeur du template (à ajuster si besoin)
TEMPLATE_WIDTH = 1353


# Lister et trier les png hors blacklist
all_pngs = sorted([
    f for f in os.listdir(png_dir)
    if f.lower().endswith('.png') and os.path.splitext(f)[0] not in blacklist
])
nb_flags = len(all_pngs)
rows = (nb_flags + cols - 1) // cols

# Charger le template pour récupérer la taille d'un drapeau et les espacements
with Image.open(template_path) as template:
    margin_x = 30
    margin_y = 30
    space_x = 30
    space_y = 30
    flag_w = (TEMPLATE_WIDTH - (cols+1)*space_x) // cols
    flag_h = int(flag_w * 0.6)
    total_h = margin_y*2 + rows*flag_h + (rows-1)*space_y
    out = Image.new('RGBA', (TEMPLATE_WIDTH, total_h), (0,0,0,0))
    for idx, fname in enumerate(all_pngs):
        img = Image.open(os.path.join(png_dir, fname)).convert('RGBA')
        img = img.resize((int(flag_w), int(flag_h)), Image.LANCZOS)
        col = idx % cols
        row = idx // cols
        x = margin_x + col * (flag_w + space_x)
        y = margin_y + row * (flag_h + space_y)
        out.alpha_composite(img, (int(x), int(y)))
    out.save(out_path)
print('Fichier généré :', out_path)
