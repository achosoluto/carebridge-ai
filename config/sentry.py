"""
Sentry error tracking configuration
"""
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

def init_sentry():
    """Initialize Sentry error tracking"""
    sentry_dsn = os.getenv('SENTRY_DSN')
    environment = os.getenv('ENVIRONMENT', 'development')

    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[DjangoIntegration()],

            # Performance monitoring
            traces_sample_rate=0.1,  # 10% of transactions

            # Error sampling
            sample_rate=1.0,  # 100% of errors

            # Environment
            environment=environment,

            # Release tracking
            release=os.getenv('GIT_COMMIT', 'unknown'),

            # Send PII (for debugging, disable in production if needed)
            send_default_pii=True,
        )