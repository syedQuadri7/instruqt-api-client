import requests

def get_invite_tracks(invite_id, endpoint, headers):
    """
    Get the list of track slugs associated with a specific track invite.

    Parameters:
    - invite_id (str): Unique identifier for the track invite.
    - endpoint (str): API endpoint for making requests.
    - headers (dict): HTTP headers for the request.

    Returns:
    - tracks (list): List of track slugs associated with the track invite.
    """
    # Construct GraphQL query for retrieving tracks associated with the invite
    query = """query {
        trackInvite(inviteID: "%s") {
            tracks {
                slug
            }
        }
    }""" % (invite_id)

    # Make a POST request to the GraphQL endpoint and convert the response to JSON
    r = requests.post(endpoint, json={"query": query}, headers=headers).json()

    # Initialize an empty list to store track slugs
    tracks = []

    # Iterate through each track in the response
    for track in r["data"]["trackInvite"]["tracks"]:
        track_slug = track["slug"]
        tracks.append(track_slug)

    return tracks
