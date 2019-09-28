from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest

from flask_api.database import db


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create(cls, data: dict) -> "Organization":
        name = data.get("name")
        organization = cls(name=name)
        db.session.add(organization)
        db.session.commit()
        return organization

    @classmethod
    def update(cls, pk: int, data: dict) -> "Organization":
        organization = cls.query.filter(cls.id == pk).one()
        organization.name = data.get("name")
        db.session.add(organization)
        db.session.commit()
        return organization

    @classmethod
    def delete(cls, pk: int) -> None:
        organization = cls.query.filter(cls.id == pk).one()
        db.session.delete(organization)
        db.session.commit()


class Shelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id", ondelete="CASCADE"))
    organization = db.relationship(
        "Organization", backref=db.backref("shelves", lazy="dynamic", cascade="all, delete-orphan")
    )
    size = db.Column(db.SmallInteger)
    available_size = db.Column(db.SmallInteger)

    def __str__(self) -> str:
        return f"{self.organization} - Shelf {self.id}"

    @classmethod
    def create(cls, data: dict) -> "Shelf":
        size = data.get("size")
        organization = Organization.query.filter(Organization.id == data.get("organization_id")).one()
        shelf = cls(size=size, organization=organization)
        db.session.add(shelf)
        shelf.update_available_size(db.session)
        db.session.commit()
        return shelf

    @classmethod
    def update(cls, pk: int, data: dict) -> "Shelf":
        shelf = cls.query.filter(cls.id == pk).one()
        shelf.size = data.get("size")
        db.session.add(shelf)
        shelf.update_available_size(db.session)
        db.session.commit()
        return shelf

    def update_available_size(self, session: Session) -> None:
        counted = self.boxes.count()
        self.available_size = self.size - counted
        if self.available_size < 0:
            raise BadRequest("Size too small")
        session.add(self)

    @classmethod
    def delete(cls, pk: int) -> None:
        shelf = cls.query.filter(cls.id == pk).one()
        db.session.delete(shelf)
        db.session.commit()


class Box(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.Integer, db.ForeignKey("shelf.id", ondelete="CASCADE"))
    shelf = db.relation("Shelf", backref=db.backref("boxes", lazy="dynamic", cascade="all, delete-orphan"))

    def __str__(self) -> str:
        return f"{self.shelf} - Box {self.id}"

    @classmethod
    def create(cls, data: dict) -> "Box":
        shelf = Shelf.query.filter(Shelf.id == data.get("shelf_id")).one()
        box = cls(shelf=shelf)
        db.session.add(box)
        shelf.update_available_size(db.session)
        db.session.commit()
        return box

    @classmethod
    def update(cls, pk: int, data: dict) -> "Box":
        box = cls.query.filter(cls.id == pk).one()
        box.name = data.get("name")
        db.session.add(box)
        db.session.commit()
        return box

    @classmethod
    def delete(cls, pk: int) -> None:
        box = cls.query.filter(cls.id == pk).one()
        db.session.delete(box)
        box.shelf.update_available_size(db.session)
        db.session.commit()
