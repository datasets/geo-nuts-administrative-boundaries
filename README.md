Geo Boundaries for NUTS administrative levels 1, 2 and 3 edition 2013.

If you don't know what NUTS (Nomenclature of Territorial Units for Statistics) are, see the [related Wikipedia article](https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics)

## Data

Data is taken from the [GISCO EU website](http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data).

We choose to deliver data as Shapefiles (SHP) and as GeoJSON.

SHP are in `data/shp` directory.

GeoJSON are in `data` folder

Datasets are provided for NUTS levels 1, 2 and 3.

The columns are

* **NUTS_ID**: String (5.0)
* **STAT_LEVL_**: Integer (9.0)

You will also find the original data within `data/NUTS_2013_60M_SH`.

If you need other related informations to NUTS, you can take a look at PDF file describing relationships between original tables in `data/NUTS_2013_60M_SH/NUTS_2013_60M_SH/metadata/NUTS_2013_metadata.pdf`

## Preparation

This package include the script to automate data retrieving and filtering. As we use NodeJs/Io.js, you need to install the software. Then, install dependencies with:

    cd scripts && npm install

To launch all the process, just do (default scale: `60M`):

    node index.js

Or specify scale and use the following command, where `{scale}` can be `01M`, `03M`, `10M`, `20M` or the default `60M`:

    node index.js {scale}

We choose to let a lot of comments and you may encounter some minors job unrelated code for learning purpose if you need to use [node-gdal library](https://github.com/naturalatlas/node-gdal).

## License

This Data Package is licensed by its maintainers under the [Public Domain Dedication and License (PDDL)](http://opendatacommons.org/licenses/pddl/1.0/).

Refer to the [Copyright notice](http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units) of the source dataset for any specific restrictions on using these data in a public or commercial product.