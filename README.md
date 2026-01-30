## Setup 
You may need to `export PATH="$HOME/.local/bin:$PATH"` to get the cli to work properly

Run ./setup.sh, you must have `docker` and `docker-compose` installed for this to work.

## Commands:
There are three commands in the format:
```
sbom-cli ingest <sbom-file>
sbom-cli query --component <name> [--version <version>]
sbom-cli query --license <license>
```

### Example commands:
#### Keycloak
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
sbom-cli query --component "keycloak-parent" \
    --host localhost \
    --port 27017 \
    --username admin \
    --password password \
    --db-name sbom_db \
    --collection-name sboms
```


#### Proton Bridge
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
sbom-cli query --component "github.com/ProtonMail/proton-bridge" --version "v1.6.3" \
    --host localhost \
    --port 27017 \
    --username admin \
    --password password \
    --db-name sbom_db \
    --collection-name sboms
```

#### Both

```
sbom-cli query --license "Apache-2.0" \
    --host localhost \
    --port 27017 \
    --username admin \
    --password password \
    --db-name sbom_db \
    --collection-name sboms

```