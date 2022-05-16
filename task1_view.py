import json
from pyjsonviewer import view_data


def view(final_data, max_depth):
    data_to_view = {}
    for data in final_data["items"]:
        if data["domain"] == "openx.com":
            data_to_view[data["domain"]] = {
                "domain": data["domain"], "contractors": data["contractors"],
                "maximum_depth": max_depth}
        elif data["contractors"] == []:
            data_to_view[data["domain"]] = {
                "domain": data["domain"],  "seller_type": "direct"}
        else:
            data_to_view[data["domain"]] = {
                "domain": data["domain"], "contractors": data["contractors"],
                "seller_type": "indirect"}

    view_data(json_data=data_to_view)


if __name__ == "__main__":
    with open("maxdepth.txt", "r") as file:
        max_depth = file.read()
    final_data = json.load(open('finaldata.json'))
    view(final_data, max_depth)
