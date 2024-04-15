import requests

def get_invite_track_completions(invite_ids, org_slug, endpoint, headers):
    """
    Get completion events for invites, including user details, track/challenge information, and timestamps.

    Parameters:
    - invite_ids (list): List of invite IDs.
    - org_slug (str): Organization slug.
    - endpoint (str): API endpoint for making requests.
    - headers (dict): HTTP headers for the request.

    Returns:
    - invite_data (list): List of lists containing invite completion details.
    """
    # Initialize an empty list to store invite completion details
    invite_data = []

    # Iterate through each invite ID in the list
    for invite_id in invite_ids:
        # Construct GraphQL query for retrieving invite completion events
        query = """
            query {
                trackInvite(inviteID: "%s") {
                    claims {
                        user {
                            profile {
                                email
                            }
                        }
                        events {
                            track {
                                title
                                slug
                            }
                            challenge {
                                slug
                            }
                            status
                            time
                            message
                        }
                    }
                }
            }""" % (invite_id)

        # Make a POST request to the GraphQL endpoint and convert the response to JSON
        r = requests.post(endpoint, json={"query": query}, headers=headers)

        # Check if the request was successful (status code 200)
        if r.status_code == 200:
            # Extract invite claims from the response
            claims = r.json()

            # Iterate through each claim in the invite claims
            for claim in claims["data"]["trackInvite"]["claims"]:
                user_email = claim["user"]["profile"]["email"]

                # Iterate through each event in the claim events
                for event in claim["events"]:
                    # Extract relevant information from the event
                    track_slug = "None" if event["track"] is None else event["track"]["slug"]
                    track_title = "None" if event["track"] is None else event["track"]["title"]
                    message = event["message"]
                    time = event["time"]
                    challenge = "None" if event["challenge"] is None else event["challenge"]["slug"]

                    # Create a row containing invite completion details and append it to the list
                    row = [user_email, invite_id, track_title, track_slug, challenge, message, time]
                    invite_data.append(row)
        else:
            # Raise an exception if the query fails to run
            raise Exception(f"Query failed to run with a {r.status_code}")

    return invite_data
