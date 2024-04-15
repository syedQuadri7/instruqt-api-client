# Function to retrieve track statistics based on slugs, organization slug, date range, and GraphQL client

def get_challenge_stats_by_slug(track_slugs, org_slug, endpoint, headers, filter_developers, dates, client):
    
    # Iterate through each track slug
    for track_slug in track_slugs:
        # Container for a single track's data
        challenge_data = []
        print(track_slug)

        # Iterate through specified date range
        for k, v in dates.items():
            # GraphQL query to retrieve track statistics
            query = f"""query {{
                statistics(trackSlug: "{track_slug}", organizationSlug: "{org_slug}", filterDevelopers: {filter_developers}, start: "{k}", end: "{v}") {{
                    track {{
                        id
                        title
                        challenges {{
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
                    }}
                }}
                }}
            }}"""

            # Execute the GraphQL query using the provided client
            track = client.do_query(query)

            # Extract relevant information from the GraphQL response
            track_title = track["statistics"]["track"]["title"]
            track_id = track["statistics"]["track"]["id"]

            # Add track title to the row if not already present
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
            print(row)
            challenge_data.append(row)

    # Return the aggregated track statistics data
    return challenge_data
