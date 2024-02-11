import daily_update

# scrape
daily_update.update_players()
daily_update.update_standings()
daily_update.update_teams()

# internal organization
daily_update.update_internal_info()

# grades
daily_update.update_grades_players()
daily_update.update_grades_teams()