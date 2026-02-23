import csv
def average_gdp(files):
    country_gdp = {}

    for file in files:
        with open(file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                country = row["country"]
                gdp = float(row["gdp"])
                country_gdp.setdefault(country, []).append(gdp)

    result = []
    for country, values in country_gdp.items():
        avg = round(sum(values) / len(values), 2)
        result.append([country, avg])

    result.sort(key=lambda x: x[1], reverse=True)
    return result


REPORTS = {
    "average-gdp": average_gdp,
}