import requests

def get_track_stats_by_slug(track_slugs, org_slug, endpoint, headers, filter_developers, start, end):
    """
    Get track statistics by slug, including titles, started totals, and completed totals.

    Parameters:
    - track_slugs (list): List of track slugs.
    - org_slug (str): Organization slug.
    - endpoint (str): API endpoint for making requests.
    - headers (dict): HTTP headers for the request.
    - filter_developers (str): Filter developers based on a condition.
    - start (str): Start date for the statistics.
    - end (str): End date for the statistics.

    Returns:
    - slug_data (list): List of lists containing track statistics.
    """
    # Initialize an empty list to store track statistics
    slug_data = []

    # Iterate through each track slug in the list
    for track_slug in track_slugs:
        # Construct GraphQL query for retrieving track statistics
        query = f"""query {{
            statistics(trackSlug: "{track_slug}", organizationSlug: "{org_slug}", filterDevelopers: {filter_developers}, start: "{start}", end: "{end}") {{
                track {{
                    title
                    started_total
                    completed_total
                }}
            }}
        }}"""

        # Make a POST request to the GraphQL endpoint and convert the response to JSON
        r = requests.post(endpoint, json={"query": query}, headers=headers)

        # Check if the request was successful (status code 200)
        if r.status_code == 200:
            # Extract track information from the response
            track_data = r.json()
            track = track_data["data"]["statistics"]["track"]

            # Extract relevant data from the track information
            title = track["title"]
            started_total = track["started_total"]
            completed_total = track["completed_total"]

            # Create a row containing the track statistics
            row = [title, started_total, completed_total]

            # Append the row for the current track to the slug_data list
            slug_data.append(row)
        else:
            # Raise an exception if the query fails to run
            raise Exception(f"Query failed to run with a {r.status_code}")

    return slug_data
