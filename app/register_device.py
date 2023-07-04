import audible
import itertools
import getpass

# Authorize and register in one step
auth = audible.Authenticator.from_login(
    input("username:"),
    getpass.getpass("password":),
    locale="us",
    with_username=False
)

# Save credentials to file
auth.to_file("audible-creds")
