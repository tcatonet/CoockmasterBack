class ErrorMessages:
    DATABASE_ERROR = "Error: Database error"
    MISSING_PROJECT_NAME = "project name is missing"
    NAME_ACCOUNT_ERROR = "Error: This name is already used"
    PASSWORD_ACCOUNT_ERROR = "Error: Your password is incorrect"
    SAME_ACCOUNT_PASSWORD_ERROR = "Error: Your new passwords must be the same"
    FOUND_ACCOUNT_ERROR = "Error: Your account cannot be found"
    EXISTING_EMAIL_ACCOUNT_ERROR = "Error: An account with your email already exist"
    ACCOUNT_AUTHENTICATE_ERROR = "Error: Wrong email or password"
    INVALID_NAME_PROJECT = "Invalid name project"

    NAME_PROJECT_ERROR = "Error: This name is already used"
    NAME_NO_PROJECT_ERROR = "Error: There is no project with this name"

    FORMAT_PASSWORD_CHECK_ERROR = "The password must contain one number, one capital letter, one special character and the lenght should be 8-30"
    SAME_ACCOUNT_PASSWORD_CHECK_ERROR = "Your new passwords must be the same"
    WRONG_INFRA_CHECK_ERROR = "Wrong infrastructure"
    WRONG_INSEE_CHECK_ERROR = "Wrong insee code"
    WRONG_EMAIL_CHECK_ERROR = "Wrong email format"

    WRONG_PAYLOAD_FORMAT_ERROR = "Wrong payload format"
    INTERNAL_ERROR = "Internal error"

    INTERNAL_ERROR_TRY = "Internal error try later"

    CHECK_DATA_ERROR = "Data check error"

    SENDMAIL_ERROR = "Error while sending message, try later or send your own mail at test@test.fr"

    INVALID_TOKEN = 'token is invalid'
    MISSING_TOKEN = 'token is missing'
    INVALID_LOCATION = "Unnable to find your location"

    ACCOUNT_DOESNT_EXISTS = "account attached to this email does not exists"


class InfoMessages:
    ACCOUNT_CREATION_SUCCESS = "Your account was successfull created"
    ACCOUNT_RETRIEVE_SUCCESS = "Your informations was successfull retrieved"
    ACCOUNT_DELETE_SUCCESS = "Your account deletion was successfull"
    ACCOUNT_UPDATE_SUCCESS = "Your account was successfully update"
    ACCOUNT_PASSWORD_SUCCESS = "Your password was successfully update"
    ACCOUNT_PROJECTS_SUCCESS = "Your projects was successfully retrieve"
    ACCOUNT_AUTHENTICATE_SUCCESS = "Your are successfully authenticate"

    GEORISK_DATA_RETRIEVE_SUCCESS = "You successfully get data of the geo risk api"
    PROJECT_CREATE_SUCCESS = "Your project was successfully create"
    PROJECT_UPDATE_SUCCESS = "Your project was successfully update"
    PROJECT_DELETE_SUCCESS = "Your project was successfully delete"
    PROJECT_RETRIEVE_SUCCESS = "Your project was successfully retrieve"
    INFRASTRUCTURE_RETRIEVE_SUCCESS = "Infrastructure was successfully retrieve"
    SENDMAIL_SUCCESS = "Your message was successfully send"
