import daily_update
import info

# scrape
if info.in_season():
    daily_update.update_players()
    daily_update.update_standings()
    daily_update.update_teams()

    # internal organization
    daily_update.update_internal_info()

    # grades
    daily_update.update_grades_players()
    daily_update.update_grades_teams()

    daily_update.update_upstream()
else:
    print("Season is over!")
    if info.season_percentage() == 1.0:
        daily_update.clean_up()
# if last day of season:
    # move all data to archive