import requests

def get_invite_emails(invite_id, endpoint, headers):
    """
    Get email addresses associated with a specific track invite.

    Parameters:
    - invite_id (str): Unique identifier for the track invite.
    - endpoint (str): API endpoint for making requests.
    - headers (dict): HTTP headers for the request.

    Returns:
    - invite_emails (list): List of email addresses associated with the track invite.
    """
    # Construct GraphQL query for retrieving user emails associated with the invite
    query = """query {
        trackInvite(inviteID: "%s") {
            claims {
                user {
                    profile {
                        email
                    }
                }
            }
        }
    }""" % (invite_id)

    # Make a POST request to the GraphQL endpoint and convert the response to JSON
    r = requests.post(endpoint, json={"query": query}, headers=headers).json()

    # Initialize an empty list to store email addresses
    invite_emails = []

    # Iterate through each user claim in the response
    for user in r["data"]["trackInvite"]["claims"]:
        user_email = user["user"]["profile"]["email"]
        invite_emails.append(user_email)

    return invite_emails
