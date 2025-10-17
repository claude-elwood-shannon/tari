# Integración CI con Ledger App Builder

Este documento describe cómo integrar el testing framework de Tari Ledger Wallet con el sistema de CI usando la imagen Docker oficial de Ledger.

## Descripción General

El proyecto ya tiene un workflow de CI configurado en `.github/workflows/build_ledger_wallet.yml` que utiliza la imagen Docker oficial de Ledger para compilar la aplicación para múltiples dispositivos.

## Workflow CI Existente

### Configuración Actual

El workflow actual:
- **Imagen Docker**: `ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:4.15.0`
- **Dispositivos soportados**: 
  - ✅ `nanosplus` (funcionando correctamente)
  - ✅ `flex` (funcionando correctamente)
  - ⚠️ `nanox` (best_effort: true)
  - ⚠️ `stax` (best_effort: true)

### Comando de Compilación

```yaml
docker run --rm \
  -v ".:/app" \
  -w "/app/applications/minotari_ledger_wallet/wallet" \
  ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:4.15.0 \
  cargo ledger build ${{ matrix.ledger_target }} -- --locked
```

## Imágenes Docker Disponibles

### Tipos de Imágenes

1. **`ledger-app-builder`** (imagen completa)
   - Base: Debian slim + herramientas Rust
   - Uso: Compilación estándar
   - Comando: `docker pull ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:latest`

2. **`ledger-app-builder-lite`** (imagen ligera)
   - Base: Debian slim
   - Uso: Solo compilación C
   - Comando: `docker pull ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder-lite:latest`

3. **`ledger-app-dev-tools`** (imagen de desarrollo)
   - Base: Imagen completa + Ragger + Speculos
   - Uso: Testing y desarrollo
   - Comando: `docker pull ghcr.io/ledgerhq/ledger-app-builder/ledger-app-dev-tools:latest`

## Integración de Testing en CI

### Propuesta de Workflow de Testing

Para integrar los tests Ragger en la CI, podemos crear un workflow adicional:

```yaml
name: Test Ledger Wallet with Ragger

on:
  push:
    branches: [ development, mainnet, nextnet ]
    paths:
      - 'applications/minotari_ledger_wallet/**'
      - 'tests/ledger_wallet/**'
  pull_request:
    branches: [ development, mainnet, nextnet ]
    paths:
      - 'applications/minotari_ledger_wallet/**'
      - 'tests/ledger_wallet/**'

jobs:
  ragger-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        device: [nanosp, flex]
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          pip install ledgered
          pip install 'ragger[speculos]'
          
      - name: Run Ragger tests
        run: |
          cd tests/ledger_wallet
          python -m pytest test_tari_ragger.py --device ${{ matrix.device }} -v
```

### Comandos de Testing con Docker

Para ejecutar tests dentro del contenedor de desarrollo:

```bash
# Ejecutar contenedor de desarrollo
docker run --rm -ti \
  -v "$(realpath .):/app" \
  --user $(id -u):$(id -g) \
  -v "/tmp/.X11-unix:/tmp/.X11-unix" \
  -e DISPLAY=$DISPLAY \
  ghcr.io/ledgerhq/ledger-app-builder/ledger-app-dev-tools:latest

# Dentro del contenedor
python -m virtualenv venv --system-site-package
source ./venv/bin/activate
pip install -r tests/requirements.txt
python -m pytest tests/ledger_wallet/test_tari_ragger.py --device nanosp -v
```

## Mejoras Propuestas para la CI

### 1. Actualizar Versión de la Imagen Docker

El workflow actual usa la versión `4.15.0`. Podemos actualizar a la última versión:

```yaml
env:
  DOCKER_IMAGE: "ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:latest"
```

### 2. Agregar Testing Automático

Proponemos agregar un job de testing después de la compilación:

```yaml
  ragger-testing:
    needs: [builds]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        device: [nanosp, flex]
    
    steps:
      - name: Download built artifacts
        uses: actions/download-artifact@v4
        with:
          pattern: "minotari_ledger_wallet-*-${{ matrix.device }}-*"
          
      - name: Run Ragger tests
        run: |
          # Configurar entorno y ejecutar tests
          python -m pytest tests/ledger_wallet/test_tari_ragger.py --device ${{ matrix.device }} -v
```

### 3. Integración con Speculos

Para testing automatizado sin interfaz gráfica:

```yaml
- name: Run headless Speculos tests
  run: |
    # Ejecutar Speculos en modo headless
    speculos build/nanosplus/bin/app.elf --model nanosplus --display headless &
    # Ejecutar tests Ragger
    python -m pytest tests/ledger_wallet/test_tari_ragger.py --device nanosp -v
```

## Configuración de Variables de Entorno

### Variables Requeridas

```bash
# Para compilación local (equivalente a CI)
export LEDGER_SDK_PATH=/data/git/tari/ledger-secure-sdk

# Para testing con Ragger
export RAGGER_DEVICE=nanosp  # o flex
```

### Manifest Configuration

El archivo `ledger_app.toml` debe estar configurado correctamente:

```toml
[app]
sdk = "rust"
build_directory = "applications/minotari_ledger_wallet/wallet"
devices = ["flex", "nanosp"]
```

## Troubleshooting de CI

### Problemas Comunes

1. **Compilación falla para flex**
   - Solución: Limpiar caché antes de compilar
   ```bash
   cargo clean
   cargo ledger build flex
   ```

2. **Ragger no encuentra el manifest**
   - Verificar que `ledger_app.toml` esté en el directorio raíz
   - Confirmar que la ruta `build_directory` sea correcta

3. **Speculos no inicia en CI**
   - Usar modo headless: `--display headless`
   - Verificar que el binario esté compilado correctamente

### Logs y Debugging

Agregar logging detallado al workflow:

```yaml
- name: Debug build output
  run: |
    ls -la applications/minotari_ledger_wallet/wallet/target/${{ matrix.ledger_target }}/release/
    file applications/minotari_ledger_wallet/wallet/target/${{ matrix.ledger_target }}/release/minotari_ledger_wallet
```

## Recursos Adicionales

- [Repositorio ledger-app-builder](https://github.com/LedgerHQ/ledger-app-builder)
- [Documentación de Ragger](https://github.com/LedgerHQ/ragger)
- [Documentación de Speculos](https://github.com/LedgerHQ/speculos)

## Conclusión

La integración CI actual ya está bien configurada usando la imagen Docker oficial de Ledger. Las principales mejoras propuestas son:
1. Agregar testing automatizado con Ragger
2. Actualizar a la última versión de la imagen Docker
3. Mejorar el troubleshooting y logging

El framework de testing está listo para ser integrado en la pipeline de CI existente.
