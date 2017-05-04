import logging

from django.test.runner import DiscoverRunner


class NoLoggingTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):

        # disable logging below CRITICAL while testing
        logging.disable(logging.CRITICAL)

        return super(NoLoggingTestRunner, self).run_tests(test_labels, extra_tests, **kwargs)
