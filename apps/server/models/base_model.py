import json
from sqlalchemy import Column, DateTime, UUID, ForeignKey
from datetime import datetime
from models.db import Base

class BaseModel(Base):
    """
    BaseModel is an abstract base class for all SQLAlchemy ORM models ,
    providing common columns and functionality.

    Attributes:
        created_on: Datetime column to store the timestamp about when a row is created.
        updated_on: Datetime column to store the timestamp about when a row is updated.

    Methods:
        to_dict: Converts the current object to a dictionary.
        to_json: Converts the current object to a JSON string.
        from_json: Creates a new object of the class using the provided JSON data.
        __repr__: Returns a string representation of the current object.
    """
    __abstract__ = True
    created_on = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_on = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    
    def to_dict(self):
        """
        Converts the current SQLAlchemy ORM object to a dictionary representation.

        Returns:
            A dictionary mapping column names to their corresponding values.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def to_json(self):
        """
            Converts the current SQLAlchemy ORM object to a JSON string representation.

            Returns:
                A JSON string representing the object with column names as keys and their corresponding values.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_data):
        """
            Creates a new SQLAlchemy ORM object of the class using the provided JSON data.

            Args: json_data (str): A JSON string representing the object with column names as keys and their
            corresponding values.

            Returns:
                A new SQLAlchemy ORM object of the class.
        """
        return cls(**json.loads(json_data))

    def __repr__(self):
        """
            Returns a string representation of the current SQLAlchemy ORM object.

            Returns:
                A string with the format "<Class Name> (<dictionary representation of the object>)".
        """
        return f"{self.__class__.__name__} ({self.to_dict()})"
    
class RootBaseModel(Base):
    """
    BaseModel is an abstract base class for all SQLAlchemy ORM models ,
    providing common columns and functionality.

    Attributes:
        created_on: Datetime column to store the timestamp about when a row is created.
        updated_on: Datetime column to store the timestamp about when a row is updated.

    Methods:
        to_dict: Converts the current object to a dictionary.
        to_json: Converts the current object to a JSON string.
        from_json: Creates a new object of the class using the provided JSON data.
        __repr__: Returns a string representation of the current object.
    """
    __abstract__ = True
    
    def to_dict(self):
        """
        Converts the current SQLAlchemy ORM object to a dictionary representation.

        Returns:
            A dictionary mapping column names to their corresponding values.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def to_json(self):
        """
            Converts the current SQLAlchemy ORM object to a JSON string representation.

            Returns:
                A JSON string representing the object with column names as keys and their corresponding values.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_data):
        """
            Creates a new SQLAlchemy ORM object of the class using the provided JSON data.

            Args: json_data (str): A JSON string representing the object with column names as keys and their
            corresponding values.

            Returns:
                A new SQLAlchemy ORM object of the class.
        """
        return cls(**json.loads(json_data))

    def __repr__(self):
        """
            Returns a string representation of the current SQLAlchemy ORM object.

            Returns:
                A string with the format "<Class Name> (<dictionary representation of the object>)".
        """
        return f"{self.__class__.__name__} ({self.to_dict()})"
