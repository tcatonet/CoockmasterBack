from user import test_get_user, test_delete_user, test_post_user, test_patch_user
from login import test_logged_user, test_user_login
from common import run_scenario


# run_scenario([test_get_user, test_post_user, test_get_user, test_delete_user, test_get_user])

# run_scenario([test_post_user, test_user_login, test_logged_user, test_delete_user])

# run_scenario([test_get_user, test_post_user, test_get_user, test_delete_user, test_get_user])

run_scenario([test_post_user, test_patch_user, test_get_user, test_delete_user])
