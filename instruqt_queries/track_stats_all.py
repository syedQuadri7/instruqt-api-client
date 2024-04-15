import requests

def get_track_stats_all(tracks_list, org_slug, endpoint, headers, filter_developers, start, end):
    """
    Get statistics for all tracks in the specified time range.

    Parameters:
    - tracks_list (list): List of track dictionaries.
    - org_slug (str): Organization slug.
    - endpoint (str): API endpoint for making requests.
    - headers (dict): HTTP headers for the request.
    - filter_developers (str): Filter for including developers in statistics.
    - start (str): Start date for the statistics.
    - end (str): End date for the statistics.

    Returns:
    - track_stats (list): List of lists containing track statistics.
    """
    # Initialize an empty list to store track statistics
    track_stats = []

    # Iterate through each track in the list
    for track in tracks_list:
        # Extract track slug from the track dictionary
        track_slug = track["slug"]

        # Construct GraphQL query for retrieving track statistics
        query = """
            query {
                statistics(trackSlug: "%s", organizationSlug: "%s", filterDevelopers: %s, start: "%s", end: "%s") {
                    track {
                        title
                        started_total
                        completed_total
                    }
                }
            }""" % (track_slug, org_slug, filter_developers, start, end)

        # Make a POST request to the GraphQL endpoint and convert the response to JSON
        r = requests.post(endpoint, json={"query": query}, headers=headers)

        # Check if the request was successful (status code 200)
        if r.status_code == 200:
            # Extract track statistics from the response
            track_data = r.json()
            title = track_data["data"]["statistics"]["track"]["title"]
            started_total = track_data["data"]["statistics"]["track"]["started_total"]
            completed_total = track_data["data"]["statistics"]["track"]["completed_total"]

            # Create a row containing track statistics and append it to the list
            row = [title, started_total, completed_total]
            track_stats.append(row)
        else:
            # Raise an exception if the query fails to run
            raise Exception(f"Query failed to run with a {r.status_code}")

    return track_stats
