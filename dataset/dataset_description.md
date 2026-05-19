# Dataset Description

## Source
Dataset extracted from Strava activities using the Strava REST API.

## Relevant Columns

| Column | Description | Unit |
|---|---|---|
| name | Activity name | text |
| distance | Distance traveled | miles |
| moving_time | Time in movement | minutes |
| total_elevation | Elevation gain | feet |
| average_speed | Average speed | mph |
| sport_type | Activity type | text |
| date | Activity date | datetime |

## Data Transformations
For analysis purposes, the dataset will be converted to the metric system:
- miles → kilometers
- mph → km/h
- feet → meters