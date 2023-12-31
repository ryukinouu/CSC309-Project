from django.shortcuts import render
from ..models import (
    PetSeeker,
    PetShelter,
    MyUser,
)
from ..serializers import (
    UserCreateSerializer,
    # UserLogInSerializer,
    SeekerUpdateSerializer,
    ShelterUpdateSerializer,
    ShelterProfileSerializer,
    ShelterListSerializer,
    SeekerProfileSerializer,
    SeekerDeleteSerializer,
    ShelterDeleteSerializer,
)
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    ListAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from applications.models import Application
from rest_framework.pagination import PageNumberPagination
from django.http import Http404

# Create your views here.
# Create Shelter and Seeker user
class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        return super().perform_create(serializer)


# Update Shelter and Seeker user
class UserUpdateView(UpdateAPIView):
    serializer_class = SeekerUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_shelter:
            return ShelterUpdateSerializer
        elif self.request.user.is_seeker:
            return SeekerUpdateSerializer

    def get_object(self):
        # Check token validity
        user = get_object_or_404(MyUser, username=self.request.user.username)

        if user.username != self.kwargs["username"]:
            raise PermissionDenied()
        if user.is_shelter:
            return get_object_or_404(
                PetShelter, username=self.kwargs["username"]
            )
        elif user.is_seeker:
            return get_object_or_404(
                PetSeeker, username=self.kwargs["username"]
            )


# Retrieve Shelter
class ShelterRetrieveView(RetrieveAPIView):
    serializer_class = ShelterProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Check token validity
        _ = get_object_or_404(MyUser, username=self.request.user.username)

        return get_object_or_404(PetShelter, username=self.kwargs["username"])


# Retrieve Seeker (need to check if the seeker has an active application)
class SeekerRetrieveView(RetrieveAPIView):
    serializer_class = SeekerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Check token validity
        user = get_object_or_404(MyUser, username=self.request.user.username)

        if user.is_shelter:
            seeker = get_object_or_404(
                PetSeeker, username=self.kwargs["username"]
            )
            if Application.objects.filter(
                status="pending",
                shelter=self.request.user,
                applicant=seeker,
            ).exists():
                return seeker
            else:
                raise Http404()
        elif user.username != self.kwargs["username"]:
            raise PermissionDenied()
        else:
            return get_object_or_404(
                PetSeeker, username=self.kwargs["username"]
            )


class ShelterListView(ListAPIView):
    serializer_class = ShelterListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return PetShelter.objects.all()


class UserDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_shelter:
            return ShelterDeleteSerializer
        elif self.request.user.is_seeker:
            return SeekerDeleteSerializer

    def get_object(self):
        # Check token validity
        user = get_object_or_404(MyUser, username=self.request.user.username)

        if user.username != self.kwargs["username"]:
            raise PermissionDenied()
        if user.is_shelter:
            return get_object_or_404(
                PetShelter, username=self.kwargs["username"]
            )
        elif user.is_seeker:
            return get_object_or_404(
                PetSeeker, username=self.kwargs["username"]
            )
