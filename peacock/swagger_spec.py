# -*- coding: utf-8 -*-

from atom import atom, simple_atom
from traits.api import Int, Str, Float, List, Enum
from traits.api import Bool, Any, Dict, Either, This
from traits.api import Instance

# Use the default of None for all basic types
Str  = Str(None)
Bool = Bool(None)
Int  = Int(None)
Float= Float(None)

# Monkey-patch instance to create a default type
#def Instance(trait_type,*args,**kwargs):
#    return traits.api.Instance(trait_type,args=args,kwargs=kwargs)

class License(atom):
    name = Str
    url  = Str
    _required = ["name"]

class Contact(atom):
    name  = Str
    url   = Str
    email = Str

class Info(atom):
    title   = Str
    version = Str
    description    = Str
    termsOfService = Str
    license = Instance(License,())
    contact = Instance(Contact,())
    _required = ["title", "version"]

class XMLObject(atom):
    name = Str
    namespace = Str
    prefix = Str
    attribute = Bool
    wrapped   = Bool

class ExternalDocs(atom):
    description = Str
    url = Str
    _required = ["url"]

class Tag(atom):
    name = Str
    description = Str
    externalDocs = Instance(ExternalDocs)
    _required = ["name"]

class Scopes(simple_atom):
    data = Dict(Str, Str)

class SecurityRequirement(simple_atom):
    data = Dict(Str, List(Str))

class SecurityScheme(atom):
    type_ = Enum([None,"basic", "apiKey","oauth2"])
    description = Str
    name = Str
    in_  = Enum([None,"query","header"])
    flow = Enum([None, "implicit", "password", "application", "accessCode"])
    authorizationUrl = Str
    tokenUrl = Str
    scopes = Instance(Scopes)

    _required = ["type_",]
    _conditional_required = {
        ("type_",("apiKey",)):["name","in_"],
        ("type_",("oauth2",)):["flow","authorizationUrl","tokenUrl","scopes"],
    }
    _name_mappings = {"in_":"in", "type_":"type"}
        
class SecurityDefinitions(simple_atom):
    data = Dict(Str, SecurityScheme)
        
class Item(atom):
    ref_    = Str
    type_   = Enum([None,"string","number","integer","boolean","array","file"])
    format  = Str
    allowEmptyValue = Bool
    default = Str
    maximum = Float
    exclusiveMaximum = Bool
    minimum = Float
    exclusiveMinimum = Float
    maxLength = Int
    minLength = Int
    pattern = Str
    maxItems = Int
    minItems = Int
    uniqueItems = Bool
    enum = List(Str)
    multipleOf = Float

    #_required = ["type_"]
    
    _conditional_required = {
        ("type_",("array",)):["items"],
    }
    _name_mappings = {"type_":"type",
                      "ref_":"$ref"}

    items = Instance(This)
    
#Item.add_class_trait('items', Instance(Item))

class Reference(atom):
    ref_ = Str
    _name_mappings = {"ref_":"$ref"}
    _required = ["ref_"]


class Property(Item):
    pass

class Properties(simple_atom):
    data = Dict(Str, Property)
    
class Schema(atom):
    ref_ = Instance(Reference)
    title = Str
    description = Str
    required = List(Str)
    type_ = Str

    properties = Instance(Properties)
    #allOf = ???
    #additionalProperties = ???
    #maxProperties = Str
    #minProperties = Str
    items = Instance(Item)

    # Further schema documentation
    discriminator = Str
    readOnly = Bool
    xml = Instance(XMLObject)
    externalDocs = Instance(ExternalDocs)
    example = Any
    
    _name_mappings = {"ref_":"$ref"}
    _name_mappings.update(Item._name_mappings)


class Definitions(simple_atom):
    data = Dict(Str, Instance(Schema))

###############################################################################

class Parameter(Item):
    name = Str
    description = Str
    required = Bool
    collectionFormat = Enum([None,"csv","ssb","tsv","pipes","multi"])

    in_   = Enum(["query", "header", "path", "formData", "body"])
    schema = Instance(Schema)
        
    _required = ["name","in_"]
    
    _conditional_required = {
        ("in_",("body",)):["schema"],
        ("in_",("query", "header", "path", "formData",)):["type_"],
    }
    _conditional_required.update(Item._conditional_required)
    
    _name_mappings = {"in_":"in"}
    _name_mappings.update(Item._name_mappings)

class Parameters(simple_atom):
    data = Dict(Str, Parameter)

###############################################################################

class Header(Item):
    pass

class Headers(simple_atom):
    data = Dict(Str, Header)

class Example(simple_atom):
    data = Dict(Str,Dict(Str,Str))

class Response(atom):
    description = Str
    schema = Instance(Schema)
    headers = Instance(Headers)
    examples = Instance(Example)
    _required = ["description"]

class Responses(simple_atom):
    data = Dict(Str, Response)

###############################################################################

class Operation(atom):
    tags = List(Str)
    summary = Str
    description = Str
    externalDocs = Instance(ExternalDocs)
    operationId = Str
    consumes = List(Str)
    produces = List(Str)
    parameters = List(Either(Parameters,Reference))
    responses = Instance(Responses)
    schemes   = List(Enum([None,"http", "https", "ws", "wss"]))
    deprecated = Bool
    security = Instance(SecurityRequirement)
    _required = ["responses"]

class Path(atom):
    ref_ = Instance(Reference)
    get  = Instance(Operation)
    put  = Instance(Operation)
    post = Instance(Operation)
    delete  = Instance(Operation)
    options = Instance(Operation)
    head = Instance(Operation)
    patch = Instance(Operation)
    parameters = List(Either(Parameters,Reference))
    _name_mappings = {"ref_":"$ref"}

class Paths(simple_atom):
    data = Dict(Str, Path)

###############################################################################

class Swagger(atom):
    swagger = Enum(["2.0"])
    info = Instance(Info)
    host = Str
    basePath = Str
    schemes = List(Enum([None,"http", "https", "ws", "wss"]))
    consumes = List(Str)
    produces = List(Str)
    paths = Instance(Paths)
    definitions = Instance(Definitions)
    parameters = Instance(Parameters)
    responses = Instance(Responses)
    securityDefinitions = Instance(SecurityDefinitions)
    security = List(Instance(SecurityRequirement))
    tags = Instance(Tag)
    externalDocs = Instance(ExternalDocs)
    _required=["paths","info"]

###############################################################################
