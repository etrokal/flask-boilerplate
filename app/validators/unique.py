from wtforms import ValidationError


class Unique(object):
    """Validator that checks field uniqueness in the database"""

    def __init__(self,  model, field, message: str | None = None,):
        self.model = model
        self.field = field
        if not message:
            message = u'This value already exists'
        self.message = message

    def __call__(self, form, field):
        existing = self.model.query.filter(
            self.field == field.data).first()

        record_id = getattr(form, 'id', None)
        if record_id:
            record_id = record_id.data
        else:
            record_id = None

        if existing and (record_id is None or record_id != existing.id):
            raise ValidationError(self.message)
