# Function to retrieve track statistics based on slugs, organization slug, date range, and GraphQL client

def get_track_stats_by_slug(track_slugs, org_slug, endpoint, headers, filter_developers, dates, client):
    # Container for track statistics data
    slug_data = []

    # Iterate through each track slug
    for track_slug in track_slugs:
        # Container for a single track's data
        row = []
        print(track_slug)

        # Iterate through specified date range
        for k, v in dates.items():
            # GraphQL query to retrieve track statistics
            query = f"""query {{
                statistics(trackSlug: "{track_slug}", organizationSlug: "{org_slug}", filterDevelopers: {filter_developers}, start: "{k}", end: "{v}") {{
                    track {{
                        title
                        started_total
                        completed_total
                    }}
                }}
            }}"""

            # Execute the GraphQL query using the provided client
            track = client.do_query(query)

            # Extract relevant information from the GraphQL response
            title = track["statistics"]["track"]["title"]
            started_total = track["statistics"]["track"]["started_total"]

            # Add track title to the row if not already present
            if title not in row:
                row.append(title)

            # Add started_total to the row
            row.append(started_total)

        # Append the row to the overall slug_data
        slug_data.append(row)

    # Return the aggregated track statistics data
    return slug_data
