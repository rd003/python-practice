from marshmallow import Schema, fields, validate

class PersonSchema(Schema):
    id = fields.Int(dump_only=True)
    firstName = fields.Str(
        data_key='firstName',
        attribute='first_name',
        required=True,
        allow_none=False,
        validate=validate.Length(min=1, max=30, error="First name must be between 1 and 30 characters"),
        error_messages={
            'required': 'First name is required',
            'null': 'First name should not be null'
        }
    )
    lastName = fields.Str(
        data_key="lastName",
        attribute='last_name',
        required=True,
        allow_none=False,
        validate=validate.Length(min=1, max=30, error="Last name must be between 1 and 30 characters"),
        error_messages={
            'required': 'Last name is required',
            'null': 'Last name should not be null'
        }
    )

    class Meta:
        strict = True

class PersonUpdateSchema(Schema):
    firstName = fields.Str(
        data_key='firstName',
        attribute='first_name',
        allow_none=False,
        validate=validate.Length(min=1, max=30, error="First name must be between 1 and 30 characters"),
        error_messages={'null': 'First name should not be null'}
    )
    lastName = fields.Str(
        data_key="lastName",
        attribute='last_name',
        allow_none=False,
        validate=validate.Length(min=1, max=30, error="Last name must be between 1 and 30 characters"),
        error_messages={'null': 'Last name should not be null'}
    )
    
    class Meta:
        strict = True 
