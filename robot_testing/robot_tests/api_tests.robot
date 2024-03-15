*** Settings ***
Library    RequestsLibrary

*** Test Cases ***
Check API endpoint returns status 200
    Create Session    my_session    http://localhost:8000
    ${response}=    Get Request    my_session    /api/contacts/all
    Should Be Equal As Strings    ${response.status_code}    200

