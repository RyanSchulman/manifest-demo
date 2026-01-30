#!/usr/bin/env python3
import json
from pathlib import Path
import click
from pymongo import MongoClient, errors
from getpass import getpass

# TODO: Index on component and license


def get_mongo_client(host, port, username=None, password=None):
    """
    Connect to MongoDB with optional username/password.
    """
    try:
        if username and password:
            uri = f"mongodb://{username}:{password}@{host}:{port}/"
        else:
            uri = f"mongodb://{host}:{port}/"

        client = MongoClient(uri)
        client.admin.command("ping")  # test connection
        return client
    except errors.ConnectionFailure as e:
        click.secho(f"Error: Cannot connect to MongoDB: {e}", fg="red")
        raise click.Abort()


@click.group()
def cli():
    """SBOM CLI tool for ingesting CycloneDX 1.6 SBOMs into MongoDB."""
    pass

@cli.command()
@click.option("--component", help="Search SBOMs for a component by name")
@click.option("--version", help="Component version (requires --component)")
@click.option("--license", "license_name", help="Search SBOMs by license name")
@click.option("--host", default="localhost", help="MongoDB host")
@click.option("--port", default=27017, help="MongoDB port", type=int)
@click.option("--username", default=None, help="MongoDB username")
@click.option("--password", default=None, help="MongoDB password (prompted if not provided)")
@click.option("--db-name", default="sbom_db", help="Database name")
@click.option("--collection-name", default="sboms", help="Collection name")
def query(component, version, license_name, host, port, username, password, db_name, collection_name):
    """Query SBOMs by component name/version or license."""
    if username and not password:
        password = getpass(f"Password for MongoDB user '{username}': ")

    if not component and not license_name or (component and license_name):
        click.secho("Error: Must provide either --component or --license, but not both", fg="red")
        raise click.Abort()

    client = get_mongo_client(host, port, username, password)
    db = client[db_name]
    collection = db[collection_name]

    mongo_query = {}

    # TODO: Support the component and components section, not clear if this is actually requred from the
    # task since it just says "component" and not "components". I would just add another input called
    # `components` to accomplish this
    if component:
        mongo_query["metadata.component.name"] = component
        if version:
            mongo_query["metadata.component.version"] = version

    if license_name:
        # CycloneDX stores licenses in components[*].licenses[*].license.name
        mongo_query["components.licenses.license.id"] = license_name

    try:
        results = list(collection.find(mongo_query))
        if not results:
            click.secho("No SBOMs found matching the query.", fg="yellow")
            return

        for sbom in results:
            click.secho(f"SBOM ID: {sbom.get('_id')}", fg="green")
    except errors.PyMongoError as e:
        click.secho(f"Error querying SBOMs: {e}", fg="red")
        raise click.Abort()

@cli.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--host", default="localhost", help="MongoDB host")
@click.option("--port", default=27017, help="MongoDB port", type=int)
@click.option("--username", default=None, help="MongoDB username")
@click.option("--password", default=None, help="MongoDB password (will prompt if not provided)")
@click.option("--db-name", default="sbom_db", help="Database name")
@click.option("--collection-name", default="sboms", help="Collection name")
def ingest(file, host, port, username, password, db_name, collection_name):
    """
    Ingest a CycloneDX 1.6 SBOM JSON file into MongoDB.
    """
    file_path = Path(file)
    
    # Prompt for password if username is provided but password not
    if username and not password:
        password = getpass(f"Password for MongoDB user '{username}': ")

    # Load SBOM JSON
    try:
        with open(file_path, "r") as f:
            sbom_data = json.load(f)
    except json.JSONDecodeError as e:
        click.secho(f"Error: Failed to parse JSON: {e}", fg="red")
        raise click.Abort()

    # Validate CycloneDX version
    version = sbom_data.get("bomFormat")
    spec_version = sbom_data.get("specVersion")
    if version != "CycloneDX":
        click.secho("Warning: SBOM is not CycloneDX 1.6 format.", fg="yellow")

    # Connect to MongoDB
    client = get_mongo_client(host, port, username, password)
    db = client[db_name]
    collection = db[collection_name]

    # Insert SBOM
    try:
        result = collection.insert_one(sbom_data)
        click.secho(f"SBOM ingested successfully with ID: {result.inserted_id}", fg="green")
    except errors.PyMongoError as e:
        click.secho(f"Error: Failed to insert SBOM: {e}", fg="red")
        raise click.Abort()


if __name__ == "__main__":
    cli()
