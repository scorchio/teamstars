import datetime

from django.contrib.auth.models import User
from mock import Mock, patch, PropertyMock
from unittest import TestCase

from common.models import Profile
from common.social_auth_pipeline import save_fb_profile, save_profile_picture
from common.tests.api.test_api_auth import TEST_USER, TEST_PASSWORD


class SaveFacebookProfileTestCase(TestCase):
    def setUp(self):
        self.mock_backend = Mock()
        self.mock_backend.name = 'facebook'
        self.mock_user = Mock()
        self.mock_response_full = {
            'link': 'http://whatever',
            'birthday': '12/31/1999',
            'location': {'name': 'somewhere'},
        }
        self.mock_response_partial = {
            'link': 'http://whatever',
        }

    def test_handle_full_profile_response(self):
        with patch('common.social_auth_pipeline.Profile.objects.update_or_create') as mock_profile_update:
            save_fb_profile(self.mock_backend, self.mock_user, self.mock_response_full)

        mock_profile_update.assert_called_once_with(user=self.mock_user, defaults={
            'fb_link': 'http://whatever',
            'birthday': datetime.datetime(1999, 12, 31),
            'location': 'somewhere',
        })

    def test_handle_partial_profile_response(self):
        with patch('common.social_auth_pipeline.Profile.objects.update_or_create') as mock_profile_update:
            save_fb_profile(self.mock_backend, self.mock_user, self.mock_response_partial)

        mock_profile_update.assert_called_once_with(user=self.mock_user, defaults={
            'fb_link': 'http://whatever',
            'birthday': None,
            'location': None,
        })

    def test_partial_response_flow_for_no_profile(self):
        """Validates that it's possible to save a profile when the profile didn't exist
         before and we only have partial data (just the FB link)."""
        user = User.objects.create_user(username=TEST_USER, password=TEST_PASSWORD)
        save_fb_profile(self.mock_backend, user, self.mock_response_partial)
        profile = Profile.objects.first()
        self.assertEqual(profile.fb_link, self.mock_response_full['link'])


class SaveFacebookPictureTestCase(TestCase):
    def setUp(self):
        self.mock_backend = Mock()
        self.mock_backend.name = 'facebook'
        self.user = User.objects.create_user(username=TEST_USER, password=TEST_PASSWORD)
        self.mock_request = patch('common.social_auth_pipeline.request')
        self.mock_request.return_value = Mock(status_code=200, content='')
        self.mock_response = {'id': '1111'}

    def test_save_picture_flow(self):
        self.assertIsNone(self.user.profile.photo.name)
        save_profile_picture(self.mock_backend, self.user, self.mock_response, None)
        self.assertTrue(self.user.profile.photo.name.startswith('./avatar_{id}'.format(id=self.user.id)), )

    @patch('common.social_auth_pipeline.ContentFile')
    def test_save_picture_no_image_yet(self, mock_file):
        mock_user = Mock()
        mock_user.id = 1
        mock_file.return_value = 'cfile'
        save_profile_picture(self.mock_backend, mock_user, self.mock_response, None)
        mock_user.profile.photo.save.assert_called_once_with('avatar_1.jpg', 'cfile', save=True)

    def tearDown(self):
        self.user.profile.photo.delete()
        self.user.delete()
