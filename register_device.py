import audible
import itertools
import getpass

# Authorize and register in one step
auth = audible.Authenticator.from_login(
    "ho0ber@gmail.com",
    getpass.getpass(),
    locale="us",
    with_username=False
)

# Save credentials to file
auth.to_file("creds")
