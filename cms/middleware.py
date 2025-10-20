import traceback
import logging
from django.utils.deprecation import MiddlewareMixin
from .models import ErrorLog

logger = logging.getLogger(__name__)


class ErrorLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log errors to database for admin viewing
    """

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception
        """
        try:
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')

            # Get username
            user = str(request.user.username) if request.user.is_authenticated else 'Anonymous'

            # Get user agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # Get full traceback
            tb = traceback.format_exc()

            # Determine severity based on exception type
            severity = 'ERROR'
            if isinstance(exception, (KeyboardInterrupt, SystemExit)):
                severity = 'CRITICAL'
            elif isinstance(exception, (ValueError, TypeError, AttributeError)):
                severity = 'ERROR'
            elif isinstance(exception, PermissionError):
                severity = 'WARNING'

            # Create error log entry
            ErrorLog.objects.create(
                severity=severity,
                message=str(exception),
                path=request.path,
                method=request.method,
                user=user,
                ip_address=ip_address,
                user_agent=user_agent[:1000],  # Limit length
                exception_type=exception.__class__.__name__,
                traceback=tb,
                resolved=False
            )

        except Exception as e:
            # Don't let logging errors break the application
            logger.error(f"Failed to log error to database: {e}")

        # Return None to allow normal error handling to continue
        return None


class Custom404Middleware(MiddlewareMixin):
    """
    Log 404 errors to database
    """

    def process_response(self, request, response):
        """
        Log 404 responses
        """
        if response.status_code == 404 and not request.path.startswith('/media/') and not request.path.startswith('/static/'):
            try:
                # Get client IP
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip_address = x_forwarded_for.split(',')[0]
                else:
                    ip_address = request.META.get('REMOTE_ADDR')

                user = str(request.user.username) if request.user.is_authenticated else 'Anonymous'
                user_agent = request.META.get('HTTP_USER_AGENT', '')

                ErrorLog.objects.create(
                    severity='WARNING',
                    message=f'Page not found: {request.path}',
                    path=request.path,
                    method=request.method,
                    user=user,
                    ip_address=ip_address,
                    user_agent=user_agent[:1000],
                    exception_type='Http404',
                    traceback='',
                    resolved=False
                )
            except Exception as e:
                logger.error(f"Failed to log 404 error: {e}")

        return response
