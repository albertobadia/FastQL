from django.db import models
import graphene
from django_currentuser.db.models import CurrentUserField
from rest_framework.serializers import ModelSerializer
from graphene_django_extras.mutation import DjangoSerializerMutation
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
import graphene_django_optimizer as gql_optimizer


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
            @login_required
            def update(cls, root, info, **kwargs):
                return super(Mutation, cls).update(root, info, **kwargs)

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
                "interfaces": (graphene.relay.Node,)
            }
        }
        )

        return model_type
    
    @classmethod
    def get_single_resolver(cls):

        @login_required
        def single_resolver(self, info, **kwargs):
            pk = kwargs.get("pk")
            if pk is not None:
                return cls.objects.get(pk=pk)
            return None
        
        return single_resolver

    @classmethod
    def get_multi_resolver(cls):

        @login_required
        def multi_resolver(self, info, **kwargs):
            querySet = cls.objects.all()

            orderBy = kwargs.get("orderBy")
            if orderBy is not None:
                querySet = querySet.order_by(*orderBy)
            
            filters = kwargs.get("filters")
            if filters is not None:
                querySet = querySet.filter(**filters)

            return gql_optimizer.query(querySet, info)

        return multi_resolver
