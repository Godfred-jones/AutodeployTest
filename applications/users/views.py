# import pyotp
# from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import default_token_generator
# from django.http import Http404
# from django.utils.crypto import get_random_string
# from django.utils.timezone import now
# from djoser.compat import get_user_email
# from djoser.conf import settings as djoser_settings
# from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import (
#     CreateModelMixin,
#     DestroyModelMixin,
#     ListModelMixin,
#     RetrieveModelMixin,
#     UpdateModelMixin,
# )
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.viewsets import GenericViewSet

# from applications.common.utils import encode_uid
# from applications.events.models import Event
# from applications.users.models import User as UserObj

# from .models import UtilityAccountProfile
# from .serializers import (
#     CreateUserSerializer,
#     CreateUtilityAccountResponseSerializer,
#     CreateUtilityAccountSerializer,
#     ForgotPasswordSerializer,
#     ResetPasswordSerializer,
#     ReturnSecretSerializer,
#     ReturnUidAndTokenSerializer,
#     UserSerializer,
#     UtilityAccountProfileSerializer,
#     UtilityAccountProfileUpdateSerializer,
#     VerifyResetEmailSerializer,
# )


# def generate_otp(secret=None):
#     totp = pyotp.TOTP(secret, interval=180)
#     return totp.now()


# User = get_user_model()


# class UserViewSet(
#     RetrieveModelMixin,
#     ListModelMixin,
#     UpdateModelMixin,
#     CreateModelMixin,
#     DestroyModelMixin,
#     GenericViewSet,
# ):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     lookup_field = "id"

#     # def get_queryset(self, *args, **kwargs):
#     #     return self.queryset.filter(id=self.request.user.id)

#     def get_serializer_class(self):
#         if self.action == "create":
#             return CreateUserSerializer
#         return super().get_serializer_class()

#     # @action(detail=False, methods=["GET"])
#     # def me(self, request):
#     #     serializer = UserSerializer(request.user, context={"request": request})
#     #     return Response(status=status.HTTP_200_OK, data=serializer.data)


# class UserMeView(GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     # def get_queryset(self, *args, **kwargs):
#     #     id = self.request.user.id
#     #     # return User.objects.get(id=self.request.user.id)
#     #     return self.queryset.filter(id=id)

#     def get(self, request, *args, **kwargs):
#         user = User.objects.get(id=request.user.id)
#         serializer = UserSerializer(user)
#         return Response(data=serializer.data)


# class AuthViewSet(GenericViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     token_generator = default_token_generator

#     def get_serializer_class(self):
#         if self.action == "forgot_password":
#             return ForgotPasswordSerializer
#         if self.action == "verify_reset_email":
#             return VerifyResetEmailSerializer
#         if self.action == "reset_password":
#             return ResetPasswordSerializer
#         return super().get_serializer_class()

#     @extend_schema(responses={200: ReturnSecretSerializer})
#     @action(
#         ["post"],
#         detail=False,
#         url_path="forgot-password",
#         permission_classes=[AllowAny],
#     )
#     def forgot_password(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.get_user()
#         ######
#         secret = pyotp.random_base32()
#         data = {"secret": secret}
#         # secret_serializer = ReturnSecretSerializer(data)

#         if user:
#             # remove next two lines in prod 👇
#             otp = generate_otp(secret)
#             data.update({"otp": otp})
#             return Response(data=data, status=status.HTTP_200_OK)
#             # send_password_reset(user, secret)
#             # return Response(secret_serializer.data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_404_NOT_FOUND, data="User Not Found")
#         # return Response(data=secret_serializer.data, status=status.HTTP_200_OK)

#     @extend_schema(responses={200: ReturnUidAndTokenSerializer})
#     @action(
#         ["post"],
#         detail=False,
#         url_path="verify_reset_email",
#         permission_classes=[AllowAny],
#     )
#     def verify_reset_email(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.get_user()
#         uid = encode_uid(user.pk)
#         token = default_token_generator.make_token(user)
#         to_serialize = {"uid": uid, "token": token}
#         response_serializer = ReturnUidAndTokenSerializer(to_serialize)
#         return Response(response_serializer.data, status=status.HTTP_200_OK)

#     @extend_schema(responses={200: None})
#     @action(
#         ["post"],
#         detail=False,
#         url_path="reset_password",
#         permission_classes=[AllowAny],
#     )
#     def reset_password(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         serializer.user.set_password(serializer.data["new_password"])
#         if hasattr(serializer.user, "last_login"):
#             serializer.user.last_login = now()
#         serializer.user.save()

#         if djoser_settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
#             context = {"user": serializer.user}
#             to = [get_user_email(serializer.user)]
#             djoser_settings.EMAIL.password_changed_confirmation(
#                 self.request, context
#             ).send(to)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class UtilityAccountView(GenericAPIView):
#     # queryset = UtilityAccountProfile.objects.all()
#     serializer_class = CreateUtilityAccountSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user.id
#         if self.request.method == "POST":
#             return UtilityAccountProfile.objects.none()
#         elif self.request.method == "GET":
#             # return UtilityAccountProfile.objects.all()

#             # TODO: Revisit for when we add co-owners
#             return UtilityAccountProfile.objects.filter(event__organizer=user)

#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return CreateUtilityAccountSerializer
#         elif self.request.method == "GET":
#             return UtilityAccountProfileSerializer
#         elif self.request.method == "PUT":
#             return UtilityAccountProfileUpdateSerializer

#     def get_object(self, pk):
#         try:
#             return UtilityAccountProfile.objects.get(pk=pk)
#         except UtilityAccountProfile.DoesNotExist:
#             raise Http404("User does not exist")

#     @extend_schema(
#         summary="create_utility_account",
#         responses={
#             200: OpenApiResponse(
#                 response=CreateUtilityAccountResponseSerializer,
#             ),
#         },
#     )
#     def post(self, request, *args, **kwargs):
#         serializer_class = self.get_serializer_class()
#         serializer = serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         event = Event.objects.get(id=serializer.data.get("event"))
#         if event.organizer.id == self.request.user.id:
#             related_utility_accounts_number = event.utility_account.count()
#             username = f"u{int(related_utility_accounts_number)+1}.{event.short_alias}"
#             email = username + "@eventz.app"
#             new_user = UserObj.objects.create(
#                 name=username,
#                 email=email,
#                 account_type=UserObj.AccountType.UTILITY_ACCOUNT.value,
#             )
#             password = get_random_string(9)
#             new_user.set_password(password)
#             new_user.save()

#             UtilityAccountProfile.objects.create(user=new_user, event=event)

#             data = {"username": email, "password": password}

#             return Response(data=data, status=status.HTTP_201_CREATED)
#         else:
#             data = {"detail": "You are not permitted to perform this action"}
#             return Response(data=data, status=status.HTTP_403_FORBIDDEN)

#     @extend_schema(
#         summary="get_utility_accounts",
#         responses={
#             200: OpenApiResponse(
#                 response=UtilityAccountProfileSerializer(many=True),
#             ),
#             # 200: UtilityAccountProfileSerializer(many=True)
#         },
#         parameters=[
#             OpenApiParameter(name="event_id", description="Event Id", type=str),
#         ],
#     )
#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         event_id = request.query_params.get("event_id")
#         # TODO: Put checks to ensure only owner has access to view
#         if event_id:
#             queryset = queryset.filter(event=event_id)

#         serializer_class = self.get_serializer_class()
#         serializer = serializer_class(queryset, many=True)
#         return Response(data=serializer.data)


# # github example: 455391023+Godfo-james@users.noreply.github.com
# # example: amazon.xyz@my.user.name-my.alias.provider.com
# # -------------

# # username.eventalias@eventz.app

# # event = event.objects.get(id=id)
# # alias = event.alias

# # -------------


# class UpdateUtilityAccountView(GenericAPIView):
#     queryset = UtilityAccountProfile.objects.all()
#     serializer_class = UtilityAccountProfileUpdateSerializer
#     permission_classes = [IsAuthenticated]

#     # def get_queryset(self):
#     #     if self.request.method == "PUT":
#     #         id = self.kwargs.get("id")
#     #         return UtilityAccountProfile.objects.filter(id=id)

#     # def get_object(self, id):
#     #     try:
#     #         return UtilityAccountProfile.objects.get(id=id)
#     #     except UtilityAccountProfile.DoesNotExist:
#     #         raise Http404("User does not exist")

#     @extend_schema(
#         summary="update_utility_account",
#         responses={
#             200: OpenApiResponse(
#                 response=UtilityAccountProfileUpdateSerializer,
#             ),
#         },
#     )
#     def patch(self, request, id):
#         try:
#             instance = UtilityAccountProfile.objects.get(id=id)
#         except UtilityAccountProfile.DoesNotExist:
#             data = {"datail": "User Not Found"}
#             return Response(data=data, status=status.HTTP_404_NOT_FOUND)

#         # instance = self.get_object(id)

#         # if self.request.user.id:
#         if instance.event.organizer.id == self.request.user.id:

#             serializer = UtilityAccountProfileUpdateSerializer(
#                 instance, data=request.data, partial=True
#             )
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             data = {"detail": "User updated successfully"}
#             return Response(status=status.HTTP_200_OK, data=data)
#         else:
#             data = {"datail": "You are not permitted to perform this action"}
#             return Response(data=data, status=status.HTTP_403_FORBIDDEN)
