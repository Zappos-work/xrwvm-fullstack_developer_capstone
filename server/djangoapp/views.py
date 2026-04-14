from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

import logging
import json

# from .populate import initiate

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({
            "status": False,
            "error": "Invalid request method"
        }, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName", "")
        password = data.get("password", "")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })

        return JsonResponse({
            "userName": username,
            "status": False
        }, status=401)

    except Exception as exc:
        logger.error("login_user error: %s", exc)
        return JsonResponse({
            "status": False,
            "error": "Login failed"
        }, status=500)


def logout_request(request):
    if request.method != "GET":
        return JsonResponse({
            "status": False,
            "error": "Invalid request method"
        }, status=405)

    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({
            "status": False,
            "error": "Invalid request method"
        }, status=405)

    try:
        data = json.loads(request.body)

        username = data.get("userName", "").strip()
        password = data.get("password", "")
        first_name = data.get("firstName", "").strip()
        last_name = data.get("lastName", "").strip()
        email = data.get("email", "").strip()

        if not username or not password:
            return JsonResponse({
                "status": False,
                "error": "Username and password are required"
            }, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "error": "Already Registered"
            }, status=409)

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        login(request, user)

        return JsonResponse({
            "userName": username,
            "status": True
        })

    except Exception as exc:
        logger.error("registration error: %s", exc)
        return JsonResponse({
            "status": False,
            "error": "Registration failed"
        }, status=500)


# Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
#     ...


# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request, dealer_id):
#     ...


# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
#     ...


# Create a `add_review` view to submit a review
# def add_review(request):
#     ...