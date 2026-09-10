import os
import sys
import requests
import folium

BASE_URL = "https://api.search.brave.com/res/v1/local"


def get_api_key() -> str:
    """Reads the API key from the environment — same pattern as brave_demo.py.
    Never hardcode the key into this file."""
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        print("Error: BRAVE_API_KEY environment variable not set.")
        sys.exit(1)
    return api_key


def fetch_place_ids(api_key: str, query: str, location: str, radius: int = 5000, count: int = 10) -> list:
    """Step 1: Search for places. This returns lightweight results —
    mainly an id and a title per place, not full details yet."""
    url = f"{BASE_URL}/place_search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key,
    }
    params = {"q": query, "location": location, "radius": radius, "count": count}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])
    print(f"Found {len(results)} place(s) for '{query}' near '{location}'.")
    return [r["id"] for r in results if "id" in r]


def fetch_place_details(api_key: str, place_ids: list) -> list:
    """Step 2: Enrich place IDs with full details (address, coordinates,
    rating, etc.) via the /local/pois endpoint. Batches up to 20 IDs per call."""
    if not place_ids:
        return []

    url = f"{BASE_URL}/pois"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key,
    }
    # The API expects repeated `ids` query params: ids=X&ids=Y&ids=Z
    params = [("ids", pid) for pid in place_ids[:20]]

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])


def extract_coordinates(place: dict):
    """CONFIRMED against a real API response (Sep 2026): Brave returns
    coordinates as a plain two-item list: "coordinates": [lat, lon] —
    not a named field. That's the first pattern checked below. The other
    patterns are kept as fallbacks in case a different endpoint or place
    type ever returns a different shape."""
    coords = place.get("coordinates")
    if isinstance(coords, (list, tuple)) and len(coords) == 2:
        try:
            return float(coords[0]), float(coords[1])
        except (TypeError, ValueError):
            pass

    candidates = [
        lambda p: (p.get("latitude"), p.get("longitude")),
        lambda p: (p.get("location", {}).get("lat"), p.get("location", {}).get("lng")),
        lambda p: (p.get("lat"), p.get("lon")),
    ]
    for extract in candidates:
        try:
            lat, lon = extract(place)
            if lat is not None and lon is not None:
                return float(lat), float(lon)
        except (AttributeError, TypeError, ValueError):
            continue
    return None


def build_map(places: list, center_lat: float, center_lon: float, output_file: str = "brave_places_map.html"):
    """Step 3: Plot the enriched places on an interactive map.
    Brave gives us the data; folium (wrapping Leaflet.js + OpenStreetMap
    tiles) is what actually draws it — Brave doesn't provide map tiles itself."""
    place_map = folium.Map(location=[center_lat, center_lon], zoom_start=14)

    plotted = 0
    for place in places:
        coords = extract_coordinates(place)
        name = place.get("title") or place.get("name") or "Unknown place"
        if coords is None:
            print(f"  Skipped '{name}' — no coordinates found in response (see extract_coordinates()).")
            continue
        lat, lon = coords

        # Confirmed present in real responses: postal_address and contact.telephone.
        # Build a richer popup if they're there; fall back to just the name if not.
        address = place.get("postal_address", {}).get("displayAddress", "")
        phone = place.get("contact", {}).get("telephone", "")
        popup_lines = [f"<b>{name}</b>"]
        if address:
            popup_lines.append(address)
        if phone:
            popup_lines.append(phone)
        popup_html = "<br>".join(popup_lines)

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=name,
        ).add_to(place_map)
        plotted += 1

    place_map.save(output_file)
    print(f"Plotted {plotted} of {len(places)} place(s). Map saved to: {output_file}")


def main():
    debug = "--debug" in sys.argv
    api_key = get_api_key()

    query = "coffee shops"
    location = "timnath colorado"
    center_lat, center_lon = 40.5291, -104.9853  # Timnath, CO — verified coordinates

    try:
        place_ids = fetch_place_ids(api_key, query, location)
        if not place_ids:
            print("No places found — try a broader query or a larger radius.")
            return

        details = fetch_place_details(api_key, place_ids)

        if debug and details:
            import json
            print("\n--- RAW FIRST RESULT (--debug) ---")
            print(json.dumps(details[0], indent=2))
            print("--- END RAW RESULT ---\n")

        build_map(details, center_lat, center_lon)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


if __name__ == "__main__":
    main()