import requests
import pandas as pd
from datetime import datetime, timezone, timedelta


# --- CONFIGURATION ---
USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
DAYS_BACK = 7  # Past days
EXCLUDED_STATES = {"HI", "Hawaii"}  # Exclude Hawaii
NUMBER_EVENTS = 20000 # Large enough to capture all events in a week
MIN_MAGNITUDE = 2.5 # Below 2.5 magnitude is usually not felt by people


# --- FUNCTIONS ---
def fetch_earthquake_data(days_back=7):
    """
    Fetch earthquake data from the USGS API for the past `days_back` days.
    Returns a pandas DataFrame with relevant fields.
    """
    # Calculate date range: past 7 days using timezone-aware UTC datetimes
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days_back)

    params = {
        "format": "geojson",
        "starttime": start_time.strftime("%Y-%m-%d"),
        "endtime": end_time.strftime("%Y-%m-%d"),
        "minlatitude": 20,  # Southernmost point of continental US
        "maxlatitude": 72,  # Northernmost point of continental US
        "minlongitude": -170,    # Westernmost point of continental US
        "maxlongitude": -65, # Easternmost point of continental US
        "limit": NUMBER_EVENTS,  # Limit the results to the specified number of events
        "minmagnitude": MIN_MAGNITUDE # Limit to events with a magnitude larger than the specified minimum.
    }

    print(f"Fetching earthquake data from {params['starttime']} to {params['endtime']}...")
    response = requests.get(USGS_API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    # Parse features into DataFrame
    records = []
    for feature in data["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        records.append({
            "time": pd.to_datetime(props["time"], unit="ms"),
            "place": props["place"],
            "mag": props["mag"],
            "longitude": coords[0],
            "latitude": coords[1],
            "state": extract_state_from_place(props["place"])
        })

    df = pd.DataFrame(records)
    #Checks
    #print("DataFrame columns after creation:", df.columns)
    #print(df.head())

    if "state" not in df.columns:
        print("Error: 'state' column not found in DataFrame!")
        return df  # or handle appropriately

    # Exclude Hawaii
    df = df[~df["state"].isin(EXCLUDED_STATES)] # Min and max latitude, longtitude already exclude Hawaii
    #print("Columns:", df.columns)
    #print(df.head())
    return df

def extract_state_from_place(place):
    """
    Extract the state abbreviation or name from the USGS 'place' string.
    Returns state abbreviation (e.g., 'CA', 'AK', etc.) or None if not found.
    """
    if not place or not isinstance(place, str):
        return None
    # USGS place strings often end with ', XX' where XX is the state abbreviation
    if ',' in place:
        state = place.split(',')[-1].strip()
        if len(state) == 2 and state.isupper():
            return state
        return state  # Sometimes full state name
    return None


# --- CHECK ---
# Download csv to check data structure
# def export_earthquake_data_to_csv(df, filename="earthquake_data.csv"):
#     """
#     Export earthquake data to CSV file.
#     """
#     try:
#         df.to_csv(filename, index=False)
#         print(f"Earthquake data exported to {filename}")
#     except Exception as e:
#         print(f"Error exporting earthquake data: {e}")
# export_earthquake_data_to_csv(fetch_earthquake_data(DAYS_BACK), "earthquake_data.csv")


if __name__ == "__main__":
    # Step 1: Fetch earthquake data
    df_quakes = fetch_earthquake_data(DAYS_BACK)
    print(f"Fetched {len(df_quakes)} earthquakes in the past {DAYS_BACK} days (excluding Hawaii).\n")
    print(df_quakes.head())  # Show a preview

    # Step 2: Aggregate earthquake statistics by state
    state_stats = (
        df_quakes.groupby("state")
        .agg(count=("mag", "count"), max_magnitude=("mag", "max"))
        .sort_values(by="count", ascending=False)
    )
    print(f"Earthquake statistics by state past {DAYS_BACK} days:\n")
    print(state_stats)

    # Highlight the state with the most earthquakes
    if not state_stats.empty:
        top_state = state_stats.index[0]
        top_count = state_stats.iloc[0]["count"]
        print(f"\nState with the most earthquakes: {top_state} ({top_count} events)")
    else:
        print("No earthquake data available.")

    # Step 3: Define client locations (Table 1)
    CLIENT_LOCATIONS = [
        {   "building": "West Anchorage High School",
            "city": "Anchorage",
            "state": "Alaska",
            "address": "1700 Hillcrest Dr, Anchorage, AK 99517"
        },
        {   "building": "City Hall",
            "city": "San Francisco",
            "state": "CA",
            "address": "1 Dr Carlton B Goodlett Pl, San Francisco, CA 94102"
        },
        {   "building": "Los Angeles Memorial Coliseum",
            "city": "Los Angeles",
            "state": "CA",
            "address": "3911 S Figueroa St, Los Angeles, CA 90037"
        },
        {   "building": "Harrah's Reno (Former)",
            "city": "Reno",
            "state": "Nevada",
            "address": "219 N Center St, Reno, NV 89501"
        },
        {   "building": "Benson Polytechnic High School",
            "city": "Portland",
            "state": "Oregon",
            "address": "546 NE 12th Ave, Portland, OR 97232"
        },
        {   "building": "Salt Lake Temple",
            "city": "Salt Lake City",
            "state": "Utah",
            "address": "50 N Temple, Salt Lake City, UT 84150"
        },
        {   "building": "Challis High School",
            "city": "Challis",
            "state": "Idaho",
            "address": "1 Schoolhouse Rd, Challis, ID 83226"
        }
    ]

    # Step 4: Assess earthquake risk for each client location
    print("\nEarthquake risk assessment for client locations:")
    for loc in CLIENT_LOCATIONS:
        state = loc["state"]
        stats = state_stats.loc[state] if state in state_stats.index else None
        if stats is not None:
            count = stats["count"]
            max_mag = stats["max_magnitude"]
            # Simple risk indicator based on count and magnitude
            # (Shortcut: High if >10 quakes or max magnitude >=5.0, Moderate if >5 quakes or max magnitude >=3.0, else Low)
            if count > 10 or (max_mag and max_mag >= 5.0):
                risk = "High"
            elif count > 5 or (max_mag and max_mag >= 3.0):
                risk = "Moderate"
            else:
                risk = "Low"
            print(f"- {loc['building']} ({loc['city']}, {state}): {risk} risk | Earthquakes: {count}, Max Magnitude: {max_mag}")
        else:
            print(f"- {loc['building']} ({loc['city']}, {state}): No recent earthquake data available.")



