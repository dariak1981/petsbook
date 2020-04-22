# users/constants.py
SUPERUSER = 1
STAFF = 3
MODERATOR = 3
VISITOR = 4

USER_TYPE_CHOICES = (
      (SUPERUSER, 'superuser'),
      (STAFF, 'staff'),
      (MODERATOR, 'moderator'),
      (VISITOR, 'visitor'),
  )
