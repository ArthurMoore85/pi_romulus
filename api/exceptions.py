# -*- coding: utf-8 -*-
"""
.. module:: .exceptions.py
    :synopsis: API Exceptions

.. moduleauthor:: Arthur Moore <arthur.moore85@gmail.com>
.. creation date:: 27-10-2017
.. licence:: 
"""
from __future__ import unicode_literals

__author__ = "arthur"


class ApiException(Exception):
    """
    Base exception for all non-specific exceptions
    """
    pass


class ForbiddenException(ApiException):
    """
    Raised when a 403 response is received
    """
    pass


class NotFoundException(ApiException):
    """
    Raised when a 404 response is received
    """
    pass


class MovedException(ApiException):
    """
    Raised when a 301 response is received
    """
    pass


class RedirectException(ApiException):
    """
    Raised when a 307 response is received
    """
    pass


class UnauthorizedException(ApiException):
    """
    Raised when a 401 response is received.
    """
    pass


class InternalServerException(ApiException):
    """
    Raised when a 500 response is received.
    """
    pass


class UnavailableException(ApiException):
    """
    Raised when a 503 response is received.
    """
    pass


class MissingEndpointException(ApiException):
    """
    Raised when endpoint is missing.
    """
    pass


class UnknownURLException(ApiException):
    """
    Raised when the base URL is missing.
    """
    pass


def handle_response_codes(status_code):
    """
    Handles the exceptions for various types of
    responses.
    :param status_code:
    :return:
    """
    if status_code == 404:
        raise NotFoundException(
            'URL provided could not be found'
        )
    elif status_code == 403:
        raise ForbiddenException(
            'URL access is forbidden'
        )
    elif status_code == 301:
        raise MovedException(
            'URL permanently moved'
        )
    elif status_code == 307:
        raise RedirectException(
            'URL is temporarily redirected'
        )
    elif status_code == 401:
        raise UnauthorizedException(
            'You are unauthorized to view this URL'
        )
    elif status_code == 500:
        raise InternalServerException(
            'The remote server encountered an internal server error'
        )
    elif status_code == 503:
        raise UnavailableException(
            'URL is unavailable.'
        )
    elif status_code == 'missing_endpoint':
        raise MissingEndpointException(
            'Endpoint could not be found.'
        )
    elif status_code == 'missing_base_url':
        raise UnknownURLException(
            'Base URL has not been set.'
        )
    else:
        raise ApiException('An error occurred')
