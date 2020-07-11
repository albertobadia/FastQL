# FastQL
### GraphQL API automatically generated from Django models
### ( README under construction )

Contains a BaseModel class to parse auto build types, querys, and mutations.

You can parse arguments directly to queryset:

  - filters: {name__icontains: "Richard"}
  - orderBy: ["-name"]
  - exclude: {last_name__icontains: "Harris"}

  You must consider that Graphene overwirte fields like "first_name" to "firstName", this arguments are for the model itself, so you can use the original field name.
