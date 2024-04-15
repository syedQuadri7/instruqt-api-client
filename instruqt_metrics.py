# Import necessary modules
import json
import os
import instruqt
from instruqt_queries import (
    list_all_tracks, list_invite_emails, list_invite_tracks,
    track_stats_all, track_stats_by_invite, track_stats_by_slug, list_all_invites,
    track_stats_by_slug_by_year, challenge_stats_by_slug, utilities, list_track_slugs,test
)

file_path = 'config.json'


def read_config_file(file_path):
    # Read and parse the JSON configuration file
    with open(file_path, 'r') as file:
        config = json.load(file)

    return (
        config.get("google_sheets").get("spreadsheet"),
        config.get("metrics").get("track_stats"),
        config.get("metrics").get("track_stats_yearly"),
        config.get("metrics").get("invite_stats"),
        config.get("metrics").get("track_invite_stats"),
        config.get("metrics").get("challenge_stats"),
        config.get("instruqt").get("endpoint", ""),
        config.get("instruqt").get("org_slug", ""),
        config.get("instruqt").get("filter_developers", ""),
        config.get("demos").get("terraform_demos"),
        config.get("demos").get("vault_demos"),
        config.get("demos").get("consul_demos"),
        config.get("demos").get("nomad_demos"),
        config.get("demos").get("packer_demos"),
        config.get("demos").get("zts_demos"),
        config.get("workshops").get("terraform_workshops"),
        config.get("workshops").get("vault_workshops"),
        config.get("workshops").get("consul_workshops"),
        config.get("workshops").get("nomad_workshops"),
        config.get("HVD").get("terraform_adopt")
    )


SPREADSHEET, TRACK_STAT_HEADERS, TRACK_STAT_HEADERS_YEARLY, INVITE_STAT_HEADERS, TRACK_INVITE_HEADERS, CHALLENGE_STAT_HEADERS, ENDPOINT, ORG_SLUG, FILTER_DEVELOPERS, TERRAFORM_DEMOS, VAULT_DEMOS, CONSUL_DEMOS, NOMAD_DEMOS, PACKER_DEMOS, ZTS_DEMOS, TERRAFORM_WORKSHOPS, VAULT_WORKSHOPS, CONSUL_WORKSHOPS, NOMAD_WORKSHOPS, TF_ADOPT = read_config_file(
    file_path)  # Append TERRAFORM_ADOPT when tracks are GA

# Google Sheet Access
CREDENTIALS_FILE = os.environ["GOOGLE_SPREADSHEET_CREDENTIALS"]

# Instruqt
ACCESS_TOKEN = os.environ["INSTRUQT_REFRESH_TOKEN"]
HTTP_HEADERS = {"Authorization": "Bearer %s" % (ACCESS_TOKEN)}

# CORE_DEMOS = TERRAFORM_DEMOS + VAULT_DEMOS + PACKER_DEMOS + ZTS_DEMOS
# EMERGING_DEMOS = CONSUL_DEMOS + NOMAD_DEMOS

# ALL_DEMOS = CORE_DEMOS + EMERGING_DEMOS

# CORE_WORKSHOPS = TERRAFORM_WORKSHOPS + VAULT_WORKSHOPS
# EMERGING_WORKSHOPS = CONSUL_WORKSHOPS + NOMAD_WORKSHOPS

# ALL_WORKSHOPS = CORE_WORKSHOPS + EMERGING_WORKSHOPS

# ALL_WORKSHOPS = TF_ADOPT

ic = instruqt.InstruqtClient(
    uri='https://play.instruqt.com/graphql', refresh_token=ACCESS_TOKEN)


# Get all track slugs
def delete_items_from_list(original_list, items_to_delete):
    return [item for item in original_list if item not in items_to_delete]


items_to_delete = ['nomad-if-chip', 'nomad-if-cluster', 'tfe-and-vcs-systems', 'tfe-manual-install',
                   'tfe-standalone-public', 'vault-certified-hashicorp-implementation-partner-chip']

ALL_TRACKS = sorted(list_track_slugs.get_all_track_slugs(ORG_SLUG, ic))
ALL_TRACKS = delete_items_from_list(ALL_TRACKS, items_to_delete)

# Write the sorted track slugs to a file
with open('track_slugs', 'w') as f:
    json.dump(ALL_TRACKS, f)


# Define POVs and Invite IDs
POVS = []
INVITE_IDS = []


def pull_all_tracks_data(worksheet, start=None, end=None):
    # Get all tracks data
    all_tracks = list_all_tracks.get_all_tracks(
        ORG_SLUG, ENDPOINT, HTTP_HEADERS)
    print(all_tracks)
    start_date, end_date = utilities.dates_formatted(start, end)

    # Get track stats for all tracks
    track_data = track_stats_all.get_track_stats_all(
        all_tracks, ORG_SLUG, ENDPOINT, HTTP_HEADERS, FILTER_DEVELOPERS, start_date, end_date)

    # Write track stats to Google Sheets
    # utilities.write_to_sheets(CREDENTIALS_FILE, SPREADSHEET, worksheet, TRACK_STAT_HEADERS, track_data)


def pull_track_slug_data(worksheet, track_slugs, start=None, end=None):
    start_date, end_date = utilities.dates_formatted(start, end)

    # Get track stats for specific track slugs
    track_slug_data = track_stats_by_slug.get_track_stats_by_slug(
        track_slugs, ORG_SLUG, ENDPOINT, HTTP_HEADERS, FILTER_DEVELOPERS, start_date, end_date)

    # Write track stats to Google Sheets
    utilities.write_to_sheets(
        CREDENTIALS_FILE, SPREADSHEET, worksheet, TRACK_STAT_HEADERS, track_slug_data)


def pull_all_challenges_from_invite(worksheet, invite_ids):
    # Get all challenges from invites
    all_challenges = track_stats_by_invite.get_invite_track_completions(
        invite_ids, ORG_SLUG, ENDPOINT, HTTP_HEADERS)

    # Write invite challenges to Google Sheets
    utilities.write_to_sheets(
        CREDENTIALS_FILE, SPREADSHEET, worksheet, INVITE_STAT_HEADERS, all_challenges)


def pull_invites_for_track(worksheet, track_list, client, start=None, end=None):
    invite_data = list_all_invites.get_all_invites(
        ORG_SLUG, ENDPOINT, HTTP_HEADERS, client)

    # Filter invites based on track list and date range
    filtered_invites = utilities.filter_by_slug(
        invite_data, track_list, start, end)

    # Write filtered invites to Google Sheets
    utilities.write_to_sheets(
        CREDENTIALS_FILE, SPREADSHEET, worksheet, TRACK_INVITE_HEADERS, filtered_invites)


def pull_track_slug_data_year(worksheet, track_slugs, year, client):
    dates = utilities.month_map(year)

    # Get track stats for specific track slugs and year
    track_slug_data = track_stats_by_slug_by_year.get_track_stats_by_slug(
        track_slugs, ORG_SLUG, ENDPOINT, HTTP_HEADERS, FILTER_DEVELOPERS, dates, client)

    # Write yearly track stats to Google Sheets
    utilities.write_to_sheets(CREDENTIALS_FILE, SPREADSHEET,
                              worksheet, TRACK_STAT_HEADERS_YEARLY, track_slug_data)


def pull_all_challenges_data(worksheet, track_slugs, client, start=None, end=None):
    start_date, end_date = utilities.dates_formatted(start, end)

    # Get all challenges for specific track slugs
    all_challenges = challenge_stats_by_slug.get_all_challenges(
        track_slugs, ORG_SLUG, ENDPOINT, HTTP_HEADERS, FILTER_DEVELOPERS, start_date, end_date, client)

    # Write all challenges to Google Sheets
    utilities.write_to_sheets(
        CREDENTIALS_FILE, SPREADSHEET, worksheet, CHALLENGE_STAT_HEADERS, all_challenges)

# MONTHLY SALES PLAY DEMO METRICS FOR FY
# print("running pull_track_slug_data_year Sales Play Demo Metrics - FY23")
# pull_track_slug_data_year("Sales Play Demo Metrics - FY23", ALL_DEMOS, "2022", ic)

# MONTHLY WORKSHOP DEMO METRICS FOR FY
# pull_track_slug_data_year("HVD Metrics", TF_ADOPT, "2024", ic)
# pull_track_slug_data_year("Workshop Metrics - FY25", ALL_TRACKS, "2024", ic)
# pull_all_challenges_data("Challenge Metrics - FY25", ALL_TRACKS, ic, "2024-01-01", "2024-12-31")

# test.get_challenge_stats_by_slug(ALL_TRACKS, ORG_SLUG, ENDPOINT, HTTP_HEADERS, FILTER_DEVELOPERS, "2024-01-01", "2024-12-31", ic)


def testing(worksheet, track_slugs, client, start=None, end=None):
    start_date, end_date = utilities.dates_formatted(start, end)

    # Get all challenges for specific track slugs
    all_challenges = test.get_challenge_stats_by_slug(track_slugs, ORG_SLUG, ENDPOINT, HTTP_HEADERS, FILTER_DEVELOPERS, dates, client)

testing("Challenge Metrics - FY25", ALL_TRACKS, ic, "2024-01-01", "2024-12-31")
# # WORKSHOP INVITE METRICS FOR FY
# pull_invites_for_track("Workshop Invites - FY23", ALL_WORKSHOPS, ic, "2022-01-01", "2022-12-31")

# pull_all_tracks_data(ALL_WORKSHOPS,"2024-01-01", "2024-12-31")
