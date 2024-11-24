import daily_update
import info

# scrape
if info.in_season():
    daily_update.update_players()
    # daily_update.update_standings()
    # daily_update.update_teams()

    # internal organization
    daily_update.update_internal_info()

    # grades
    daily_update.update_grades_players()
    daily_update.update_grades_teams()
else:
    print("Season is over!")
# if last day of season:
    # move all data to archive