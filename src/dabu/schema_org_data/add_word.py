"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-23 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

from .add_properties_to_object import add_properties_to_object
from .get_graph_item import get_graph_item


def create_context_schema(word):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16
    """
    context = dict()
    context["required"] = [word]
    context["properties"] = {word: {"type": "string",
                                    "enum": ["https://schema.org/" + word]}}
    return context


def add_word(schemaorg_data, word):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-23

    This function generates a json schema from https://schema.org , which
    desribes the given word.

    :param schemaorg_data: json-ld data from https://schema.org as returned
                           from :func:`get_schema_org_data`.
    :param word: word, which are a Schema.org Type (Schema.org vocabulary)

    :return: return a list of:

             * missing words
             * json schema describing a json-ld for the given word
    """
    # pylint: disable=too-many-branches
    missing_words = []
    schema = dict()
    data = get_graph_item(schemaorg_data, word)
    if data is None:
        return [], None
    if ("@type" in data) and (data["@type"] == "rdfs:Class"):
        # found json object description
        schema["definitions"] = dict()
        schema["definitions"][word] = dict()
        schema["definitions"][word]["type"] = "object"
        if "rdfs:comment" in data:
            schema["definitions"][word]["description"] = data["rdfs:comment"]
        # schema["definitions"][word]["required"] = ["@context"]
        schema["definitions"][word]["required"] = []
        schema["definitions"][word]["properties"] = dict()
        properties = schema["definitions"][word]["properties"]
        # properties["@context"] = create_context_schema(word)
        if "rdfs:subClassOf" in data:
            sub_class_of = []
            if isinstance(data["rdfs:subClassOf"], dict):
                if data["rdfs:subClassOf"]["@id"].startswith('schema:'):
                    sub_class_of.append(data["rdfs:subClassOf"]["@id"])
            elif isinstance(data["rdfs:subClassOf"], list):
                for sco in data["rdfs:subClassOf"]:
                    if sco["@id"].startswith('schema:'):
                        sub_class_of.append(sco["@id"])
            else:
                raise NotImplementedError(
                    'data type of "rdfs:subClassOf" not handled')
            if bool(sub_class_of):  # len(sub_class_of) > 0
                schema["definitions"][word]["allOf"] = list()
                schema["definitions"][word]["allOf"].append(properties)
                properties = schema["definitions"][word]["allOf"][0]
                for sco in sub_class_of:
                    new_word = sco.split('schema:')[1]
                    schema["definitions"][word]["allOf"].append(
                        {"$ref": "#/definitions/" + new_word})
                    missing_words.append(new_word)
                del schema["definitions"][word]["properties"]
        # add other properties to: properties
        add_properties_to_object(
            schemaorg_data, word, properties, missing_words)
        # items with: "schema:domainIncludes": {"@id": "schema:Person"}
        # example: "@id": "schema:additionalName",
        schema["required"] = ["@context"]
        schema["properties"] = dict()
        schema["properties"]["@context"] = create_context_schema(word)
        if not bool(schema["definitions"][word]["required"]):  # len(..) == 0
            del schema["definitions"][word]["required"]
    return missing_words, schema
