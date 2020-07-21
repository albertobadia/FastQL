import graphene
import graphene_django_optimizer as gql_optimizer
from django.db import models
from django_currentuser.db.models import CurrentUserField
from rest_framework.serializers import ModelSerializer
from graphene_django_extras.mutation import DjangoSerializerMutation
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType


def get_id(kwargs):
    """Search id key in kwargs and returns value"""
    for i in kwargs:
        try:
            return kwargs[i]["id"]
        except KeyError:
            return get_id(kwargs[i])


class BaseModel(models.Model):
    """Act as base class for models, include some extra fields and methods"""

    user = CurrentUserField(
        related_name="%(class)s_entrys",
        help_text='The user that last created / modified the instance'
    )

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on wich the object was created.'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on wich the object was last modified.'
    )

    class Meta:
        """Meta options"""

        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']

    # Login require configs
    _query_login_required = True
    _create_login_required = True
    _update_login_required = True
    _delete_login_required = True

    @classmethod
    def get_config(cls):
        """Returns a dict wich store some configs for cls access"""
        return {
            "query_login_required": cls._query_login_required,
            "create_login_required": cls._create_login_required,
            "update_login_required": cls._update_login_required,
            "delete_login_required": cls._delete_login_required,
        }

    @classmethod
    def user_create_test(cls, user, instance):
        """By default test if user is the owner"""

        return cls.objects.get(pk=instance).user == user

    @classmethod
    def user_update_test(cls, user, instance):
        """By default test if user is the owner"""

        return cls.objects.get(pk=instance).user == user

    @classmethod
    def user_delete_test(cls, user, instance):
        """By default test if user is the owner"""

        return cls.objects.get(pk=instance).user == user

    @classmethod
    def get_serializer(cls):
        """Return a basic ModelSerializer ready for normal use cases"""

        class Serializer (ModelSerializer):
            """Auto build serializer from model reference"""

            class Meta:
                """Meta options"""

                model = cls
                fields = '__all__'

        return Serializer

    @classmethod
    def get_mutation(cls):
        """Return a basic DjangoSerializerMutation ready for normal use cases"""

        class Mutation(DjangoSerializerMutation):
            """Generic mutation"""

            class Meta:
                """Meta options"""

                description = cls.__name__ + " generic mutation"
                serializer_class = cls.get_serializer()

            @classmethod
            @login_required
            def create(cls, root, info, **kwargs):
                return super(Mutation, cls).create(root, info, **kwargs)

            @classmethod
            def update(cls, root, info, **kwargs):
                user = info.context.user
                instance = get_id(kwargs)

                if not cls._meta.model._update_login_required:
                    return super(Mutation, cls).update(root, info, **kwargs)

                elif not user.is_anonymous:
                    if cls._meta.model.user_update_test(user, instance):
                        return super(Mutation, cls).update(root, info, **kwargs)

                raise Exception("Instance operation not permited")

            @classmethod
            @login_required
            def delete(cls, root, info, **kwargs):
                return super(Mutation, cls).delete(root, info, **kwargs)

        return Mutation

    @classmethod
    def get_type(cls):
        """Return a basic DjangoObjectType ready for normal use cases"""

        model_type = type(cls.__name__, (DjangoObjectType,),
            {
                "pk": graphene.Int(),
                "Meta": {
                    "model": cls,
                    "fields": "__all__",
                    "filter_fields": {"user": ["exact"]},
                    "interfaces": (graphene.relay.Node,),
                },
            }
        )

        return model_type

    @classmethod
    def get_single_resolver(cls):
        """Returns a function that acts as a single resolver"""

        def single_resolver(self, info, **kwargs):
            pk = kwargs.get("pk")
            config = cls.get_config()

            if pk is not None:
                if not config.get("query_login_required") or info.context.user.is_authenticated:
                    return cls.objects.get(pk=pk)

                raise Exception("User not logged in")

            return None

        return single_resolver

    @classmethod
    def get_multi_resolver(cls):
        """Returns a function that acts as a multi resolver"""

        def multi_resolver(self, info, **kwargs):
            config = cls.get_config()
            exclude = kwargs.get("exclude")
            filters = kwargs.get("filters")
            orderBy = kwargs.get("orderBy")

            if not config.get("query_login_required") or info.context.user.is_authenticated:
                qs = cls.objects.all()

                if exclude:
                    qs = qs.exclude(**exclude)
                if filters:
                    qs = qs.filter(**filters)
                if orderBy:
                    qs = qs.order_by(*orderBy)

                return gql_optimizer.query(qs, info)

            raise Exception("User not logged in")

        return multi_resolver
