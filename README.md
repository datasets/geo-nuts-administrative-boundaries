<a className="gh-badge" href="https://datahub.io/core/geo-nuts-administrative-boundaries"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

# Geo Boundaries for NUTS administrative levels 1, 2 and 3

Boundaries of the European NUTS regions (Nomenclature of Territorial Units for Statistics) at levels 1, 2 and 3, as GeoJSON polygons, taken from Eurostat GISCO. If you don't know what NUTS are, see the [related Wikipedia article][wiki-nuts].

Column definitions and types are in `datapackage.json`.

## Data

There is one file for each NUTS level in the `data` folder. The NUTS edition (the year) is part of the file name.

| File | Content |
|---|---|
| `data/NUTS_RG_60M_<year>_4326_LEVL_1.geojson` | NUTS level 1 regions |
| `data/NUTS_RG_60M_<year>_4326_LEVL_2.geojson` | NUTS level 2 regions |
| `data/NUTS_RG_60M_<year>_4326_LEVL_3.geojson` | NUTS level 3 regions |

In the file names, `60M` is the map scale (1:60 million, the coarsest GISCO scale), `RG` means region polygons, and `4326` is the coordinate reference system, [EPSG:4326][epsg] (longitude and latitude in degrees).

Each file is a GeoJSON `FeatureCollection`. Each feature is one region, as a `MultiPolygon`, with these properties:

| Property | Meaning |
|---|---|
| `NUTS_ID` | String. NUTS code of the region, for example `DE212`. Unique in each file |
| `LEVL_CODE` | Integer. NUTS level: 1, 2 or 3 |
| `CNTR_CODE` | String. Two-letter country code used by Eurostat. Greece is `EL` |
| `NAME_LATN` | String. Region name in Latin script |
| `NUTS_NAME` | String. Region name in the national language and script, for example Greek |
| `MOUNT_TYPE`, `URBN_TYPE`, `COAST_TYPE` | Integer, or `null` where GISCO gives no value. Mountain, urban-rural and coastal typology codes |
| `NAME_ENGL`, `NAME_FREN`, `NAME_GERM` | String. Country name in English, French and German |
| `ISO3_CODE` | String. Three-letter ISO 3166-1 country code |
| `SVRG_UN` | String. Sovereignty status of the country: `UN Member State` or `Sovereignty unsettled` |
| `CAPT` | String. Capital of the country |
| `EU_STAT`, `EFTA_STAT`, `CC_STAT` | String, `T` or `F`. Whether the country is an EU member state, an EFTA member or an EU candidate country |

The country properties (`NAME_*`, `ISO3_CODE`, `SVRG_UN`, `CAPT` and the three `*_STAT` flags) are repeated on every region of the country. They are the properties that GISCO publishes in these files. The build script stops with an error if the files and `datapackage.json` ever disagree.

### Known limitations

* **Use is restricted.** GISCO allows these data to be used for non-commercial purposes only, and requires the credit "© EuroGeographics for the administrative boundaries" on any publication that uses them. See License.
* `MOUNT_TYPE`, `URBN_TYPE` and `COAST_TYPE` are `null` for some regions outside the EU (for example Türkiye and Serbia).
* `NAME_FREN`, `NAME_GERM` and `CAPT` are `null` for Kosovo (`XK`) regions.
* Some `NUTS_NAME` values end with a space (for example `EL3`). Trim them before you compare names.
* Not every country has every level. For example, Bosnia and Herzegovina (`BA`) has regions at levels 1 and 2 only.
* The 1:60 million scale is coarse. It suits maps of Europe, not maps of a single region or city.
* GISCO's release notes say that the boundaries of Türkiye were made using OpenStreetMap data. See License.
* The files have no `crs` member (the script removes it). Coordinates are always EPSG:4326.

## Data sources

* [Eurostat GISCO][gisco-nuts], the territorial units for statistics (NUTS) boundaries, downloaded from the [GISCO distribution service][gisco-dist]: the polygons and all properties. Licence: restricted. Non-commercial use only, with a required credit (see [License](#license)).
* Boundaries of Türkiye: GISCO's release notes say they were made using [OpenStreetMap][osm] data. Licence: unclear for this repo (see [License](#license)).

Changes made to the source data: the three GeoJSON files (NUTS levels 1, 2 and 3, scale 60M, EPSG:4326, region polygons) are downloaded from GISCO and republished with one change: the top-level `crs` member is removed. All features and properties are otherwise unchanged. The script checks that the properties in the files match the fields listed in `datapackage.json`.

Not endorsed by, or affiliated with, Eurostat, the European Commission or EuroGeographics.

[wiki-nuts]: https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics
[epsg]: https://epsg.io/4326
[gisco-nuts]: https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units/territorial-units-statistics
[gisco-dist]: https://gisco-services.ec.europa.eu/distribution/v2/nuts/
[osm]: https://www.openstreetmap.org/copyright

## Preparation

The script needs Python 3, `requests` and `beautifulsoup4`. To rebuild the files in `data`:

```bash
# Install libraries
pip install -r scripts/requirements.txt

# Download the latest files and update the data
python scripts/process.py
```

The script reads the [GISCO distribution service][gisco-dist], finds the latest NUTS edition, and downloads the level 1, 2 and 3 files (60M, EPSG:4326, region polygons). It writes them to `data` only if all three downloads worked, and updates the file names, paths and sizes in `datapackage.json`.

A GitHub workflow (`.github/workflows/actions.yml`) runs the script on the 1st of every month (and on pushes to `main` and on manual runs) and commits the files if they changed. GISCO publishes new files only now and then, so most runs change nothing.

The dataset can also be found on [datahub.io](https://datahub.io/core/geo-nuts-administrative-boundaries).

## License

The boundary data is not free for every use. GISCO's copyright information for its statistical units (which include NUTS) says:

> "The permission to use the data is granted on condition that: the data will not be used for commercial purposes; the source will be acknowledged."

It asks for this notice, in the legend of any map and in the introductory page of any publication that uses the data:

> "© EuroGeographics for the administrative boundaries"

It also says: "If you intend to use the data commercially, please contact EuroGeographics for information about their licence agreements." (Source: [GISCO, statistical units][gisco-copyright].) Eurostat's general [copyright notice][eurostat-copyright] allows commercial reuse of its own data, but says the general rules "can be subject to conditions which may be specified in individual copyright notices". The GISCO notice above is such a condition.

What we could not establish:

* The EuroGeographics licence agreements themselves. GISCO's metadata points to a "License conditions for EuroGeographics Administrative and Topographic spatial datasets" page. It needs an EU Login, so we could not read it.
* What licence applies to the Türkiye boundaries that GISCO says were made using OpenStreetMap data. OpenStreetMap data is under the Open Database Licence (ODbL), which has its own credit and share-alike rules. We could not find how GISCO treats this.

The maintainers place only their own work (the download script, the file layout and the descriptor) under the [Public Domain Dedication and License (PDDL)][pddl]. This does not cover the boundary data. See also [ATTRIBUTION.txt](ATTRIBUTION.txt).

[gisco-copyright]: https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units
[eurostat-copyright]: https://ec.europa.eu/eurostat/web/main/help/copyright-notice
[pddl]: https://opendatacommons.org/licenses/pddl/1.0/
