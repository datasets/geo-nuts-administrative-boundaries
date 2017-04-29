const scale = process.argv[2] || "60M",
    filename = `NUTS_2013_${scale}_SH.zip`;

const debug = require('debug')('gdal'),
    http = require('http'),
    fs = require('fs'),
    request = require('request'),
    AdmZip = require('adm-zip'),
    gdal = require('gdal'),
    shelljs = require('shelljs'),
    S = require('string'),
    out = fs.createWriteStream(filename);

// Create data directory
const dataDir = '../data';
if (!shelljs.test('-e', dataDir)) {
    shelljs.mkdir(dataDir);
}

// Declare function to transform geodata
function generateFromSQL(inputFileName, outputFileName, options) {
    // Set options
    var opts = options || { outputDriverName: 'ESRI Shapefile', outputSrsCode: 4326};
    // Open the filename
    var ds_src = gdal.open(
      inputFileName
    );
    // var driver = ds_src.driver;

    // var driver_metadata = driver.getMetadata();
    // debug(driver_metadata);
    var layer_src;
    // Get Layer or filter it
    if (opts.query) {
        layer_src = ds_src.executeSQL(opts.query);
    } else {
        layer_src = ds_src.layers.get(0);
    }
    // Get Layer SRS
    var srs_source = layer_src.srs;
    // debug(layer_src);
    // Create desired output SRS
    var srs = gdal.SpatialReference.fromEPSG(opts.outputSrsCode);
    // Create the function for SRS transformation between both SRS (input, output)
    var transformer = new gdal.CoordinateTransformation(srs_source, srs);

    // Set output driver
    var dst_driver = gdal.drivers.get(opts.outputDriverName);
    // Create output datasource using output filename
    var ds_dst = dst_driver.create(outputFileName);
    // Get type from input file to apply to output
    var outputType = gdal[gdal.Geometry.getName(layer_src.geomType)];
    // If file output, first arg name not useful
    var layer_dst = ds_dst.layers.create(layer_src.name, srs, outputType);
    debug(ds_src);
    // We retrieve the fields definition for the first feature in source
    var feature_defn_src = layer_src.features.first().defn.clone();

    // We loop to add all fields to dest layer except
    // geometry parameters like 'SHAPE_Leng' or 'SHAPE_Area'
    feature_defn_src.fields.forEach(function(field) {
        if (!S(field.name).startsWith('SHAPE_')) {
            // debug(field.name);
            layer_dst.fields.add(field);
        }
    });
    debug(layer_src.features.first().fields.getNames());

    layer_src.features.forEach(function(feat) {
        var newFeat = feat.clone();
        feat.getGeometry().transform(transformer);
        layer_dst.features.add(newFeat);
        // debug(feat.getGeometry().toJSON());
    });

    debug(layer_dst.features.count());
    // Close destination data source to write to file and avoid memory leak
    ds_dst.close();
}

let req = request({
    method: 'GET',
    uri: `http://ec.europa.eu/eurostat/cache/GISCO/geodatafiles/${filename}`,
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
        'Referer': '',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'encoding': 'null',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
});

req.pipe(out);

req.on('end', function() {
    let zip = new AdmZip(filename);
    zip.extractAllTo(/*target path*/"../data/", /*overwrite*/true);
    shelljs.rm(filename);

    let inputFileName = `../data/NUTS_2013_${scale}_SH/data/NUTS_RG_${scale}_2013.shp`;
    let query = `SELECT * FROM NUTS_RG_${scale}_2013 WHERE STAT_LEVL_ = `;

    // We create shp directory
    let shpDataDir = '../data/shp';
    if (!shelljs.test('-e', shpDataDir)) {
        shelljs.mkdir(shpDataDir);
    }
    let existingFiles = shelljs.ls(`../data/nuts_rg_${scale}_2013_lvl_*`, `../data/shp/nuts_rg_${scale}_2013_lvl_*`);
    debug(existingFiles);
    // We clean existing files
    existingFiles.forEach(function(file) {
        if (shelljs.test('-e', file)) {
            shelljs.rm(file);
        }
    });

    let levels = ['1', '2', '3'];
    levels.forEach(function(el) {
        let outputFileNameShp = `../data/shp/nuts_rg_${scale}_2013_lvl_${el}.shp`;
        generateFromSQL(inputFileName, outputFileNameShp, {
            query: query + el,
            outputDriverName: 'ESRI Shapefile',
            outputSrsCode: 4326
        });
        let outputFileNameGeoJSON = `../data/nuts_rg_${scale}_2013_lvl_${el}.geojson`;
        generateFromSQL(inputFileName, outputFileNameGeoJSON, {
            query: query + el,
            outputDriverName: 'GeoJSON',
            outputSrsCode: 4326
        });
    });
});
