from django.urls import reverse
from projectroles.tests.test_permissions_api import TestProjectAPIPermissionBase

from cohorts.models import CohortCase
from cohorts.tests.factories import CohortCaseFactory, CohortFactory
from variants.tests.factories import CaseFactory


class TestCohortApiView(TestProjectAPIPermissionBase):
    """Permission tests for the API views dealing with ``Case``."""

    def setUp(self):
        super().setUp()
        self.cohort = CohortFactory(project=self.project, user=self.contributor_as.user)
        self.cases = CaseFactory.create_batch(2, project=self.project)

    def test_list(self):
        url = reverse(
            "cohorts:ajax-cohort-list-create",
            kwargs={"project": self.project.sodar_uuid},
        )
        good_users = [
            self.superuser,
            self.owner_as.user,
            self.delegate_as.user,
            self.contributor_as.user,
            self.guest_as.user,
        ]
        bad_users = [self.anonymous, self.user_no_roles]
        self.assert_response(url, good_users, 200, method="GET")
        self.assert_response(url, bad_users, 403, method="GET")

    def test_create(self):
        url = reverse(
            "cohorts:ajax-cohort-list-create",
            kwargs={"project": self.project.sodar_uuid},
        )
        good_users = [
            self.superuser,
            self.owner_as.user,
            self.delegate_as.user,
            self.contributor_as.user,
        ]
        bad_users = [self.guest_as.user, self.user_no_roles, self.anonymous]  # Forbidden
        data = {"name": "New Cohort", "cases": [str(case.sodar_uuid) for case in self.cases]}
        self.assert_response(url, good_users, 201, method="POST", data=data)
        self.assert_response(url, bad_users, 403, method="POST", data=data)

    def test_update(self):
        url = reverse(
            "cohorts:ajax-cohort-retrieve-update-destroy",
            kwargs={"cohort": self.cohort.sodar_uuid},
        )
        good_users = [
            self.superuser,
            self.contributor_as.user,
        ]
        bad_users = [
            self.owner_as.user,
            self.delegate_as.user,
            self.guest_as.user,
            self.user_no_roles,
            self.anonymous,
        ]
        data = {"name": "Updated name", "cases": [str(case.sodar_uuid) for case in self.cases]}
        self.assert_response(url, good_users, 200, method="PUT", data=data)
        self.assert_response(url, bad_users, 403, method="PUT", data=data)

    def test_destroy(self):
        cohort_uuid = self.cohort.sodar_uuid
        url = reverse(
            "cohorts:ajax-cohort-retrieve-update-destroy",
            kwargs={"cohort": cohort_uuid},
        )
        good_users = [
            self.superuser,
            self.contributor_as.user,
        ]
        bad_users = [
            self.owner_as.user,
            self.delegate_as.user,
            self.guest_as.user,
            self.user_no_roles,
            self.anonymous,
        ]

        def restore_cohort():
            CohortFactory(
                sodar_uuid=cohort_uuid, project=self.project, user=self.contributor_as.user
            )

        self.assert_response(url, good_users, 204, method="DELETE", cleanup_method=restore_cohort)
        self.assert_response(url, bad_users, 403, method="DELETE")


class TestAccessibleProjectsCasesApiView(TestProjectAPIPermissionBase):
    """Permission tests for the API views listing accessible projects included cases."""

    def setUp(self):
        super().setUp()
        self.cohort = CohortFactory(project=self.project)
        self.cases = CaseFactory.create_batch(2, project=self.project)

    def test_list(self):
        url = reverse(
            "cohorts:ajax-accessible-projects-cases-list",
            kwargs={"project": self.project.sodar_uuid},
        )
        good_users = [
            self.superuser,
            self.owner_as.user,
            self.delegate_as.user,
            self.contributor_as.user,
            self.guest_as.user,
        ]
        bad_users = [self.user_no_roles, self.anonymous]
        self.assert_response(url, good_users, 200, method="GET")
        self.assert_response(url, bad_users, 403, method="GET")


class TestCohortCaseApiView(TestProjectAPIPermissionBase):
    """Permission tests for the API views dealing with ``CohortCase``."""

    def setUp(self):
        super().setUp()
        self.cohort = CohortFactory(project=self.project, user=self.contributor_as.user)
        self.cases = CaseFactory.create_batch(3, project=self.project)
        self.cohortcases = [
            CohortCaseFactory(cohort=self.cohort, case=self.cases[0]),
            CohortCaseFactory(cohort=self.cohort, case=self.cases[1]),
        ]

    def test_list(self):
        url = reverse(
            "cohorts:ajax-cohortcase-list",
            kwargs={"cohort": self.cohort.sodar_uuid},
        )
        good_users = [
            self.superuser,
            self.owner_as.user,
            self.delegate_as.user,
            self.contributor_as.user,
            self.guest_as.user,
        ]
        bad_users = [self.user_no_roles, self.anonymous]
        self.assert_response(url, good_users, 200, method="GET")
        self.assert_response(url, bad_users, 403, method="GET")

    def test_create(self):
        url = reverse(
            "cohorts:ajax-cohortcase-create",
            kwargs={"project": self.project.sodar_uuid},
        )
        good_users = [
            self.superuser,
            self.owner_as.user,
            self.delegate_as.user,
            self.contributor_as.user,
        ]
        bad_users = [self.guest_as.user, self.user_no_roles, self.anonymous]  # Forbidden
        data = {"cohort": self.cohort.sodar_uuid, "case": self.cases[2].sodar_uuid}

        def remove_cohortcase():
            CohortCase.objects.last().delete()

        self.assert_response(
            url, good_users, 201, method="POST", data=data, cleanup_method=remove_cohortcase
        )
        self.assert_response(url, bad_users, 403, method="POST", data=data)

    def test_destroy(self):
        cohortcase_uuid = self.cohortcases[0].sodar_uuid
        url = reverse(
            "cohorts:ajax-cohortcase-destroy",
            kwargs={"cohortcase": cohortcase_uuid},
        )
        good_users = [
            self.superuser,
            self.contributor_as.user,
        ]
        bad_users = [
            self.owner_as.user,
            self.delegate_as.user,
            self.guest_as.user,
            self.user_no_roles,
            self.anonymous,
        ]

        def restore_cohortcase():
            CohortCaseFactory(sodar_uuid=cohortcase_uuid, cohort=self.cohort, case=self.cases[0])

        self.assert_response(
            url, good_users, 204, method="DELETE", cleanup_method=restore_cohortcase
        )
        self.assert_response(url, bad_users, 403, method="DELETE")
