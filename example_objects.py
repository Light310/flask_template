"""
This is the example_objects module and supports all the REST actions for the
example_objects data
"""

from flask import make_response, abort
from config import db
from models import ExampleObject, ExampleObjectSchema


def read_all():
    """
    This function responds to a request for /api/example_objects
    with the complete lists of example_objects
    :return:        json string of list of example_objects
    """
    # Create the list of example_objects from our data
    example_objects = ExampleObject.query.order_by(ExampleObject.field2).all()

    # Serialize the data for the response
    example_object_schema = ExampleObjectSchema(many=True)
    data = example_object_schema.dump(example_objects)
    return data


def read_one(example_object_id):
    """
    This function responds to a request for /api/example_objects/{example_object_id}
    with one matching example_object from example_objects
    :param example_object_id:   Id of example_object to find
    :return:            example_object matching id
    """
    # Get the example_object requested
    example_object = ExampleObject.query.filter(ExampleObject.example_object_id == example_object_id).one_or_none()

    # Did we find a example_object?
    if example_object is not None:

        # Serialize the data for the response
        example_object_schema = ExampleObjectSchema()
        data = example_object_schema.dump(example_object)
        return data

    # Otherwise, nope, didn't find that example_object
    else:
        abort(
            404,
            "ExampleObject not found for Id: {example_object_id}".format(example_object_id=example_object_id),
        )


def create(example_object):
    """
    This function creates a new example_object in the example_objects structure
    based on the passed in example_object data
    :param example_object:  example_object to create in example_objects structure
    :return:        201 on success, 406 on example_object exists
    """
    field1 = example_object.get("field1")
    field2 = example_object.get("field2")

    existing_example_object = (
        ExampleObject.query.filter(ExampleObject.field1 == field1)
        .filter(ExampleObject.field2 == field2)
        .one_or_none()
    )

    # Can we insert this example_object?
    if existing_example_object is None:

        # Create a example_object instance using the schema and the passed in example_object
        schema = ExampleObjectSchema()
        new_example_object = schema.load(example_object, session=db.session)

        # Add the example_object to the database
        db.session.add(new_example_object)
        db.session.commit()

        # Serialize and return the newly created example_object in the response
        data = schema.dump(new_example_object)

        return data, 201

    # Otherwise, nope, example_object exists already
    else:
        abort(
            409,
            "ExampleObject {field1} {field2} exists already".format(
                field1=field1, field2=field2
            ),
        )


def update(example_object_id, example_object):
    """
    This function updates an existing example_object in the example_objects structure
    Throws an error if a example_object with the name we want to update to
    already exists in the database.
    :param example_object_id:   Id of the example_object to update in the example_objects structure
    :param example_object:      example_object to update
    :return:            updated example_object structure
    """
    # Get the example_object requested from the db into session
    update_example_object = ExampleObject.query.filter(
        ExampleObject.example_object_id == example_object_id
    ).one_or_none()

    # Try to find an existing example_object with the same name as the update
    field1 = example_object.get("field1")
    field2 = example_object.get("field2")

    existing_example_object = (
        ExampleObject.query.filter(ExampleObject.field1 == field1)
        .filter(ExampleObject.field2 == field2)
        .one_or_none()
    )

    # Are we trying to find a example_object that does not exist?
    if update_example_object is None:
        abort(
            404,
            "ExampleObject not found for Id: {example_object_id}".format(example_object_id=example_object_id),
        )

    # Would our update create a duplicate of another example_object already existing?
    elif (
        existing_example_object is not None and existing_example_object.example_object_id != example_object_id
    ):
        abort(
            409,
            "ExampleObject {field1} {field2} exists already".format(
                field1=field1, field2=field2
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in example_object into a db object
        schema = ExampleObjectSchema()
        update = schema.load(example_object, session=db.session)

        # Set the id to the example_object we want to update
        update.example_object_id = update_example_object.example_object_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated example_object in the response
        data = schema.dump(update_example_object)

        return data, 200


def delete(example_object_id):
    """
    This function deletes a example_object from the example_objects structure
    :param example_object_id:   Id of the example_object to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the example_object requested
    example_object = ExampleObject.query.filter(ExampleObject.example_object_id == example_object_id).one_or_none()

    # Did we find a example_object?
    if example_object is not None:
        db.session.delete(example_object)
        db.session.commit()
        return make_response(
            "ExampleObject {example_object_id} deleted".format(example_object_id=example_object_id), 200
        )

    # Otherwise, nope, didn't find that example_object
    else:
        abort(
            404,
            "ExampleObject not found for Id: {example_object_id}".format(example_object_id=example_object_id),
        )