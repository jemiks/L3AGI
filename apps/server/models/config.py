from __future__ import annotations
from typing import List, Optional
import uuid

from sqlalchemy import Column, String, Boolean, UUID, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import and_, or_
from models.base_model import BaseModel
from typings.config import ConfigInput, ConfigQueryParams, AccountSettings
from exceptions import ConfigNotFoundException
from utils.encyption import encrypt_data, decrypt_data, is_encrypted

import uuid

class ConfigModel(BaseModel):
    """
    Model representing a tool configuration.

    Attributes:
        id (UUID): The primary key of the tool configuration.
        key (String): The key of the tool configuration.
        agent_id (UUID): The ID of the agent associated with the configuration.
        toolkit_id (UUID): The ID of the toolkit associated with the configuration.
        account_id (UUID): The ID of the account associated with the configuration.
        workspace_id (UUID): The ID of the project associated with the configuration.
        datasource_id (UUID): The ID of the datasource associated with the configuration.
        value (String): The value of the tool configuration.
        key_type (String): The type of key used.
        is_secret (Boolean): Whether the tool configuration is a secret.
        is_required (Boolean): Whether the tool configuration is a required field.
        is_deleted (Boolean): Whether the tool configuration is deleted.
    """
    __tablename__ = 'config'


    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    key = Column(String, index=True)
    agent_id = Column(UUID,ForeignKey('agent.id', ondelete='CASCADE'), nullable=True, index=True)
    toolkit_id = Column(UUID, nullable=True)
    account_id = Column(UUID, ForeignKey('account.id', ondelete='CASCADE'), nullable=True)
    workspace_id = Column(UUID, ForeignKey('workspace.id', ondelete='CASCADE'), nullable=True, index=True)
    datasource_id = Column(UUID, ForeignKey('datasource.id', ondelete='CASCADE'), nullable=True, index=True)
    team_id = Column(UUID, ForeignKey('team.id', ondelete='CASCADE'), nullable=True, index=True)
    team_agent_id = Column(UUID, ForeignKey('team_agent.id', ondelete='CASCADE'), nullable=True, index=True)
    value = Column(String)
    key_type = Column(String)
    is_secret = Column(Boolean)
    is_required = Column(Boolean)    
    is_deleted = Column(Boolean, default=False, index=True)
    
        
    created_by = Column(UUID, ForeignKey('user.id', name='fk_created_by', ondelete='CASCADE'), nullable=True, index=True)
    modified_by = Column(UUID, ForeignKey('user.id', name='fk_modified_by', ondelete='CASCADE'), nullable=True, index=True)
    creator = relationship("UserModel", foreign_keys=[created_by], cascade="all, delete", lazy='select')

    # Define indexes
    Index('ix_config_model_created_by_is_deleted', 'created_by', 'is_deleted')
    Index('ix_config_model_id_is_deleted', 'id', 'is_deleted')
    
    def __repr__(self) -> str:
        return (
            f"Config(id={self.id}, "
            f"key='{self.key}', value='{self.value}', "
            f"key_type='{self.key_type}', is_secret={self.is_secret}, is_required={self.is_required}, "
            f"is_deleted={self.is_deleted}, account_id={self.account_id})"
        )

    @classmethod
    def create_config(cls, db, config, user, account):
        """
        Creates a new config with the provided configuration.

        Args:
            db: The database object.
            config_with_config: The object containing the config and configuration details.

        Returns:
            Config: The created config.

        """
        db_config = ConfigModel(
                         created_by=user.id, 
                         account_id=account.id,
                         )
        cls.update_model_from_input(db_config, config)
        if db_config.is_secret:
            db_config.value = encrypt_data(db_config.value)
        db.session.add(db_config)
        db.session.flush()  # Flush pending changes to generate the config's ID
        db.session.commit()
        
        return db_config
       
    @classmethod
    def update_config(cls, db, id, config, user, account):
        """
        Creates a new config with the provided configuration.

        Args:
            db: The database object.
            config_with_config: The object containing the config and configuration details.

        Returns:
            Config: The created config.

        """
        old_config = cls.get_config_by_id(db=db, config_id=id, account=account)
        if not old_config:
            raise ConfigNotFoundException("Config not found")
        db_config = cls.update_model_from_input(config_model=old_config, config_input=config)

        if db_config.is_secret:
            db_config.value = encrypt_data(db_config.value)
        db_config.modified_by = user.id
        db.session.add(db_config)
        db.session.commit()

        return db_config
     
    @classmethod
    def update_model_from_input(cls, config_model: ConfigModel, config_input: ConfigInput):
        for field in ConfigInput.__annotations__.keys():
            setattr(config_model, field, getattr(config_input, field))
            
        return config_model  
    
    @classmethod
    def get_configs(cls, db, query:ConfigQueryParams, account):        
        filter_conditions = [ConfigModel.account_id == account.id, or_(or_(ConfigModel.is_deleted == False, ConfigModel.is_deleted is None), ConfigModel.is_deleted is None)]

        # Iterate over fields in ConfigQueryParams
        for field in ConfigQueryParams.__annotations__.keys():
            # If the field value is not None, add it to the filter conditions
            if getattr(query, field) is not None:
                filter_conditions.append(getattr(ConfigModel, field) == getattr(query, field))

        # Query the database with the filter conditions
        configs = (
            db.session.query(ConfigModel)
            .filter(and_(*filter_conditions))
            .all()
        )
        for config in configs:
            if config and config.is_secret and is_encrypted(config.value):
                config.value = decrypt_data(config.value)
        return configs
    

    @classmethod
    def get_config_by_id(cls, db, config_id, account):
        """
            Get Config from config_id

            Args:
                session: The database session.
                config_id(int) : Unique identifier of an Config.

            Returns:
                Config: Config object is returned.
        """
        config = (
            db.session.query(ConfigModel)
            .filter(ConfigModel.id == config_id, or_(or_(ConfigModel.is_deleted == False, ConfigModel.is_deleted is None), ConfigModel.is_deleted is None))
            .first()
        )
        if config and config.is_secret and is_encrypted(config.value):
            config.value = decrypt_data(config.value)
            
        return config
    
    @classmethod
    def get_account_settings(cls, db, account) -> AccountSettings:
        keys = ["open_api_key", "hugging_face_token"]

        configs: List[ConfigModel] = (
            db.session.query(ConfigModel)
            .filter(ConfigModel.key.in_(keys), ConfigModel.account_id == account.id, or_(or_(ConfigModel.is_deleted == False, ConfigModel.is_deleted is None), ConfigModel.is_deleted is None))
            .all()
        )

        config = {}

        for cfg in configs:
            config[cfg.key] = decrypt_data(cfg.value) if is_encrypted(cfg.value) else cfg.value

        return AccountSettings(openai_api_key=config.get("open_api_key"), hugging_face_auth_token=config.get("hugging_face_token"))

    @classmethod
    def delete_by_id(cls, db, config_id, account):
        db_config = db.session.query(ConfigModel).filter(ConfigModel.id == config_id, ConfigModel.account_id==account.id).first()

        if not db_config or db_config.is_deleted:
            raise ConfigNotFoundException("Config not found")

        db_config.is_deleted = True
        db.session.commit()

    

    