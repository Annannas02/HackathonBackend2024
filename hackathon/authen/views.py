from django.contrib.auth import hashers
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import pyotp
from otp.models import OTP
from users.serializers import UserSerializer
from users import models as usermodels
from authen import serializers
from datetime import timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import hashlib
import os

#USER REGISTRATION
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    phone = request.data.get("phone")
    username = request.data.get("username")
    unhashed_password = request.data.get("password")


    hashed_password = hashers.make_password(unhashed_password)
    secret = pyotp.random_base32()
    
    user = usermodels.User.objects.create(
        username=username,
        password=hashed_password
    )

    user_serialized = UserSerializer(user)
    return Response({"message" : "User created successfully", "user": user_serialized.data}, status=status.HTTP_200_OK)

#GENERATION OF TOTP
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_totp(request):
    serializer = serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        try:
            user = usermodels.User.objects.get(username=serializer.data["username"])
            if user.check_password(serializer.data['password']) is False:
                return response.Response('Password is incorrect.',
                                        status=status.HTTP_400_BAD_REQUEST)

        except user.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )


        # Create a TOTP instance with the provided secret
        totp = pyotp.TOTP('base32secret3232')
        totp_code = totp.now()
        
        # Attempt to get an existing OTP entry for the user
        otp_entry = OTP.objects.filter(personid=user).first()

        if otp_entry:
            # Update the timestamp and phone for the existing entry
            otp_entry.timestamp = timezone.now()
            otp_entry.save()
        else:
            # Create a new OTP entry if none exists
            OTP.objects.create(personid=user, timestamp=timezone.now())
            

            #, "user_id": user.id
        return Response({"totp_code": totp_code}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
        

# VALIDATION OF INPUTTED OTP VS GIVEN OTP
@api_view(['POST'])
@permission_classes([AllowAny])
def authenticate_2fa(request):
    otp = request.data.get('totp_code')


    if not otp:
        return Response(
            {"error": "OTP is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = usermodels.User.objects.get(username=request.data.get("username"))

    try:
    # Verify if the user has an associated OTP entry
        otp_entry = OTP.objects.filter(personid=user).first()

        if not otp_entry:
            return Response(
                {"error": "No OTP entry found for the user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        totp = pyotp.TOTP('base32secret3232')

        # Compare the provided OTP with the OTP associated with the timestamp in the database
        if otp==totp.at(for_time=otp_entry.timestamp):
            
            refresh = RefreshToken.for_user(user=user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return response.Response(
                {'tokens': tokens},
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                {"error": "Invalid OTP. Authentication failed."},
                status=status.HTTP_401_UNAUTHORIZED
            )


    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
