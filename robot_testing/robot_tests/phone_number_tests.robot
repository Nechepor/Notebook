*** Settings ***
Library    String
Library    OperatingSystem
Library    Collections
Library    ${EXECDIR}/Custom.py


*** Keywords ***
Should Be False
    [Arguments]    ${value}
    Run Keyword If    '${value}' == 0    Fail    Should Be False


*** Test Cases ***
Valid Phone Number Test
    [Documentation]    Test with a valid phone number
    [Tags]    phone-number
    ${result}    is_phone_number    79011234567
    Should Be True    ${result}

Invalid Phone Number Test
    [Documentation]    Test with an invalid phone number
    [Tags]    phone-number
    ${result}    Is Phone Number    invalid_phone
    Should Be False    ${result}

No Phone Number Test
    [Documentation]    Test with no phone number
    [Tags]    phone-number
    ${result}    Is Phone Number    This is not a phone number
    Should Be False    ${result}