from rest_framework import serializers
from general.models import Comment, Post, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )

    def create(self, validated_data):
        user = User.objects.create(
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", )


class NestedPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "body",
            "created_at",
        )


class UserRetrieveSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()
    friend_count = serializers.SerializerMethodField()
    posts = NestedPostListSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "is_friend",
            "friend_count",
            "posts",
        )

    def get_friend_count(self, obj) -> int:
        return obj.friends.count()

    def get_is_friend(self, obj) -> bool:
        return obj in self.context["request"].user.friends.all()


class UserListSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "is_friend")

    def get_is_friend(self, obj) -> bool:
        current_user = self.context["request"].user
        return current_user in obj.friends.all()
    

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class PostListSerializer(serializers.ModelSerializer):
    author = UserShortSerializer()
    body = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "body",
            "created_at",
        )
    
    def get_body(self, obj) -> str:
        if len(obj.body) > 128:
            return obj.body[:125] + "..."
        return obj.body
    

class PostRetrieveSerializer(serializers.ModelSerializer):
    author = UserShortSerializer()
    my_reaction = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "body",
            "my_reaction",
            "created_at",
        )

    def get_my_reaction(self, obj) -> str:
        reaction = self.context["request"].user.reactions.filter(post=obj).last()
        return reaction.value if reaction else ""
    

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "body",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    def get_fields(self):
        fields = super().get_fields()
        if self.context["request"].method == "GET":
            fields["author"] = UserShortSerializer(read_only=True)
        return fields
    
    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "post",
            "body",
            "created_at",
        )
