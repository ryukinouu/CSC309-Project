from ..models import (
    MyUser,
    PetSeeker,
    PetShelter,
)
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    BooleanField,
    ImageField,
    EmailField,
)
from rest_framework.exceptions import ValidationError as restValidationError
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError as djangoValidationError

# Create Shelter and Seeker user
class UserCreateSerializer(ModelSerializer):
    password1 = CharField(max_length=128, write_only=True)
    password2 = CharField(max_length=128, write_only=True)

    # field to determine the type of user
    become_shelter = BooleanField(required=True, write_only=True)

    class Meta:
        model = MyUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
            "become_shelter",
        ]

    def create(self, validated_data):
        
        # Helpers that raise the error messages all at once
        valid = True
        errors = {}
        
        email = validated_data.get("email")
        password1 = validated_data.pop("password1", "")
        password2 = validated_data.pop("password2", "")
        become_shelter = validated_data.pop("become_shelter", "")
        if MyUser.objects.filter(email=email).exists():
            valid = False
            errors["email"] = "User with this email already exists."
        # check password
        if password1 and password2 and password1 != password2:
            valid = False
            errors["password2"] = "password mismatch"
            
        if not valid:
            raise restValidationError(errors)
            
        # check user type
        if become_shelter:
            user = PetShelter.objects.create(**validated_data)
            user.is_shelter = True
            user.shelter_name = validated_data.get("username")
        else:
            user = PetSeeker.objects.create(**validated_data)
            user.is_seeker = True
        # user.email = email
        user.set_password(password1)
        user.save()
        return user


# Update basic info for both Shelter and Seeker user
class SeekerUpdateSerializer(ModelSerializer):
    old_password = CharField(style={"input_type": "password"}, required=False)
    new_password = CharField(style={"input_type": "password"}, required=False)
    username = CharField(required=False)
    email = EmailField(required=False)
    first_name = CharField(required=False, max_length=100)
    last_name = CharField(required=False, max_length=100)

    class Meta:
        model = MyUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "address",
            "city",
            "province",
            "postal_code",
            "user_avatar",
            "receive_communications",
            "receive_news",
            "old_password",
            "new_password",
        ]

    def update(self, instance, validated_data):
        old_password = validated_data.pop("old_password", None)
        new_password = validated_data.pop("new_password", None)

        # Helpers that raise the error messages all at once
        valid = True
        errors = {}

        # Check if email exists
        if "email" in validated_data:
            email = validated_data["email"]
            if MyUser.objects.filter(email=email) and email != instance.email:
                errors["email"] = "This email already exists."
                valid = False
            else:
                validate_email(email)

        # Check if username exists
        if "username" in validated_data:
            username = validated_data["username"]
            if (
                MyUser.objects.filter(username=username)
                and username != instance.username
            ):
                errors["username"] = "This username already exists."
                valid = False

        # Check if phone_number is valid
        if "phone_number" in validated_data:
            phone_number = validated_data["phone_number"]
            phone_regex = RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
            )
            try:
                phone_regex(phone_number)
            except djangoValidationError:
                errors["phone_number"] = "Phone number must be entered in the format:"\
                + "'+999999999'. Up to 15 digits allowed."
                valid = False
        
        # Check if old password is correct
        if old_password and new_password:
            if instance.check_password(old_password):
                instance.set_password(new_password)
                instance.save()
            else:
                errors["password"] = "Old password is incorrect."
                valid = False
        
        if not valid:
            raise restValidationError(errors)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ShelterUpdateSerializer(SeekerUpdateSerializer):
    shelter_name = CharField(required=False)
    shelter_avatar = ImageField(required=False)
    mission_statement = CharField(required=False)

    class Meta:
        model = MyUser
        fields = SeekerUpdateSerializer.Meta.fields + [
            "shelter_name",
            "shelter_avatar",
            "mission_statement",
        ]
        
    def update(self, instance, validated_data):
        if "shelter_name" in validated_data:
            shelter_name = validated_data["shelter_name"]
            if (
                PetShelter.objects.filter(shelter_name=shelter_name) and shelter_name != instance.shelter_name
            ):
                raise restValidationError({"shelter_name": "This shelter name already exists."})
            else:
                setattr(instance, "shelter_name", validated_data["shelter_name"])
        if "shelter_avatar" in validated_data:
            setattr(instance, "shelter_avatar", validated_data["shelter_avatar"])
        if "mission_statement" in validated_data:
            setattr(instance, "mission_statement", validated_data["mission_statement"])
        instance.save()
        # update Shelter
        return super().update(instance, validated_data)


# Get profile of a shelter
class ShelterProfileSerializer(ModelSerializer):
    class Meta:
        model = PetShelter
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "address",
            "city",
            "province",
            "postal_code",
            "user_avatar",
            "shelter_name",
            "shelter_avatar",
            "mission_statement",
        ]

class ShelterListSerializer(ModelSerializer):
    class Meta:
        model = PetShelter
        fields = [
            "id",
            "shelter_name",
            "username",
            "city",
            "province",
            "postal_code",
            "phone_number",
            "email",
        ]

# Get profile of a seeker from a shelter's perspective
class SeekerProfileSerializer(ModelSerializer):
    class Meta:
        model = PetSeeker
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "address",
            "city",
            "province",
            "postal_code",
            "user_avatar",
        ]


# Delete user
class UserDeleteSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"


class SeekerDeleteSerializer(UserDeleteSerializer):
    class Meta:
        model = PetSeeker
        fields = "__all__"


class ShelterDeleteSerializer(UserDeleteSerializer):
    class Meta:
        model = PetShelter
        fields = "__all__"
