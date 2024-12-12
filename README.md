<a className="gh-badge" href="https://datahub.io/core/geo-nuts-administrative-boundaries"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

# Geo Boundaries for NUTS administrative levels 1, 2 and 3

If you don't know what NUTS (Nomenclature of Territorial Units for Statistics) are, see the [related Wikipedia article](https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics).

## Data

Data is sourced from the [GISCO EU website](https://gisco-services.ec.europa.eu/distribution/v2/nuts/).

We provide data as GeoJSON. Data is stored in the `data` folder.

Datasets are available for NUTS levels 1, 2, and 3.

The columns are:

* **NUTS_ID**: String (5.0)
* **STAT_LEVL_**: Integer (9.0)

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
Up-to-date (auto-updates every year) geo-nuts-administartive-boundaries dataset could be found on the datahub.io:
https://datahub.io/core/geo-nuts-administartive-boundaries 

## License

This Data Package is licensed by its maintainers under the [Public Domain Dedication and License (PDDL)](http://opendatacommons.org/licenses/pddl/1.0/).

Refer to the [Copyright notice](http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units) of the source dataset for any specific restrictions on using these data in a public or commercial product.
