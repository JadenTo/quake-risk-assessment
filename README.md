# Earthquake Risk Assessment

## Project Overview

  The program fetches earthquake data from the USGS Earthquake API for desired historical period, 
  aggregates statistics by state, and provides risk assessments for specific 
  client locations.

## Features

- Fetches earthquake data from USGS API (excluding Hawaii by default)
- Aggregates earthquake statistics by state (count, max magnitude)
- Assesses risk levels for client locations
- Exports raw earthquake data to CSV if needed


## Requirements

- Python 3.8+
- Internet connection (for API access)

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   

## Usage

1. Run the main program:
   ```bash
   python main.py
   ```

2. The program will:
     - Fetch earthquake data from the desired past days
     - Display earthquake statistics by state
     - Show risk assessment for client locations
     - Export raw data to CSV if needed

## Output

### Console Output
- Number of earthquakes fetched
- Earthquake statistics by state
- State with the most earthquakes
- Risk assessment for each client location

### CSV Export
- `earthquake_data.csv`: Raw earthquake data with time, place, magnitude, coordinates, and state

## Risk Assessment Criteria

- **High Risk**: >10 earthquakes OR max magnitude ≥ 5.0
- **Moderate Risk**: >5 earthquakes OR max magnitude ≥ 3.0  
- **Low Risk**: ≤5 earthquakes AND max magnitude < 3.0

## Client Locations

  The program assesses risk for these locations:
- West Anchorage High School (Anchorage, Alaska)
- City Hall (San Francisco, California)
- Los Angeles Memorial Coliseum (Los Angeles, California)
- Harrah's Reno (Former) (Reno, Nevada)
- Benson Polytechnic High School (Portland, Oregon)
- Salt Lake Temple (Salt Lake City, Utah)
- Challis High School (Challis, Idaho)

## Testing

  Run tests with:
```bash
python -m unittest discover tests
```

## Dependencies

- `requests`: For API calls to USGS
- `pandas`: For data manipulation and CSV export

## API Source

- USGS Earthquake API: https://earthquake.usgs.gov/fdsnws/event/1/
- Data format: GeoJSON
- Time range: Past 7 days (configurable)

## Notes

- Hawaii is excluded from all analysis as this region is not being underwritten
- The program uses a simple risk assessment model based on earthquake count and magnitude
- All times are in UTC
- Coordinates are in decimal degrees (WGS84)

## Technical Considerations

- The program handles API rate limits and errors gracefully
- State extraction uses the USGS 'place' field
- Risk assessment is based on recent activity (past week)
- CSV export includes all raw earthquake data for further analysis

## Limitations
- **Data Quality**: Relies on USGS data accuracy and completeness
- **Simple Model**: Uses basic count/magnitude thresholds rather than sophisticated risk modeling
- **State-Level Analysis**: Risk is assessed at state level, not specific location level
- **Fixed Client List**: Hardcoded list of client locations
- **No Predictive Modeling**: Provides current risk assessment, not future predictions

