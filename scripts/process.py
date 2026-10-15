import os
import re
import json
import requests
from bs4 import BeautifulSoup

url = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/"
format_ESPG = "4326"
scale = "60M"
unit = "RG"
timeout = 120  # seconds, for every request


def resource_name(filename):
    # Frictionless only accepts names made of lower-case letters, digits and . _ - /
    # "NUTS_RG_60M_2024_4326_LEVL_1.geojson" -> "nuts-rg-60m-2024-4326-levl-1"
    name = re.sub(r"[^a-z0-9]+", "-", filename.split(".")[0].lower()).strip("-")
    if not re.fullmatch(r"[-a-z0-9._/]+", name):
        raise ValueError(f"Invalid resource name {name!r} made from {filename!r}")
    return name


def update_datapackage(list_of_geojson):
    with open("datapackage.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if len(data["resources"]) != len(list_of_geojson):
        raise SystemExit(
            f"datapackage.json has {len(data['resources'])} resources "
            f"but {len(list_of_geojson)} files were downloaded"
        )
    for resource, elem in zip(data["resources"], list_of_geojson):
        resource["name"] = resource_name(elem)
        resource["path"] = "data/" + elem
        resource["bytes"] = os.path.getsize("data/" + elem)
        # The descriptor must describe the properties that are in the file.
        with open("data/" + elem, "r", encoding="utf-8") as f:
            features = json.load(f)["features"]
        expected = [field["name"] for field in resource["schema"]["fields"]]
        found = {key for feature in features for key in feature["properties"]}
        if found != set(expected):
            raise SystemExit(
                f"{elem}: properties in the file {sorted(found)} "
                f"differ from the fields in datapackage.json {sorted(expected)}. "
                "Update the schema in datapackage.json and the README."
            )
    with open("datapackage.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("datapackage.json has been updated")


def run():
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    a_tags = soup.find_all("a")
    latest_tag = ""
    for a in a_tags:
        href = a.get("href") or ""
        if "files" in href:
            latest_tag = str(href)
            break
    if not latest_tag:
        raise SystemExit(f"No link to a files page found at {url}")
    print(f"Latest tag found: {latest_tag}")

    response_2 = requests.get(url + latest_tag, timeout=timeout)
    response_2.raise_for_status()
    soup_2 = BeautifulSoup(response_2.text, "html.parser")
    li_tags = soup_2.find_all("li")
    list_of_geojson = []
    for elem in li_tags:
        if (
            scale in elem.text
            and format_ESPG in elem.text
            and unit in elem.text
            and (
                elem.text.endswith("_1.geojson")
                or elem.text.endswith("_2.geojson")
                or elem.text.endswith("_3.geojson")
            )
        ):
            a_tag = elem.find("a")
            get_href = a_tag.get("href") if a_tag else None
            if get_href:
                list_of_geojson.append(get_href)
    list_of_geojson.sort()  # _1, _2, _3: the order of the resources in datapackage.json
    print(f"GeoJSON files to download: {list_of_geojson}")
    if len(list_of_geojson) != 3:
        raise SystemExit(
            f"Expected 3 GeoJSON files (NUTS levels 1, 2, 3) at {url + latest_tag}, "
            f"found {len(list_of_geojson)}"
        )

    # Download everything first, write only when all three downloads worked.
    payloads = {}
    for geojson in list_of_geojson:
        response_3 = requests.get(url + geojson, timeout=timeout)
        response_3.raise_for_status()
        payload = response_3.json()
        payload.pop("crs", None)
        if payload.get("type") != "FeatureCollection" or not payload.get("features"):
            raise SystemExit(f"{geojson} is not a non-empty FeatureCollection")
        payloads[geojson.split("/")[1]] = payload
        print(f"{geojson} has been downloaded")

    os.makedirs("data", exist_ok=True)
    for filename, payload in payloads.items():
        with open("data/" + filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
            f.write("\n")
    return list(payloads)


if __name__ == "__main__":
    list_of_geojson = run()
    update_datapackage(list_of_geojson)
