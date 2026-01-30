## Setup 
You may need to `export PATH="$HOME/.local/bin:$PATH"`

Run ./setup.sh

## Example Commands:

```
sbom-cli ingest example/keycloak.json \
    --host localhost \
    --port 27017 \
    --username admin \
    --password password \
    --db-name sbom_db \
    --collection-name sboms
```

```
sbom-cli ingest example/proton-bridge.json \
    --host localhost \
    --port 27017 \
    --username admin \
    --password password \
    --db-name sbom_db \
    --collection-name sboms
```

```
sbom-cli query --component "bcpkix-jdk15on" \
    --host localhost \
    --port 27017 \
    --username admin \
    --password password \
    --db-name sbom_db \
    --collection-name sboms
```
```
sbom-cli query --component "github.com/ProtonMail/proton-bridge" \
    --host localhost \
    --port 27017 \
    --username admin \
    --password password \
    --db-name sbom_db \
    --collection-name sboms
```
```
sbom-cli query --license "Apache-2.0" \
    --host localhost \
    --port 27017 \
    --username admin \
    --password password \
    --db-name sbom_db \
    --collection-name sboms

```