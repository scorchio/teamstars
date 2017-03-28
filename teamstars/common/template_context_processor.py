from teamstars.settings import calendar_enabled, votes_enabled


def feature_settings(request):
    return {
        'CALENDAR_ENABLED': calendar_enabled(),
        'VOTES_ENABLED': votes_enabled()
    }
