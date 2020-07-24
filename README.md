# FastQL
### GraphQL API automatically generated from Django models

Contains a BaseModel class to parse auto build types, querys, and mutations, your model must be based on that.

There are two models example: Book, and Author.

- Authentication: Graphql-JWT ( https://django-graphql-jwt.domake.io/en/latest/ )
- Mutations and Querys: graphene-django-extras ( https://github.com/eamigo86/graphene-django-extras )
- Queryng optimization with: graphene-django-optimizer ( https://github.com/tfoxy/graphene-django-optimizer )

You can parse arguments directly to queryset:

  - filters: {name__icontains: "Richard"}
  - orderBy: ["-name"]
  - exclude: {last_name__icontains: "Harris"}
  
  ( Related objects based too )
  
  - filters: {author__name__icontains: "Jerry"}
  - exclude: {author__last_name__icontains: "Lewis"}

  You must consider that Graphene overwirte fields like "last_name" to "lastName" in querys, this arguments are for the queryset itself, so you can use the original field name for filters, exclude and orderBy arguments.
