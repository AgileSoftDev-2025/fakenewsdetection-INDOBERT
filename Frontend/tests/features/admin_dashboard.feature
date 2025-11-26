Feature: Admin Dashboard

  As an admin
  I want to view the dashboard
  So that I can monitor the news checking statistics

  Scenario: Admin views dashboard
    Given I am on "Admin Homepage"
    Then I should see "Total Pengecekan"
    And I should see "Hoax Terdeteksi"
    And I should see "Sistem Overview"
    And I should see "Update Model"
    And I should see "Aksi Admin"