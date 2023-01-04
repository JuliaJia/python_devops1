from mongoengine import (
    Document,EmbeddedDocument,
    StringField,IntField,BooleanField,
    ListField,EmbeddedDocumentField
)
# Create your models here.

class CiTypeField(EmbeddedDocument):
    meta = {'collection': 'citypes'}
    name = StringField(required=True,max_length=24)
    label = StringField(max_length=24)
    type = StringField(max_length=24)
    required = BooleanField(default=False)
    
    def __str__(self):
        return "<F {},{}>".format(self.name,self.type)

class CiType(Document):
    meta = {'collection': 'citypes'}
    name = StringField(required=True,unique_with='version',max_length=24)
    label = StringField(max_length=24)
    version = IntField(required=True,default=1)
    fields = ListField(EmbeddedDocumentField(CiTypeField))

    def __str__(self):
        return "CiType {}:{}, {}".format(
            self.name, self.version,self.fields
        )