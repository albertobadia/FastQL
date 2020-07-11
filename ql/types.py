import graphene
from graphene_django.types import DjangoObjectType
from server import models


class UserType(DjangoObjectType):
    """Type for quering User"""
    pk = graphene.Int()

    class Meta:
        """Meta options"""

        model = models.User
        exclude_fields = ["password"]
        interfaces = (graphene.relay.Node,)
