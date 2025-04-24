from rest_framework import serializers
from blog.models import Post, Catgory
from accounts.models import Profile

# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class CatgorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catgory
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    # content = serializers.CharField(read_only=True)

    # use category name intend primary key
    # catgory = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Catgory.objects.all()
    # )
    # catgory=CatgorySerializer()
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_urls = serializers.URLField(
        source="get_absolute_api_url", read_only=True
    )
    absolute_urls = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # read_only_fields = ['content']
        read_only_fields = ["author"]
        fields = [
            "id",
            "author",
            "title",
            "content",
            "status",
            "image",
            "catgory",
            "snippet",
            "created_date",
            "updated_date",
            "published_date",
            "author",
            "relative_urls",
            "absolute_urls",
        ]

    def get_absolute_urls(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        # rep['state']='list'
        # this if condition check is list or single item
        # if request.parser_context.get('kwargs').get('pk'):
        #     rep['state']='single'
        if (
            request
            and request.parser_context
            and request.parser_context.get("kwargs", {}).get("pk")
        ):
            rep.pop("relative_urls", None)
            rep.pop("absolute_urls", None)
            rep.pop("snippet", None)
        else:
            rep.pop("created_date", None)
            rep.pop("updated_date", None)
            rep.pop("published_date", None)
            rep.pop("content", None)
        rep["catgory"] = (
            CatgorySerializer(instance.catgory).data
            if instance.catgory
            else None
        )
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
