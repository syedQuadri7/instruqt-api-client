# Function to retrieve all track slugs within an organization using a GraphQL client

def get_all_track_slugs(org_slug, client):
    # GraphQL query to retrieve all track slugs within the organization
    query = f"""query {{
        tracks(organizationSlug: "{org_slug}") {{
            slug
        }}
    }}"""

    # Execute the GraphQL query using the provided client
    response = client.do_query(query)

    # Extract the slugs from the GraphQL response
    slugs = [track['slug'] for track in response['tracks']]

    # Return the list of slugs
    return slugs
