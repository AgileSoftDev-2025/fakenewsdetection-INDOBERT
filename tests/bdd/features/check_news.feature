Feature: Check news validity
  As a user, I want to check news so I can know whether it's hoax or not.

  Scenario: User checks a valid news via text
    Given I am on "check-news page"
    When I fill in "news_text" with "The government officially announces a national holiday"
    And I press "Check"
    Then I should see "Valid/Hoax"

  Scenario: User checks a valid news via document
    Given I am on "check-news page"
    When I attach the file "/path/valid_news.docx" to "news_file"
    And I press "Check"
    Then I should see "Valid/Hoax"
