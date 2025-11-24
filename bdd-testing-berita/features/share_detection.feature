# language: en
Feature: Share Hasil Deteksi Berita
  Sebagai pengguna yang telah melakukan deteksi berita
  Saya ingin dapat membagikan hasil deteksi
  Agar orang lain dapat melihat hasil analisis

  Background:
    Given the backend API is running
    And the frontend application is accessible

  @smoke @critical
  Scenario: User shares detection result via WhatsApp
    Given I am on "Results Page"
    And I see "Hoax" detection result
    When I press "Share"
    And I select "WhatsApp" from share options
    Then WhatsApp should open with pre-filled message
    And the message should contain news title
    And the message should contain "HOAX" status
    And the message should contain confidence score
    And the message should contain detection result link

  @smoke @critical
  Scenario: User copies detection result link
    Given I am on "Results Page"
    And the detection has ID "DET-2024-001234"
    When I press "Copy Link"
    Then the link "https://app.com/results/DET-2024-001234" should be copied to clipboard
    And I should see "Link copied successfully"
    And the notification should disappear after 3 seconds