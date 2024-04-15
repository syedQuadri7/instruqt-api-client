import requests

# TODO: Update to accept list


def get_all_challenges(track_slugs, org_slug, endpoint, headers, filter_developers, start, end, client):
    """
    Get challenge statistics for multiple tracks within a specified date range.

    Parameters:
    - track_slugs (list): List of track slugs to retrieve challenge statistics for.
    - org_slug (str): Organization slug.
    - endpoint (str): API endpoint for making requests.
    - headers (dict): HTTP headers for the request.
    - filter_developers (str): Filter option for developers.
    - start (str): Start date for the statistics.
    - end (str): End date for the statistics.

    Returns:
    - challenge_data (list): List of challenge statistics for the specified tracks.
    """
    challenge_data = []
    for track_slug in track_slugs:
        # Construct GraphQL query for challenge statistics
        query = """query {
            statistics(organizationSlug: "%s", trackSlug: "%s", filterDevelopers: %s, start: "%s", end: "%s") {
                track {
                    id
                    title
                    challenges {
                        id
                        title
                        unlocked_total
                        started_total
                        completed_total
                        attempts_total
                        attempts_min
                        attempts_max
                        attempts_avg
                        attempts_stddev
                        duration_min
                        duration_max
                        duration_avg
                        duration_stddev
                    }
                }
            }
        }""" % (org_slug, track_slug, filter_developers, start, end)

        # Make a POST request to the GraphQL endpoint
        # r = requests.post(endpoint, json={"query": query}, headers=headers)
        response = client.do_query(query)
        print(response)
        track_data = response.json()
        print(track_data)

        # Extract track information
        track = track_data["data"]["statistics"]["track"]
        track_id = track["id"]
        track_title = track["title"]

        # Extract challenge information
        challenges = track["challenges"]
        for challenge in challenges:
            challenge_id = challenge["id"]
            challenge_title = challenge["title"]
            started_total = challenge["started_total"]
            completed_total = challenge["completed_total"]
            attempts_total = challenge["attempts_total"]
            attempts_min = challenge["attempts_min"]
            attempts_max = challenge["attempts_max"]
            attempts_avg = challenge["attempts_avg"]
            attempts_stddev = challenge["attempts_stddev"]
            duration_min = challenge["duration_min"]
            duration_max = challenge["duration_max"]
            duration_avg = challenge["duration_avg"]
            duration_stddev = challenge["duration_stddev"]

            # Create a row with challenge statistics and append to the result
            row = [
                track_id, track_title, challenge_id, challenge_title,
                started_total, completed_total, attempts_total,
                attempts_min, attempts_max, attempts_avg,
                attempts_stddev, duration_min, duration_max,
                duration_avg, duration_stddev
            ]

            challenge_data.append(row)
        else:
            raise Exception(f"Query failed to run with a {r.status_code}")

    return challenge_data
