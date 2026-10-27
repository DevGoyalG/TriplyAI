import os
import re
import certifi
import airportsdata
import pycountry
import requests

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure SSL certificates for secure API requests
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# Load Aviationstack API configuration
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

# Default origin when user says only destination, e.g. "Japan trip"
# Change this if your default location is not India/Delhi.
DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "DEL").strip().upper()

BASE_URL = "https://api.aviationstack.com/v1/flights"

# Load airport information using IATA codes
AIRPORTS = airportsdata.load("IATA")


# Map common country names and aliases to ISO alpha-2 country codes
COUNTRY_ALIASES = {
    "america": "US",
    "australia": "AU",
    "bangladesh": "BD",
    "britain": "GB",
    "canada": "CA",
    "china": "CN",
    "england": "GB",
    "france": "FR",
    "germany": "DE",
    "india": "IN",
    "indonesia": "ID",
    "italy": "IT",
    "japan": "JP",
    "korea": "KR",
    "malaysia": "MY",
    "nepal": "NP",
    "qatar": "QA",
    "russia": "RU",
    "saudi arabia": "SA",
    "singapore": "SG",
    "south korea": "KR",
    "spain": "ES",
    "thailand": "TH",
    "turkey": "TR",
    "uae": "AE",
    "u.k.": "GB",
    "u.s.": "US",
    "u.s.a": "US",
    "uk": "GB",
    "united states": "US",
    "vietnam": "VN",
}


# Preferred main airport for each country, sorted alphabetically by country code
COUNTRY_MAIN_AIRPORT = {
    "AE": "DXB",  # United Arab Emirates
    "AU": "SYD",  # Australia
    "BD": "DAC",  # Bangladesh
    "CA": "YYZ",  # Canada
    "CN": "PEK",  # China
    "DE": "FRA",  # Germany
    "ES": "MAD",  # Spain
    "FR": "CDG",  # France
    "GB": "LHR",  # United Kingdom
    "ID": "CGK",  # Indonesia
    "IN": "DEL",  # India
    "IT": "FCO",  # Italy
    "JP": "NRT",  # Japan
    "KR": "ICN",  # South Korea
    "MY": "KUL",  # Malaysia
    "NP": "KTM",  # Nepal
    "QA": "DOH",  # Qatar
    "RU": "SVO",  # Russia
    "SA": "JED",  # Saudi Arabia
    "SG": "SIN",  # Singapore
    "TH": "BKK",  # Thailand
    "TR": "IST",  # Turkey
    "US": "JFK",  # United States
}

# Map city names to their preferred airports, sorted alphabetically
CITY_MAIN_AIRPORT = {
    "bangalore": "BLR",
    "bangkok": "BKK",
    "bengaluru": "BLR",
    "chennai": "MAA",
    "delhi": "DEL",
    "dhaka": "DAC",
    "doha": "DOH",
    "dubai": "DXB",
    "frankfurt": "FRA",
    "istanbul": "IST",
    "kuala lumpur": "KUL",
    "kolkata": "CCU",
    "kyoto": "KIX",
    "london": "LHR",
    "madrid": "MAD",
    "mumbai": "BOM",
    "new delhi": "DEL",
    "new york": "JFK",
    "osaka": "KIX",
    "paris": "CDG",
    "rome": "FCO",
    "singapore": "SIN",
    "sydney": "SYD",
    "tokyo": "NRT",
    "toronto": "YYZ",
}


def clean_text(text: str) -> str:
    """
    Normalize user input by removing special characters, extra spaces,
    and common travel-related stop words for easier text matching.
    """

    # Convert text to lowercase and remove leading/trailing spaces
    text = text.lower().strip()

    # Remove special characters and normalize multiple spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    # Remove common travel-related words that add little search value
    stop_words = [
        "flight", "flights", "ticket", "tickets", "trip", "travel",
        "plan", "complete", "days", "day", "including", "hotel",
        "hotels", "sightseeing", "under", "budget", "info", "information"
    ]

    # Keep only meaningful words for downstream matching
    words = [w for w in text.split() if w not in stop_words]

    return " ".join(words).strip()


def country_name_to_code(text: str):
    """
    Convert a country name or alias into its ISO alpha-2 country code.
    """

    text = clean_text(text)

    # Match directly against predefined country aliases
    if text in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[text]

    # Resolve country names using the pycountry library
    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2
    except LookupError:
        pass

    # Detect a country name within a longer text
    for country in pycountry.countries:
        country_name = country.name.lower()
        if country_name in text:
            return country.alpha_2

    # Match predefined aliases within a longer text
    for alias, code in COUNTRY_ALIASES.items():
        if alias in text:
            return code

    # Return None when no country match is found
    return None


def airport_country_matches(airport: dict, country_code: str) -> bool:
    """
    Check whether an airport belongs to the specified country using its ISO alpha-2 code or country name.
    """

    # Normalize the airport's country value for comparison
    airport_country = str(airport.get("country", "")).upper().strip()

    # Match directly against the country code
    if airport_country == country_code:
        return True

    # Resolve the country code to its official country name
    try:
        country = pycountry.countries.get(alpha_2=country_code)

        # Match the airport's country name against the official name
        if country and airport_country.lower() == country.name.lower():
            return True
    except Exception:
        pass

    # Return False if the airport does not match the specified country
    return False


def get_best_airport_for_country(country_code: str):
    """
    Return the preferred airport for a country, or select the best available alternative.
    """

    # Return the predefined main airport if it exists in the airport dataset
    preferred = COUNTRY_MAIN_AIRPORT.get(country_code)

    if preferred and preferred in AIRPORTS:
        return preferred

    # Collect alternative airports matching the specified country
    candidates = []

    for iata, airport in AIRPORTS.items():
        # Skip entries without an IATA code
        if not iata:
            continue

        # Consider only airports belonging to the requested country
        if airport_country_matches(airport, country_code):
            name = str(airport.get("name", "")).lower()
            city = str(airport.get("city", "")).lower()

            # Assign scores to prioritize likely major airports
            score = 0

            if "international" in name:
                score += 50
            if "intl" in name:
                score += 40
            if "capital" in name:
                score += 20
            if city:
                score += 5

            # Store each candidate with its score for ranking
            candidates.append((score, iata))

    # Return None if no matching airports are found
    if not candidates:
        return None

    # Rank candidates by score and return the highest-scoring airport code
    candidates.sort(reverse=True)
    return candidates[0][1]


def resolve_location_to_iata(location: str):
    """
    Converts country/city/airport/IATA into IATA code.

    Examples:
    Bangladesh -> DAC
    Japan -> NRT
    Dhaka -> DAC
    Tokyo -> NRT
    DAC -> DAC
    """

    if not location:
        return None

    raw_location = location.strip()

    # Direct IATA code
    if re.fullmatch(r"[A-Za-z]{3}", raw_location):
        code = raw_location.upper()
        if code in AIRPORTS:
            return code

    location_clean = clean_text(raw_location)

    if not location_clean:
        return None

    # City preferred airport
    if location_clean in CITY_MAIN_AIRPORT:
        return CITY_MAIN_AIRPORT[location_clean]

    # Country preferred airport
    country_code = country_name_to_code(location_clean)
    if country_code:
        airport = get_best_airport_for_country(country_code)
        if airport:
            return airport

    # Exact city match from airport database
    city_matches = []

    for iata, airport in AIRPORTS.items():
        city = str(airport.get("city", "")).lower().strip()
        name = str(airport.get("name", "")).lower().strip()

        score = 0

        if city == location_clean:
            score += 100
        elif location_clean in city:
            score += 70

        if location_clean in name:
            score += 50

        if "international" in name:
            score += 10

        if score > 0:
            city_matches.append((score, iata))

    if city_matches:
        city_matches.sort(reverse=True)
        return city_matches[0][1]

    return None


def find_location_mentions(query: str):
    """
    Finds country or city names inside a natural language query.
    """

    q = query.lower()
    mentions = []

    # Country aliases
    for alias in COUNTRY_ALIASES:
        if re.search(rf"\b{re.escape(alias)}\b", q):
            mentions.append(alias)

    # Country names from pycountry
    for country in pycountry.countries:
        name = country.name.lower()
        if len(name) >= 4 and re.search(rf"\b{re.escape(name)}\b", q):
            mentions.append(name)

    # City names from our preferred city map
    for city in CITY_MAIN_AIRPORT:
        if re.search(rf"\b{re.escape(city)}\b", q):
            mentions.append(city)

    # Remove duplicate while keeping order
    unique_mentions = []
    for item in mentions:
        if item not in unique_mentions:
            unique_mentions.append(item)

    return unique_mentions


def parse_route(query: str):
    """
    Returns:
    dep_iata, arr_iata

    Can return:
    None, None  -> global live flights
    DAC, NRT    -> filtered route
    DAC, None   -> all flights from DAC
    None, NRT   -> all flights to NRT
    """

    q = query.strip()
    q_lower = q.lower()

    # Global / all-country query
    global_keywords = [
        "all country",
        "all countries",
        "global flight",
        "global flights",
        "all flight",
        "all flights",
        "worldwide flight",
        "worldwide flights",
    ]

    if any(keyword in q_lower for keyword in global_keywords):
        return None, None

    # Direct IATA code route: DAC to NRT
    codes = re.findall(r"\b[A-Z]{3}\b", q)

    if len(codes) >= 2:
        dep = codes[0].upper()
        arr = codes[1].upper()
        return dep, arr

    # Pattern: from X to Y
    match = re.search(
        r"\bfrom\s+(.+?)\s+\bto\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
        q_lower,
    )

    if match:
        origin_text = match.group(1)
        dest_text = match.group(2)

        dep_iata = resolve_location_to_iata(origin_text)
        arr_iata = resolve_location_to_iata(dest_text)

        return dep_iata, arr_iata

    # Pattern: to Y from X
    match = re.search(
        r"\bto\s+(.+?)\s+\bfrom\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
        q_lower,
    )

    if match:
        dest_text = match.group(1)
        origin_text = match.group(2)

        dep_iata = resolve_location_to_iata(origin_text)
        arr_iata = resolve_location_to_iata(dest_text)

        return dep_iata, arr_iata

    # Pattern: flights from X
    match = re.search(r"\bfrom\s+(.+?)(?:[.!?]|$)", q_lower)

    if match:
        origin_text = match.group(1)
        dep_iata = resolve_location_to_iata(origin_text)
        return dep_iata, None

    # Pattern: flights to X
    match = re.search(r"\bto\s+(.+?)(?:[.!?]|$)", q_lower)

    if match:
        dest_text = match.group(1)
        arr_iata = resolve_location_to_iata(dest_text)
        return None, arr_iata

    # Fallback: find country/city mentions
    mentions = find_location_mentions(q)

    if len(mentions) >= 2:
        dep_iata = resolve_location_to_iata(mentions[0])
        arr_iata = resolve_location_to_iata(mentions[1])
        return dep_iata, arr_iata

    if len(mentions) == 1:
        arr_iata = resolve_location_to_iata(mentions[0])
        return DEFAULT_ORIGIN_IATA, arr_iata

    return None, None


def format_flight(flight: dict):
    """
    Format flight details into a readable structure with departure, arrival, and delay information.
    """

    # Extract airline, flight number, and current flight status
    airline = flight.get("airline", {}).get("name") or "Unknown airline"
    flight_number = flight.get("flight", {}).get("iata") or "Unknown flight number"
    status = flight.get("flight_status") or "Unknown"

    # Extract departure and arrival details safely
    dep = flight.get("departure", {}) or {}
    arr = flight.get("arrival", {}) or {}

    # Extract departure airport, terminal, gate, and scheduled time
    dep_airport = dep.get("airport") or "Unknown departure airport"
    dep_iata = dep.get("iata") or "Unknown"
    dep_terminal = dep.get("terminal") or "N/A"
    dep_gate = dep.get("gate") or "N/A"
    dep_scheduled = dep.get("scheduled") or "Unknown"

    # Format departure delay when available
    dep_delay = dep.get("delay")
    dep_delay_text = f"{dep_delay} minutes" if dep_delay is not None else "N/A"

    # Extract arrival airport, terminal, gate, and scheduled time
    arr_airport = arr.get("airport") or "Unknown arrival airport"
    arr_iata = arr.get("iata") or "Unknown"
    arr_terminal = arr.get("terminal") or "N/A"
    arr_gate = arr.get("gate") or "N/A"
    arr_scheduled = arr.get("scheduled") or "Unknown"

    # Format arrival delay when available
    arr_delay = arr.get("delay")
    arr_delay_text = f"{arr_delay} minutes" if arr_delay is not None else "N/A"

    # Return the formatted flight details as a readable multiline string
    return f"""
Airline: {airline}
Flight: {flight_number}
Status: {status}

Departure:
- Airport: {dep_airport}
- IATA: {dep_iata}
- Terminal: {dep_terminal}
- Gate: {dep_gate}
- Scheduled: {dep_scheduled}
- Delay: {dep_delay_text}

Arrival:
- Airport: {arr_airport}
- IATA: {arr_iata}
- Terminal: {arr_terminal}
- Gate: {arr_gate}
- Scheduled: {arr_scheduled}
- Delay: {arr_delay_text}
""".strip()


def search_flights(query: str, limit: int = 10):
    """
    Search for flights using the Aviationstack API and return formatted flight details.
    """

    # Validate that the Aviationstack API key is configured
    if not API_KEY:
        return (
            "Flight API error: AVIATIONSTACK_API_KEY is missing.\n"
            "Please add this in your .env file:\n"
            "AVIATIONSTACK_API_KEY=your_api_key_here"
        )

    # Extract departure and arrival airport codes from
    dep_iata, arr_iata = parse_route(query)

    # Prepare API request parameters with a maximum of 100 results
    params = {
        "access_key": API_KEY,
        "limit": min(limit, 100),
    }

    # Add departure and arrival filters when available
    if dep_iata:
        params["dep_iata"] = dep_iata

    if arr_iata:
        params["arr_iata"] = arr_iata

    # Send the API request and handle network or JSON parsing errors
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Flight API request failed: {e}"
    except ValueError:
        return "Flight API returned invalid JSON."

    # Handle errors returned by the Aviationstack API
    if "error" in data:
        error = data["error"]
        return (
            "Flight API error:\n"
            f"Code: {error.get('code', 'Unknown')}\n"
            f"Message: {error.get('message', 'Unknown error')}"
        )

    # Extract flight records from the API response
    flight_data = data.get("data", [])

    # Return a helpful message when no flight records are available
    if not flight_data:
        route_text = ""

        if dep_iata and arr_iata:
            route_text = f" for route {dep_iata} to {arr_iata}"
        elif dep_iata:
            route_text = f" from {dep_iata}"
        elif arr_iata:
            route_text = f" to {arr_iata}"

        return (
            f"No live flight data found{route_text}.\n\n"
            "Note: AviationStack provides live/status flight data, not ticket prices. "
            "For actual fare prices, use a flight-pricing API such as Amadeus."
        )

    # Describe the route covered by the search results
    route_info = "Global live flights"

    if dep_iata and arr_iata:
        route_info = f"Live flights from {dep_iata} to {arr_iata}"
    elif dep_iata:
        route_info = f"Live flights from {dep_iata}"
    elif arr_iata:
        route_info = f"Live flights to {arr_iata}"

    # Format flight records and limit the number returned to the caller
    formatted_flights = [format_flight(flight) for flight in flight_data[:limit]]

    # Combine route information and formatted flight details into one response
    return f"{route_info}\n\n" + "\n\n---\n\n".join(formatted_flights)


if __name__ == "__main__":
    # Test flight search for a Japan trip originating from India
    print(search_flights("Plan a 7 days Japan trip from India"))

    # Print a separator between test cases
    print("\n" + "=" * 80 + "\n")

    # Test flight search without a specific departure or destination
    print(search_flights("all country flight info"))