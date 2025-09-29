#!/bin/bash

# ------------------------------
# Script seguro para registrar app Django
# ------------------------------

APP_NAME_ORIGINAL="Escuela"   # nombre actual de la carpeta (puede ser mayúscula)
APP_NAME_LOWER="escuela"      # nombre que Django reconoce

SETTINGS_FILE="core/settings.py"

echo "1️⃣ Verificando carpeta de la app..."
if [ -d "$APP_NAME_ORIGINAL" ]; then
    echo "Renombrando carpeta $APP_NAME_ORIGINAL -> $APP_NAME_LOWER"
    mv "$APP_NAME_ORIGINAL" "$APP_NAME_LOWER"
else
    echo "La carpeta $APP_NAME_ORIGINAL no existe, se asume que ya está renombrada"
fi

# ------------------------------
# Actualizar apps.py
# ------------------------------
APPS_PY="$APP_NAME_LOWER/apps.py"

echo "2️⃣ Actualizando apps.py..."
cat > "$APPS_PY" <<EOL
from django.apps import AppConfig

class EscuelaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '$APP_NAME_LOWER'
EOL

# ------------------------------
# Agregar app a INSTALLED_APPS
# ------------------------------
echo "3️⃣ Agregando la app a INSTALLED_APPS si no está..."
if ! grep -q "'$APP_NAME_LOWER'" "$SETTINGS_FILE"; then
    echo "Agregando '$APP_NAME_LOWER' a INSTALLED_APPS"
    sed -i '' "/django.contrib.staticfiles/i\\
    '$APP_NAME_LOWER',
" "$SETTINGS_FILE"
else
    echo "La app ya está registrada en INSTALLED_APPS"
fi

# ------------------------------
# Limpiar migraciones antiguas
# ------------------------------
echo "4️⃣ Limpiando migraciones antiguas..."
if [ -d "$APP_NAME_LOWER/migrations" ]; then
    rm -rf "$APP_NAME_LOWER/migrations"
fi
mkdir "$APP_NAME_LOWER/migrations"
touch "$APP_NAME_LOWER/migrations/__init__.py"

# ------------------------------
# Crear nuevas migraciones
# ------------------------------
echo "5️⃣ Creando nuevas migraciones..."
python manage.py makemigrations $APP_NAME_LOWER

# ------------------------------
# Aplicar migraciones
# ------------------------------
echo "6️⃣ Aplicando migraciones..."
python manage.py migrate

echo "✅ App '$APP_NAME_LOWER' lista y migraciones aplicadas."
