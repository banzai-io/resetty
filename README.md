# Resetty (Reset Password Middleware for Django). Banzai made.

This repo will add an automated functionallity into django apps to allow an automated password reset every 90 days (by default) for Staff and Superuser type users.

# Install
Add the following line to your requirements.txt file

```
git+https://github.com/banzai-io/resetty.git#egg=resetty
```

# Setup
On your settings file:

## Add the resetty app

```
INSTALLED_APPS += ['resetty']
```

## Add the middleware
Add resetty's middleware after auth's AuthenticationMiddleware

```
'django.contrib.auth.middleware.AuthenticationMiddleware',
# Resetty must be placed after Session and Authentication Middleware
'resetty.middleware.ResetPasswordMiddleware', 
```

## Add resetty's password validator
It's preferable if you add it at the top of your auth validators

```
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "resetty.auth_password_validators.DoNotReusePasswordValidator",
    },
    # ... other validators below
]
```

# RESETTY OPTIONS
You can override resetty's default values in your settings file. The available options are:

### RESETTY_USER_CATEGORIES_REQUIRING_RESET
* Inspects your user's instance and determines if it needs to reset password based on the user flags
* Type: list
* Default value: `['is_staff']`
* Available values: `['is_staff'|'is_superuser']` that can be combined in the list. 

### RESETTY_RESET_PASSWORD_DELTA_DAYS
* Delta time in days after last password update where we require a new one
* Type: int 
* Default value: `90`

### RESETTY_RESET_PASSWORD_URL
* URL where the user will reset her/his password.
* Type: string
* Default value: `/admin/password_change/`

### RESETTY_REDIRECT_EXCLUDED_PATHS
* URL paths which the middleware exempts from redirection. This is important to avoid request looping
* Type: list
* Default value: `[
"/admin/login/",
"/admin/logout/",
"/admin/password_change/",
"/admin/password_change/done/"
]`
and any route that matches the pattern 
`r'\/?(.+)?\/reset\/?'`

# Last step
Set your local settings and build your container or pip install. Also, run your migrations.

# Expected behavior after install
All views not included in `RESETTY_REDIRECT_EXCLUDED_PATHS` will require you to change your password if haven't. This behavior will be repeated everytime the passwrod expires (`RESETTY_RESET_PASSWORD_DELTA_DAYS`).
