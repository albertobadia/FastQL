import graphene
import graphql_jwt
from graphene_django_extras.mutation import DjangoSerializerMutation
from django.apps import apps
from django.conf import settings
from server import models
from .query import auto_query


server_models = apps.get_app_config('server').get_models()
dict_mutations = {}

for model in server_models:
    name = model.__name__

    if not name in settings.QL_EXCLUDE_AUTO_MUTATIONS:

        model_mutation = model.get_mutation()

        mutation = type(
            name + "mutation", (model_mutation,),
            {"Meta": {"serializer_class": model.get_serializer()}}
        )


        dict_mutations.update(
            {
                "create_" + name: mutation.CreateField(),
                "update_" + name: mutation.UpdateField(),
                "delete_" + name: mutation.DeleteField()
            }
        )

dict_mutations.update(
    {
        "token_auth": graphql_jwt.ObtainJSONWebToken.Field(),
        "verify_token": graphql_jwt.Verify.Field(),
        "refresh_token": graphql_jwt.Refresh.Field(),
    }
)

auto_mutation = type("auto_mutations", (graphene.ObjectType,), dict_mutations)

schema = graphene.Schema(mutation=auto_mutation, query=auto_query)
