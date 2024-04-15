# Function to retrieve information about all invites for a specific organization

def get_all_invites(org_slug, endpoint, headers, client):
    """
    Get information about all invites for a specific organization.

    Parameters:
    - org_slug (str): Organization slug.
    - endpoint (str): API endpoint for making requests.
    - headers (dict): HTTP headers for the request.
    - client (GraphQLClient): GraphQL client for executing queries.

    Returns:
    - invites (dict): JSON response containing information about all invites.
    """
    # GraphQL query to retrieve invite information
    query = """query {
        trackInvites(organizationSlug: "%s") {
            id
            title
            publicTitle
            inviteCount
            created
            tracks {
                slug
            }
        }
    }""" % (org_slug)

    # Execute the GraphQL query using the provided client
    invites = client.do_query(query)
    
    # Return the JSON response containing information about all invites
    return invites
