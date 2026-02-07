# Pyvest

### Etape 1 ###
Installer le venv si pas déjà fait en ce mettant sur le bon cd (le projet racine) et en posant : 

py -m venv .venv
OU 
python -m venv .venv

Puis
.venv\Scripts\Activate.ps1 # Windows
source .venv/bin/activate # Mac

### Etape 2 ###
Installer les packages 
pip install -r requirements.txt obligatoire avant de démarrer
pip install -e . obligatoire sinon les packages doivent être précédé de src et le code n'est pas concut ainsi