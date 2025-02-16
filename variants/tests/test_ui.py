"""UI tests for the projectroles app"""

import json
import os
import socket
import time
from unittest import skipIf

from django.contrib import auth
from django.test import LiveServerTestCase
from django.urls import reverse
from projectroles.models import SODAR_CONSTANTS, Role
from projectroles.tests.test_models import ProjectMixin, RoleAssignmentMixin
import projectroles.tests.test_ui
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from extra_annos.tests.factories import ExtraAnnoFactory, ExtraAnnoFieldFactory
from variants.tests.factories import (
    CaseWithVariantSetFactory,
    ProjectFactory,
    SampleVariantStatisticsFactory,
    SmallVariantFactory,
)

from ..models import update_variant_counts

# SODAR constants
PROJECT_ROLE_OWNER = SODAR_CONSTANTS["PROJECT_ROLE_OWNER"]
PROJECT_ROLE_DELEGATE = SODAR_CONSTANTS["PROJECT_ROLE_DELEGATE"]
PROJECT_ROLE_CONTRIBUTOR = SODAR_CONSTANTS["PROJECT_ROLE_CONTRIBUTOR"]
PROJECT_ROLE_GUEST = SODAR_CONSTANTS["PROJECT_ROLE_GUEST"]
PROJECT_TYPE_CATEGORY = SODAR_CONSTANTS["PROJECT_TYPE_CATEGORY"]
PROJECT_TYPE_PROJECT = SODAR_CONSTANTS["PROJECT_TYPE_PROJECT"]
SITE_MODE_TARGET = SODAR_CONSTANTS["SITE_MODE_TARGET"]
SITE_MODE_SOURCE = SODAR_CONSTANTS["SITE_MODE_SOURCE"]

# Local constants
PROJECT_LINK_IDS = [
    "sodar-pr-link-project-roles",
    "sodar-pr-link-project-update",
    "sodar-pr-link-project-create",
    "sodar-pr-link-project-star",
]


User = auth.get_user_model()


SKIP_SELENIUM = "1" == os.environ.get("SKIP_SELENIUM", "0")
SKIP_SELENIUM_MESSAGE = "Selenium tests disabled"


class wait_for_the_attribute_value(object):
    """https://stackoverflow.com/a/43813210/84349

    Usage:

    self.wait.until(wait_for_the_attribute_value((By.ID, "xxx"), "aria-busy", "false"))

    """

    def __init__(self, locator, attribute, value):
        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = ec._find_element(driver, self.locator).get_attribute(self.attribute)
            return element_attribute == self.value
        except StaleElementReferenceException:
            return False


class wait_for_the_attribute_endswith_value(object):
    """https://stackoverflow.com/a/43813210/84349

    Usage:

    self.wait.until(wait_for_the_attribute_value((By.ID, "xxx"), "aria-busy", "false"))

    """

    def __init__(self, locator, attribute, value):
        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = ec._find_element(driver, self.locator).get_attribute(self.attribute)
            return element_attribute.endswith(self.value)
        except StaleElementReferenceException:
            return False


class wait_for_element_endswith_value(object):
    """https://stackoverflow.com/a/43813210/84349

    Usage:

    self.wait.until(wait_for_the_attribute_value((By.ID, "xxx"), "aria-busy", "false"))

    """

    def __init__(self, element, attribute, value):
        self.element = element
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = self.element.get_attribute(self.attribute)
            return element_attribute.endswith(self.value)
        except StaleElementReferenceException:
            return False


class element_has_class_locator(object):
    """An expectation for checking that an element has a particular css class.
       locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element

        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False


class element_has_class(object):
    """An expectation for checking that an element has a particular css class.
       locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, element, css_class):
        self.element = element
        self.css_class = css_class

    def __call__(self, driver):
        if self.css_class in self.element.get_attribute("class"):
            return self.element
        else:
            return False


class LiveUserMixin:
    """Mixin for creating users to work with LiveServerTestCase"""

    @classmethod
    def _make_user(cls, user_name, superuser):
        """Make user, superuser if superuser=True"""
        kwargs = {
            "username": user_name,
            "password": "password",
            "email": "{}@example.com".format(user_name),
            "is_active": True,
        }

        if superuser:
            user = User.objects.create_superuser(**kwargs)

        else:
            user = User.objects.create_user(**kwargs)

        user.save()
        return user


class TestUIBase(projectroles.tests.test_ui.TestUIBase):
    """Base class for UI tests"""

    def compile_url_and_login(self, kwargs={}):
        self.login_and_redirect(self.superuser, reverse(self.view, kwargs=kwargs))

    def _disable_filters(self, case_or_project):
        self.selenium.find_element_by_id("quick-presets-button").click()
        self.selenium.find_element_by_xpath("//a[@data-preset-name='whole-exome']").click()
        time.sleep(1)

    def assert_element_exists(self, kwargs, element_id, exists):
        """
        Assert existence of element on webpage based on logged user.
        :param users: User objects to test (list)
        :param url: URL to test (string)
        :param element_id: ID of element (string)
        :param exists: Whether element should or should not exist (boolean)
        """

        self.compile_url_and_login(kwargs)

        if exists:
            self.assertIsNotNone(self.selenium.find_element_by_id(element_id))
        else:
            with self.assertRaises(NoSuchElementException):
                self.selenium.find_element_by_id(element_id)


class TestVariantsCaseListView(TestUIBase):
    """Tests for variants case list view"""

    view = "variants:case-list"

    def setUp(self):
        super().setUp()
        self.case, variant_set, _ = CaseWithVariantSetFactory.get("small")
        SampleVariantStatisticsFactory(variant_set=variant_set, sample_name=variant_set.case.index)

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_case_list_item_exists(self):
        """Test if list with case is rendered."""
        self.assert_element_exists(
            {"project": self.case.project.sodar_uuid},
            "varfish-bg-table-row-{}".format(self.case.sodar_uuid),
            True,
        )


class TestVariantsCaseDetailView(TestUIBase):
    """Tests for the variants case detail view"""

    view = "variants:case-detail"

    def setUp(self):
        super().setUp()
        self.case, variant_set, _ = CaseWithVariantSetFactory.get("small")
        SampleVariantStatisticsFactory(variant_set=variant_set, sample_name=variant_set.case.index)

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_case_detail_overview_card_exists(self):
        """Test if the variant details view gets rendered"""
        self.assert_element_exists(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid},
            "card-varfish-vars-case-details-overview",
            True,
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_case_detail_pedigree_card_exists(self):
        """Test if the variant details view gets rendered"""
        self.assert_element_exists(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid},
            "card-varfish-vars-case-details-pedigree",
            True,
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_case_detail_qc_plots_card_exists(self):
        """Test if the variant details view gets rendered"""
        self.assert_element_exists(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid},
            "card-varfish-vars-case-details-qc-plots",
            True,
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_case_detail_comments_card_exists(self):
        """Test if the variant details view gets rendered"""
        self.assert_element_exists(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid},
            "card-varfish-vars-case-details-small-var-comments",
            True,
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_case_detail_flags_card_exists(self):
        """Test if the variant details view gets rendered"""
        self.assert_element_exists(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid},
            "card-varfish-vars-case-details-small-var-flags",
            True,
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_case_detail_bg_jobs_card_exists(self):
        """Test if the variant details view gets rendered"""
        self.assert_element_exists(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid},
            "card-varfish-vars-case-details-bg-jobs",
            True,
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_case_detail_qc_card_exists(self):
        """Test if the variant details view gets rendered"""
        self.assert_element_exists(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid},
            "card-varfish-vars-case-details-qc",
            True,
        )


EFFECT_FIELDS = {
    "id_effect_disruptive_inframe_deletion": False,
    "id_effect_disruptive_inframe_insertion": False,
    "id_effect_feature_truncation": False,
    "id_effect_exon_loss_variant": False,
    "id_effect_frameshift_elongation": False,
    "id_effect_frameshift_truncation": False,
    "id_effect_frameshift_variant": False,
    "id_effect_inframe_deletion": False,
    "id_effect_inframe_insertion": False,
    "id_effect_internal_feature_elongation": False,
    "id_effect_missense_variant": False,
    "id_effect_mnv": False,
    "id_effect_start_lost": False,
    "id_effect_stop_gained": False,
    "id_effect_stop_retained_variant": False,
    "id_effect_stop_lost": False,
    "id_effect_synonymous_variant": False,
    "id_effect_direct_tandem_duplication": False,
    "id_effect_downstream_gene_variant": False,
    "id_effect_coding_transcript_intron_variant": False,
    "id_effect_intergenic_variant": False,
    "id_effect_upstream_gene_variant": False,
    "id_effect_three_prime_UTR_exon_variant": False,
    "id_effect_three_prime_UTR_intron_variant": False,
    "id_effect_five_prime_UTR_exon_variant": False,
    "id_effect_five_prime_UTR_intron_variant": False,
    "id_effect_non_coding_transcript_exon_variant": False,
    "id_effect_non_coding_transcript_intron_variant": False,
    "id_effect_splice_acceptor_variant": False,
    "id_effect_splice_donor_variant": False,
    "id_effect_splice_region_variant": False,
    "id_effect_structural_variant": False,
    "id_effect_transcript_ablation": False,
    "id_effect_complex_substitution": False,
}


class TestVariantsCaseFilterView(TestUIBase):
    """Tests for the variants case filter view."""

    view = "variants:case-filter"
    window_size = (2000, 1000)

    def setUp(self):
        super().setUp()
        self.case, self.variant_set, _ = CaseWithVariantSetFactory.get("small")
        SmallVariantFactory(variant_set=self.variant_set)

    def _create_two_more_variants(self):
        SmallVariantFactory.create_batch(2, variant_set=self.variant_set)

    def _disable_effect_groups(self):
        """Helper function to disable all effect checkboxes by activating and deactivating the 'all' checkbox."""
        self.selenium.find_element_by_id("more-tab").click()
        tab = self.selenium.find_element_by_id("effect-tab")
        checkbox = self.selenium.find_element_by_id("id_effect_group_all")
        cross_checkbox = self.selenium.find_element_by_id("id_effect_synonymous_variant")
        # switch tab and wait until change happened
        tab.click()
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(checkbox))
        # initially checkbox all synonymous_variant are unchecked, test for that
        WebDriverWait(self.selenium, self.wait_time).until_not(ec.element_to_be_selected(checkbox))
        WebDriverWait(self.selenium, self.wait_time).until_not(
            ec.element_to_be_selected(cross_checkbox)
        )
        # click all to enable it and wait for changes to take place
        checkbox.click()
        WebDriverWait(self.selenium, self.wait_time).until(ec.element_to_be_selected(checkbox))
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.element_to_be_selected(cross_checkbox)
        )
        # click all to disable it and wait for changes to take place
        checkbox.click()
        WebDriverWait(self.selenium, self.wait_time).until_not(ec.element_to_be_selected(checkbox))
        WebDriverWait(self.selenium, self.wait_time).until_not(
            ec.element_to_be_selected(cross_checkbox)
        )

    def _check_effect_groups(self, group, effect_fields_patch):
        """Helper function for testing the performance of the effect group checkboxes."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # switch tab and disable effect groups
        self._disable_effect_groups()
        # patch effect fields
        patched_effect_fields = {**EFFECT_FIELDS, **effect_fields_patch}
        # select checkbox effects, if group is provided
        if group:
            self.selenium.find_element_by_id(group).click()
        # check for ticked checkboxes
        for field, value in patched_effect_fields.items():
            self.assertEqual(self.selenium.find_element_by_id(field).is_selected(), value)

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_effects_form_select_none(self):
        """Test if effect group checkbox 'all' disables all effects if activated and deactivated."""
        self._check_effect_groups(None, {})

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_effects_form_select_all(self):
        """Test if effect group checkbox 'all' selects all effect checkboxes."""
        self._check_effect_groups("id_effect_group_all", {effect: True for effect in EFFECT_FIELDS})

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_effects_form_select_nonsynonymous(self):
        """Test if effect group checkbox 'nonsynonymous' selects the correct effect checkboxes."""
        self._check_effect_groups(
            "id_effect_group_nonsynonymous",
            {
                "id_effect_disruptive_inframe_deletion": True,
                "id_effect_disruptive_inframe_insertion": True,
                "id_effect_feature_truncation": True,
                "id_effect_exon_loss_variant": True,
                "id_effect_frameshift_elongation": True,
                "id_effect_frameshift_truncation": True,
                "id_effect_frameshift_variant": True,
                "id_effect_inframe_deletion": True,
                "id_effect_inframe_insertion": True,
                "id_effect_internal_feature_elongation": True,
                "id_effect_missense_variant": True,
                "id_effect_mnv": True,
                "id_effect_start_lost": True,
                "id_effect_stop_gained": True,
                "id_effect_stop_lost": True,
                "id_effect_direct_tandem_duplication": True,
                "id_effect_structural_variant": True,
                "id_effect_transcript_ablation": True,
                "id_effect_complex_substitution": True,
            },
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_effects_form_select_splicing(self):
        """Test if effect group checkbox 'splicing' selects the correct effect checkboxes."""
        self._check_effect_groups(
            "id_effect_group_splicing",
            {
                "id_effect_splice_acceptor_variant": True,
                "id_effect_splice_donor_variant": True,
                "id_effect_splice_region_variant": True,
            },
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_effects_form_select_coding(self):
        """Test if effect group checkbox 'coding' selects the correct effect checkboxes."""
        self._check_effect_groups(
            "id_effect_group_coding",
            {"id_effect_stop_retained_variant": True, "id_effect_synonymous_variant": True},
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_effects_form_select_utr_intronic(self):
        """Test if effect group checkbox 'UTR/intronic' selects the correct effect checkboxes."""
        self._check_effect_groups(
            "id_effect_group_utr_intronic",
            {
                "id_effect_coding_transcript_intron_variant": True,
                "id_effect_three_prime_UTR_exon_variant": True,
                "id_effect_three_prime_UTR_intron_variant": True,
                "id_effect_five_prime_UTR_exon_variant": True,
                "id_effect_five_prime_UTR_intron_variant": True,
            },
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_effects_form_select_noncoding(self):
        """Test if effect group checkbox 'noncoding' selects the correct effect checkboxes."""
        self._check_effect_groups(
            "id_effect_group_noncoding",
            {
                "id_effect_downstream_gene_variant": True,
                "id_effect_intergenic_variant": True,
                "id_effect_upstream_gene_variant": True,
                "id_effect_non_coding_transcript_exon_variant": True,
                "id_effect_non_coding_transcript_intron_variant": True,
            },
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_settings_initial_database(self):
        """Test if the initial form settings correspond to the JSON dump textarea by checking the database setting."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # obtain initial settings from textarea
        settings = json.loads(
            self.selenium.find_element_by_id("settingsDump").get_attribute("value")
        )
        # check if database_select switch is set as expected to refseq
        self.assertEqual(settings["database_select"], "refseq")
        # check if initial setting is as expected
        self.assertTrue(
            self.selenium.find_element_by_xpath(
                '//input[@name="database_select" and @value="refseq"]'
            ).is_selected()
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_settings_export_database_refseq_to_ensembl(self):
        """Test the settings dump export by selecting 'ensembl' in the database selector form."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # select ensembl as transcript database (input is overlayed by the label)
        self.selenium.find_element_by_xpath('//label[@for="id_database_select_1"]').click()
        # obtain settings textarea and check if new setting was applied
        settings = json.loads(
            self.selenium.find_element_by_id("settingsDump").get_attribute("value")
        )
        self.assertEqual(settings["database_select"], "ensembl")

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_settings_import_database_refseq_to_ensembl(self):
        """Test the settings dump import by changing JSON field to 'ensembl' in the textarea."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # switch to settings tab and wait for it to be displayed
        self.selenium.find_element_by_id("more-tab").click()
        tab = self.selenium.find_element_by_id("settings-tab")
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(tab))
        tab.click()
        textarea = self.selenium.find_element_by_id("settingsDump")
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(textarea))
        # obtain initial settings from textarea
        settings_json = json.loads(textarea.get_attribute("value"))
        # change value
        settings_json["database_select"] = "ensembl"
        textarea.clear()
        textarea.send_keys(json.dumps(settings_json))
        self.selenium.find_element_by_id("settingsSet").click()
        # check if setting was applied
        self.assertTrue(
            self.selenium.find_element_by_xpath(
                '//input[@name="database_select" and @value="ensembl"]'
            ).is_selected()
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_display_loading(self):
        """Test if submitting the filter initiates the loading response."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # Wait until button is a submit button.
        WebDriverWait(self.selenium, self.wait_time).until(
            wait_for_the_attribute_value((By.ID, "submitFilter"), "data-event-type", "submit")
        )
        # Click button.
        button = self.selenium.find_element_by_id("submitFilter")
        button.click()
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.presence_of_element_located((By.ID, "logger"))
        )
        self.assertEqual(button.get_attribute("data-event-type"), "cancel")
        # Wait for background job to finish, otherwise database can't be flushed for next test.
        time.sleep(5)

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_display_cancel(self):
        """Test if submitting the filter can be canceled."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # Wait until button is a submit button.
        WebDriverWait(self.selenium, self.wait_time).until(
            wait_for_the_attribute_value((By.ID, "submitFilter"), "data-event-type", "submit")
        )
        # Find & hit button.
        button = self.selenium.find_element_by_id("submitFilter")
        button.click()
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.presence_of_element_located((By.ID, "logger"))
        )
        self.assertEqual(button.get_attribute("data-event-type"), "cancel")
        button.click()
        time.sleep(5)
        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_id("logger")
        self.assertEqual(
            self.selenium.find_element_by_id("resultsTable").get_attribute("innerHTML"), ""
        )
        self.assertEqual(button.get_attribute("data-event-type"), "submit")

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_display_results(self):
        """Test if submitting the filter yields the expected results."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        self._disable_filters("case")
        # hit submit button
        self.selenium.find_element_by_id("submitFilter").click()
        # wait for redirect
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-row"))
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_bookmark(self):
        """Test if submitting the filter yields the expected results."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        self._disable_filters("case")
        # hit submit button
        self.selenium.find_element_by_id("submitFilter").click()
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-row"))
        )
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-bookmark"))
        )
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-bookmark-comment-group"))
        ).click()
        # save bookmark
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "save"))
        ).click()
        WebDriverWait(self.selenium, self.wait_time).until(
            wait_for_the_attribute_endswith_value(
                (By.CLASS_NAME, "variant-bookmark"), "src", "/icons/fa-solid/bookmark.svg"
            )
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_multi_bookmark_one_variant(self):
        """Test if submitting the filter yields the expected results."""
        self._create_two_more_variants()

        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        self._disable_filters("case")
        # hit submit button
        self.selenium.find_element_by_id("submitFilter").click()
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "multivar-selector"))
        )
        multivar_btn = WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.ID, "multiVarButton"))
        )
        multivar_bookmark_link = WebDriverWait(self.selenium, self.wait_time).until(
            ec.presence_of_element_located((By.ID, "multivar-bookmark-comment"))
        )
        WebDriverWait(self.selenium, self.wait_time).until(
            element_has_class(multivar_btn, "btn-outline-secondary")
        )

        selectors = self.selenium.find_elements_by_class_name("multivar-selector")

        # check if buttons are disabled
        self.assertIn("btn-outline-secondary", multivar_btn.get_attribute("class"))
        self.assertIn("disabled", multivar_bookmark_link.get_attribute("class"))

        # select the first variant
        selectors[0].click()
        self.assertTrue(selectors[0].is_selected())

        # buttons should still be disabled
        self.assertIn("btn-outline-secondary", multivar_btn.get_attribute("class"))
        self.assertIn("disabled", multivar_bookmark_link.get_attribute("class"))

        # select the second variant
        selectors[1].click()
        self.assertTrue(selectors[1].is_selected())
        self.assertFalse(selectors[2].is_selected())

        # buttons should be active
        self.assertIn("btn-secondary", multivar_btn.get_attribute("class"))
        self.assertNotIn("disabled", multivar_bookmark_link.get_attribute("class"))

        # open form
        multivar_btn.click()
        multivar_bookmark_link.click()

        # check displayed form
        info_box = WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='multiVarBookmarkCommentModalContent']/div[contains(@class, 'alert-info')]",
                )
            )
        )
        _strong = WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='multiVarBookmarkCommentModalContent']/div[contains(@class, 'alert-info')]/strong",
                )
            )
        )
        # The following is timing sensitive, having strong is good enough.
        # self.assertEqual("2 variants selected.", info_box.text)

        # save bookmark
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "save"))
        ).click()

        # check bookmark set for variant 1
        WebDriverWait(self.selenium, self.wait_time).until(
            wait_for_element_endswith_value(
                selectors[0].find_element_by_xpath(
                    "../following-sibling::td[contains(@class, 'bookmark')]/a/img[contains(@class, 'variant-bookmark')]"
                ),
                "src",
                "/icons/fa-solid/bookmark.svg",
            )
        )
        # check bookmark set for variant 2
        WebDriverWait(self.selenium, self.wait_time).until(
            wait_for_element_endswith_value(
                selectors[1].find_element_by_xpath(
                    "../following-sibling::td[contains(@class, 'bookmark')]/a/img[contains(@class, 'variant-bookmark')]"
                ),
                "src",
                "/icons/fa-solid/bookmark.svg",
            )
        )
        # check if bookmark NOT set for variant 3
        self.assertTrue(
            selectors[2]
            .find_element_by_xpath(
                "../following-sibling::td[contains(@class, 'bookmark')]/a/img[contains(@class, 'variant-bookmark')]"
            )
            .get_attribute("src")
            .endswith("/icons/fa-regular/bookmark.svg")
        )

        # un-select variant 1
        selectors[0].click()
        self.assertFalse(selectors[0].is_selected())
        self.assertTrue(selectors[1].is_selected())

        # select variant 3
        selectors[2].click()
        self.assertTrue(selectors[2].is_selected())

        # open form again
        multivar_btn.click()
        multivar_bookmark_link.click()

        # select checkered flag
        comment_check_flag = WebDriverWait(self.selenium, self.wait_time).until(
            ec.element_to_be_clickable((By.ID, "comment-check-flag"))
        )
        comment_check_flag.click()

        # select visual positive flag
        comment_radio_visual_positive = WebDriverWait(self.selenium, self.wait_time).until(
            ec.element_to_be_clickable((By.ID, "comment-radio-visual-positive"))
        )
        comment_radio_visual_positive.click()

        # save form
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "save"))
        ).click()

        # select variant 1 (all three are now selected)
        selectors[0].click()
        self.assertTrue(selectors[0].is_selected())

        # open form again
        multivar_btn.click()
        multivar_bookmark_link.click()

        # check displayed form -- warning expected
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='multiVarBookmarkCommentModalContent']/div[contains(@class, 'alert-warning')]",
                )
            )
        )
        info_box = WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='multiVarBookmarkCommentModalContent']/div[contains(@class, 'alert-info')]",
                )
            )
        )
        self.assertEqual("3 variants selected.", info_box.text)

        # get highlighted flags
        flags_radios = self.selenium.find_elements_by_xpath(
            "//div[@id='multiVarBookmarkCommentModalContent']/form/div[contains(@class, 'alert-warning')]"
        )
        flags_checkboxes = self.selenium.find_elements_by_xpath(
            "//div[@id='multiVarBookmarkCommentModalContent']/form/div/div/div[contains(@class, 'alert-warning')]"
        )

        # check for correct number of highlighted flags
        self.assertEqual(len(flags_radios), 1)
        self.assertEqual(len(flags_checkboxes), 1)

        # check if correct flags where highlighted
        self.assertEqual(flags_radios[0].text, "Visual")
        self.assertEqual(
            flags_checkboxes[0].find_element_by_xpath(".//input").get_attribute("id"),
            "comment-check-flag",
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_training_mode(self):
        """Test if submitting the filter yields the expected results."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        self._disable_filters("case")
        # hit submit button
        self.selenium.find_element_by_id("submitFilter").click()
        # wait for redirect
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-row"))
        )
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-bookmark"))
        )
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-bookmark-comment-group"))
        ).click()
        # save bookmark
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "save"))
        ).click()
        WebDriverWait(self.selenium, self.wait_time).until(
            wait_for_the_attribute_endswith_value(
                (By.CLASS_NAME, "variant-bookmark"), "src", "/icons/fa-solid/bookmark.svg"
            )
        )
        # switch tab
        self.selenium.find_element_by_id("more-tab").click()
        tab = self.selenium.find_element_by_id("misc-tab")
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(tab))
        tab.click()
        # enable training mode
        training = self.selenium.find_element_by_id("id_training_mode")
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(training))
        training.click()
        # hit submit button
        self.selenium.find_element_by_id("submitFilter").click()
        # wait for redirect
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-row"))
        )
        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_class_name("bookmark")

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_download(self):
        """Test if submitting the download filter is kicked off."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # switch tab
        self.selenium.find_element_by_id("frequency-tab").click()
        exomes = self.selenium.find_element_by_xpath("//input[@name='gnomad_exomes_enabled']")
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(exomes))
        # disable exac and thousand genomes frequency filter
        exomes.click()
        self.selenium.find_element_by_xpath("//input[@name='gnomad_genomes_enabled']").click()
        # switch tab
        self.selenium.find_element_by_id("more-tab").click()
        self.selenium.find_element_by_id("quality-tab").click()
        dropdown = self.selenium.find_element_by_id("id_%s_fail" % self.case.index)
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(dropdown))
        # disable quality filters
        dropdown.click()
        option = self.selenium.find_element_by_xpath("//option[@value='ignore']")
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(option))
        option.click()
        # find and hit download button
        self.selenium.find_element_by_id("filterdisplayoptions").click()
        download = self.selenium.find_element_by_xpath(
            '//button[@name="submit" and @value="download"]'
        )
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(download))
        download.click()
        # wait for redirect and refresh page for elements to show up
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located(
                (By.XPATH, '//h2[contains(text(), "{}")]'.format("Background File Creation Job"))
            )
        )
        time.sleep(5)
        self.selenium.refresh()
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located(
                (
                    By.XPATH,
                    '//div[contains(text(), "{}")]'.format("Exporting single case to file started"),
                )
            )
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_preset_de_novo_on_quality_settings(self):
        """Test de novo preset on a quality setting"""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # select medgen relaxed preset
        self.selenium.find_element_by_id("quick-presets-button").click()
        self.selenium.find_element_by_xpath("//a[@data-preset-name='de-novo']").click()
        # verify correctness
        self.assertEquals(
            self.selenium.find_element_by_id("id_%s_dp_het" % self.case.index).get_attribute(
                "value"
            ),
            "10",
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_preset_dominant_on_quality_settings(self):
        """Test medgen dominant preset on a quality setting"""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # select medgen clinvar preset
        self.selenium.find_element_by_id("quick-presets-button").click()
        self.selenium.find_element_by_xpath("//a[@data-preset-name='dominant']").click()
        # verify correctness
        self.assertEqual(
            self.selenium.find_element_by_id("id_%s_fail" % self.case.index).get_attribute("value"),
            "drop-variant",
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_preset_whole_exome_on_effect_settings(self):
        """Test whole exome preset on the all effect setting"""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        # select whole exome preset
        self.selenium.find_element_by_id("quick-presets-button").click()
        self.selenium.find_element_by_xpath("//a[@data-preset-name='whole-exome']").click()
        # verify correctness
        self.assertTrue(self.selenium.find_element_by_id("id_effect_group_all").is_selected())

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_invalid_form_input_error_rendering(self):
        """Test if invalid form input triggers visual error response rendering."""
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        button = self.selenium.find_element_by_id("submitFilter")
        # create wrong setting
        tab = self.selenium.find_element_by_id("frequency-tab")
        tab.click()
        field = self.selenium.find_element_by_xpath("//input[@name='gnomad_exomes_frequency']")
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(field))
        field.clear()
        field.send_keys("10")
        # submit
        button.click()
        time.sleep(5)
        # check for correct error rendering
        self.assertIn("border-danger", tab.get_attribute("class").split())
        self.assertIn("border-danger", field.get_attribute("class").split())

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_corrected_invalid_form_input_error_rendering(self):
        """Test if visual error response rendering is removed when correcting invalid input."""
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        button = self.selenium.find_element_by_id("submitFilter")
        # create wrong setting
        tab = self.selenium.find_element_by_id("frequency-tab")
        tab.click()
        field = self.selenium.find_element_by_xpath("//input[@name='gnomad_exomes_frequency']")
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(field))
        field.clear()
        field.send_keys("10")
        # submit
        button.click()
        time.sleep(5)
        # correct invalid input
        field.clear()
        field.send_keys("0.1")
        button.click()
        time.sleep(5)
        self.assertNotIn("border-danger", tab.get_attribute("class").split())
        self.assertNotIn("border-danger", field.get_attribute("class").split())


class TestVariantsProjectCasesFilterView(TestUIBase):
    """Tests for the variants joint filter view."""

    view = "variants:project-cases-filter"

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        variant_sets = [None, None]
        _, variant_sets[0], _ = CaseWithVariantSetFactory.get("small", project=self.project)
        _, variant_sets[1], _ = CaseWithVariantSetFactory.get("small", project=self.project)
        SmallVariantFactory(variant_set=variant_sets[0])
        SmallVariantFactory(variant_set=variant_sets[1])
        for variant_set in variant_sets:
            update_variant_counts(variant_set.case)

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_joint_filter_display_loading(self):
        """Test if submitting the filter initiates the loading response."""
        # login
        self.compile_url_and_login({"project": self.project.sodar_uuid})
        # Wait until button is a submit button.
        WebDriverWait(self.selenium, self.wait_time).until(
            wait_for_the_attribute_value((By.ID, "submitFilter"), "data-event-type", "submit")
        )
        # find & hit button
        button = self.selenium.find_element_by_id("submitFilter")
        button.click()
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.presence_of_element_located((By.ID, "logger"))
        )
        self.assertEqual(button.get_attribute("data-event-type"), "cancel")
        # Wait for background job to finish, otherwise database can't be flushed for next test.
        time.sleep(5)

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_joint_filter_display_cancel(self):
        """Test if submitting the filter can be canceled."""
        # login
        self.compile_url_and_login({"project": self.project.sodar_uuid})
        # Wait until button is a submit button.
        WebDriverWait(self.selenium, self.wait_time).until(
            wait_for_the_attribute_value((By.ID, "submitFilter"), "data-event-type", "submit")
        )
        # find & hit button
        button = self.selenium.find_element_by_id("submitFilter")
        button.click()
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.presence_of_element_located((By.ID, "logger"))
        )
        self.assertEqual(button.get_attribute("data-event-type"), "cancel")
        button.click()
        time.sleep(5)
        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_id("logger")
        self.assertEqual(
            self.selenium.find_element_by_id("resultsTable").get_attribute("innerHTML"), ""
        )
        self.assertEqual(button.get_attribute("data-event-type"), "submit")

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_joint_filter_display_results(self):
        """Test if submitting the filter yields the expected results."""
        # login
        self.compile_url_and_login({"project": self.project.sodar_uuid})
        self._disable_filters("project")
        # hit submit button
        self.selenium.find_element_by_id("submitFilter").click()
        # wait for redirect
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-row"))
        )

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_joint_filter_download(self):
        """Test if submitting the download filter is kicked off."""
        # login
        self.compile_url_and_login({"project": self.project.sodar_uuid})
        self._disable_filters("project")
        # find and hit download button
        self.selenium.find_element_by_id("filterdisplayoptions").click()
        download = self.selenium.find_element_by_xpath(
            '//button[@name="submit" and @value="download"]'
        )
        WebDriverWait(self.selenium, self.wait_time).until(ec.visibility_of(download))
        download.click()
        # wait for redirect and refresh page for elements to show up
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located(
                (By.XPATH, '//h2[contains(text(), "{}")]'.format("Background File Creation Job"))
            )
        )
        time.sleep(5)
        self.selenium.refresh()
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located(
                (
                    By.XPATH,
                    '//div[contains(text(), "{}")]'.format("Exporting all project cases to file"),
                )
            )
        )


class TestVariantsCaseFilterViewExtraAnno(TestVariantsCaseFilterView):
    """Tests for the variants case filter view."""

    view = "variants:case-filter"
    window_size = (4000, 1300)

    def setUp(self):
        super().setUp()
        self.case, self.variant_set, _ = CaseWithVariantSetFactory.get("small")
        small_vars = SmallVariantFactory.create_batch(3, variant_set=self.variant_set)
        self.extra_anno = [
            ExtraAnnoFactory(
                release=small_vars[0].release,
                chromosome=small_vars[0].chromosome,
                start=small_vars[0].start,
                end=small_vars[0].end,
                bin=small_vars[0].bin,
                reference=small_vars[0].reference,
                alternative=small_vars[0].alternative,
                anno_data=[9, 19],
            ),
            ExtraAnnoFactory(
                release=small_vars[2].release,
                chromosome=small_vars[2].chromosome,
                start=small_vars[2].start,
                end=small_vars[2].end,
                bin=small_vars[2].bin,
                reference=small_vars[2].reference,
                alternative=small_vars[2].alternative,
                anno_data=[10, 19],
            ),
        ]
        self.extra_anno_fields = [
            ExtraAnnoFieldFactory(),
            ExtraAnnoFieldFactory(),
        ]
        self.extra_anno_field = self.extra_anno_fields[0]

    def _find_table_column_names(self):
        table = self.selenium.find_element_by_id("table-config")
        row_header = table.find_element_by_xpath('//*[@id="main"]/thead/tr[2]')
        row_header_items = row_header.find_elements_by_tag_name("th")
        row_header_values = [i.text for i in row_header_items]
        return table, row_header_items, row_header_values

    @skipIf(SKIP_SELENIUM, SKIP_SELENIUM_MESSAGE)
    def test_variant_filter_case_display_results_extra_anno(self):
        """Test if submitting the filter yields the expected results."""
        # login
        self.compile_url_and_login(
            {"project": self.case.project.sodar_uuid, "case": self.case.sodar_uuid}
        )
        self._disable_filters("case")
        # hit submit button
        self.selenium.find_element_by_id("submitFilter").click()
        # wait for redirect
        WebDriverWait(self.selenium, self.wait_time).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "variant-row"))
        )

        # only Effect is on, everything else (extra anno) off
        bt = self.selenium.find_element_by_xpath(
            '//*[@id="resultsTable"]/div[2]/div/div[4]/div/button'
        )
        self.assertTrue(bt.get_attribute("title"), "Effect")

        bt.click()
        columns_elements = self.selenium.find_element_by_xpath(
            '//*[@id="resultsTable"]/div[2]/div/div[4]/div/div'
        )

        # any extra_anno_field missing in Columns
        columns_items = columns_elements.find_elements_by_tag_name("li")
        columns_values = [i.text for i in columns_items]
        self.assertTrue(self.extra_anno_field.label in columns_values)

        # click only extra anno
        extra_anno_columns_item = None
        for column_item in columns_items:
            if column_item.text == self.extra_anno_field.label:
                extra_anno_columns_item = column_item
        self.assertIsNotNone(extra_anno_columns_item)
        extra_anno_columns_item.click()

        # find extra anno column header in the table
        table, row_header_items, row_header_values = self._find_table_column_names()
        self.assertTrue(self.extra_anno_field.label in row_header_values)

        # get extra anno header element
        extra_anno_table_header = [
            i for i in row_header_items if i.text == self.extra_anno_field.label
        ][0]

        # check extra anno values
        row_extra_anno_items = table.find_elements_by_class_name("extra_annos-1")
        # remove header name, missing values and empty row value from extra anno values
        remove_from_extra_anno_values = [self.extra_anno_field.label, "-", ""]
        row_extra_anno_values = [
            float(i.text)
            for i in row_extra_anno_items
            if i.text not in remove_from_extra_anno_values
        ]
        # click sort extra anno and see if sorted
        extra_anno_table_header.click()
        row_extra_anno_items_sorted = table.find_elements_by_class_name("extra_annos-1")
        row_extra_anno_values_sorted = [
            float(i.text)
            for i in row_extra_anno_items_sorted
            if i.text not in remove_from_extra_anno_values
        ]

        row_extra_anno_values.sort()
        self.assertTrue(row_extra_anno_values, row_extra_anno_values_sorted)

        # against the database
        row_extra_anno_values_db = [float(i.anno_data[0]) for i in self.extra_anno]
        row_extra_anno_values_db.sort()
        self.assertTrue(row_extra_anno_values_db, row_extra_anno_values_sorted)

        # click to hide extra anno
        bt.click()
        extra_anno_columns_item.click()
        # extra anno column header hidden in the table
        table, row_header_items, row_header_values = self._find_table_column_names()
        self.assertFalse(self.extra_anno_field.label in row_header_values)
