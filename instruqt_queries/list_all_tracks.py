import requests

def get_all_tracks(org_slug, endpoint, headers):
    """
    Get information about all tracks for a specific organization.

    Parameters:
    - org_slug (str): Organization slug.
    - endpoint (str): API endpoint for making requests.
    - headers (dict): HTTP headers for the request.

    Returns:
    - track_data (list): List of lists containing track information.
    """
    # Construct GraphQL query for retrieving track details
    query = """query {
        tracks(organizationSlug: "%s", orderBy: title_ASC) {
            id
            title
            slug
            permalink
            last_update
            play_count
            median_starttime
            creating
            created
            failed
            stopped
            completed
            challenges {
                id
                slug
                title
            }
            developers {
                profile {
                    display_name
                    slug
                }
            }
        }
    }""" % (org_slug)

    # Initialize an empty list to store track information
    track_data = []

    # Make a POST request to the GraphQL endpoint
    r = requests.post(endpoint, json={"query": query}, headers=headers)
    
    # Check if the request was successful (status code 200)
    if r.status_code == 200:
        data = r.json()

        # Iterate through each track in the response
        for track in data["data"]["tracks"]:
            track_id = track["id"]
            title = track["title"]
            slug = track["slug"]
            permalink = track["permalink"]
            last_update = track["last_update"]
            play_count = track["play_count"]
            median_starttime = track["median_starttime"]
            creating = track["creating"]
            created = track["created"]
            failed = track["failed"]
            stopped = track["completed"]
            
            # Join challenge slugs into a comma-separated string
            challenges = ", ".join([track["slug"] for track in track["challenges"]])
            
            # Join developer display names into a comma-separated string
            developers = ", ".join([track["profile"]["display_name"] for track in track["developers"]])

            # Create a row containing track information and append it to the list
            row = [track_id, title, slug, permalink, last_update, play_count, median_starttime,
                   creating, created, failed, stopped, challenges, developers]
            track_data.append(row)

    return track_data
