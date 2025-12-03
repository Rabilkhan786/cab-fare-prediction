# src/encoders.py

UBER_RIDES = [
    'UberX', 'UberPool', 'Black', 'WAV', 'BlackSUV'
]

LYFT_RIDES = [
    'Shared', 'Lyft Line', 'Lyft Plus', 'Lyft Premier', 'Lyft Luxsuv', 'Lyft Premier'
]

# Combined lists (for safety / fallback)
ALL_RIDE_TYPES = list(dict.fromkeys(UBER_RIDES + LYFT_RIDES + [
    'Lux', 'Taxi'  # extra possible labels
]))

# Locations used in the UI (same order matters for encoding)
LOCATIONS = ['Back Bay', 'Beacon Hill', 'Boston University', 'Fenway',
             'Financial District', 'Haymarket Square', 'North End',
             'North Station', 'Northeastern University', 'South Station',
             'Theatre District', 'West End']

LOCATION_ENCODING = {loc: i for i, loc in enumerate(LOCATIONS)}

COMPANY_ENCODING = {'Lyft': 0, 'Uber': 1}

# For models trained with specific ride_type indexes, keep a default mapping:
# Create mapping by enumerating the union (but in training you should match how you encoded).
RIDE_TYPE_ENCODING = {rt: i for i, rt in enumerate(ALL_RIDE_TYPES)}
