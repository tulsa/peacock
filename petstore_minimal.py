import peacock
from peacock import *


def minimal_peacock():
    ''' Return a minimal working swagger file object (peacock) '''
    info = peacock.Info(title="",version="")
    return peacock.Swagger(info=info,
                           paths=peacock.Paths())

print minimal_peacock()
exit()

desc = "A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification"

info = Info(
    {
    "version": "1.0.0",
    "title": "Swagger Petstore",
    "description": desc,
    "termsOfService": "http://swagger.io/terms/",
    "contact" : Contact(name="Swagger API Team"),
    "license" : License(name="MIT")
    }
)

schema = Schema(type_="array",
                items=Item(ref_="#/definitions/Pet"))

res = Response(description="A list of pets.",
               schema=schema)

desc = "Returns all pets from the system that the user has access to"
get_pet = Operation(responses=Responses({"200":res}),
                    produces=["application/json"],
                    description=desc)

P = Paths({"/pets":Path(get=get_pet)})

pet = Schema(type_="object",required=["id","name"],
             properties=Properties(
                 id=Property(type="integer",format="int64"),
                 name=Property(type="string"),
                 tag=Property(type="string"),
             ))
defs = Definitions(Pet=pet)

args = {
    "consumes":["application/json"],
    "produces":["application/json"],
    "basePath":"/api",
    "schemes":["http"],
    "host":"petstore.swagger.io",
}

S = Swagger(args, info=info,paths=P,definitions=defs)
print S

if __name__ == "__main__":
    import json

    S1 = json.loads(S.json())
    with open("examples/petstore_minimal.json") as FIN:
        S2 = json.load(FIN)
    
    from deepdiff import DeepDiff
    from pprint import pprint
    diff = DeepDiff(S2,S1)

    if len(diff)>0:
        raise SyntaxError("petstore_minimal.json doesn't match!")
    else:
        print "Passes!"

