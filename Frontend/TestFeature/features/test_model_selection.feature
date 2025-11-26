Feature: Model Selection UI
  As an admin
  I want to activate or deactivate a model
  So that I can control which AI model is currently active

  Scenario: Activate a model
    Given I open the ListModelAI page
    When I click on "Aktifkan" button of "Version 1.0"
    Then I should see a toast message "Model changed to Version 1.0"
    And the model card should show "Aktif"

  Scenario: Deactivate the active model
    Given "Version 1.0" is already active
    When I click on "Nonaktifkan" button of "Version 1.0"
    Then I should see a toast message "Model deactivated"
    And the model card should not show "Aktif"