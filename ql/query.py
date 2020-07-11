import graphene
from graphene.types.generic import GenericScalar
from django.apps import apps
from django.conf import settings
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from server.models import User
from .types import UserType


dict_querys = {}
server_models = apps.get_app_config('server').get_models()

for model in server_models:
    name = model.__name__

    if not name in settings.QL_EXCLUDE_AUTO_QUERYS:
        name = name.lower()

        model_type = model.get_type()

        single_resolver = model.get_single_resolver()
        multi_resolver = model.get_multi_resolver()

        dict_querys.update(
            {
                name: graphene.Field(model_type, pk=graphene.Int()),
                name + '_list': DjangoFilterConnectionField(
                    model_type,
                    orderBy=graphene.List(graphene.String),
                    filters=GenericScalar(),
                    exclude=GenericScalar(),
                    ),
                'resolve_' + name: single_resolver,
                'resolve_' + name + "_list": multi_resolver
            }
        )


@login_required
def resolve_User(self, info, **kwargs):
    pk = kwargs.get("pk")
    if pk is not None:
        return User.objects.get(pk=pk)
    return None

dict_querys.update(
    {
        "User": graphene.Field(UserType, pk=graphene.Int()),
        "resolve_User": resolve_User
    }
)


auto_query = type("auto_query", (graphene.ObjectType,), dict_querys)
