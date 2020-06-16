from django.conf import settings

USER_CATEGORIES_REQUIRING_RESET =  getattr(settings, 'RESETTY_USER_CATEGORIES_REQUIRING_RESET', ['is_staff'])
RESET_PASSWORD_DELTA = getattr(settings, 'RESETTY_RESET_PASSWORD_DELTA',  30)
REDIRECT_EXCLUDE_PATHS = getattr(settings, 'RESETTY_REDIRECT_EXCLUDE_PATHS', [])

# RESET_PASSWORD_AREAS = ['admin', 'account']

# other ideas
# FORCE_RESET_AT 
# SEND_RESET_REMINDER
# Exclude emails from reset...
