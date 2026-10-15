<a className="gh-badge" href="https://datahub.io/core/geo-nuts-administrative-boundaries"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

# Geo Boundaries for NUTS administrative levels 1, 2 and 3

If you don't know what NUTS (Nomenclature of Territorial Units for Statistics) are, see the [related Wikipedia article](https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics).

## Data

Data is sourced from the [GISCO EU website](https://gisco-services.ec.europa.eu/distribution/v2/nuts/).

We provide data as GeoJSON. Data is stored in the `data` folder.

Datasets are available for NUTS levels 1, 2, and 3.

Each feature is one region. The files `data/NUTS_RG_60M_2024_4326_LEVL_1.geojson`, `..._LEVL_2.geojson` and `..._LEVL_3.geojson` hold NUTS levels 1, 2 and 3 (115, 299 and 1,345 regions in the 2024 edition). Geometries are `MultiPolygon`. Each feature has these properties:

* **NUTS_ID**: String. NUTS code of the region (for example `DE212`). Unique in each file.
* **LEVL_CODE**: Integer. NUTS level (1, 2 or 3).
* **CNTR_CODE**: String. Two-letter country code used by Eurostat (Greece is `EL`).
* **NAME_LATN**: String. Region name in Latin script.
* **NUTS_NAME**: String. Region name in the national language and script.
* **MOUNT_TYPE**, **URBN_TYPE**, **COAST_TYPE**: Integer, or `null` where GISCO gives no value. Mountain, urban-rural and coastal typology codes.
* **NAME_ENGL**, **NAME_FREN**, **NAME_GERM**: String. Country name in English, French and German. French and German are `null` for Kosovo (`XK`) regions.
* **ISO3_CODE**: String. Three-letter ISO 3166-1 country code.
* **SVRG_UN**: String. Sovereignty status of the country (`UN Member State` or `Sovereignty unsettled`).
* **CAPT**: String. Capital of the country (`null` for Kosovo regions).
* **EU_STAT**, **EFTA_STAT**, **CC_STAT**: String, `T` or `F`. Whether the country is an EU member state, an EFTA member or an EU candidate country.

The same 17 properties are listed, with their types, in `datapackage.json`. They are the properties that GISCO publishes in these files. The script stops with an error if the files and `datapackage.json` ever disagree.

The specific administrative boundary data used in this project is provided at the `60M` scale with `RG` units, and utilizes the `EPSG:4326` coordinate reference system [EPSG:4326](https://epsg.io/4326).

## Preparation

This package includes scripts to automate data retrieval and processing.  
First, install the dependencies:

```bash
# Install libraries
pip install -r scripts/requirements.txt

# Run script
python scripts/process.py
```

# Automation

The files in `data` are rebuilt from the GISCO files by the GitHub workflow `.github/workflows/actions.yml`. It runs on the 1st of every month (and on every push to `main`, and by hand) and commits the files if they changed. GISCO publishes new files only now and then, so most runs change nothing. Last rebuild: see the date of the latest "Automated commit" in the history of `data`.

The dataset can also be found on datahub.io:
https://datahub.io/core/geo-nuts-administrative-boundaries

## License

This Data Package is licensed by its maintainers under the [Public Domain Dedication and License (PDDL)](http://opendatacommons.org/licenses/pddl/1.0/).

Refer to the [Copyright notice](http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units) of the source dataset for any specific restrictions on using these data in a public or commercial product.
