from __future__ import annotations
from typing import List, Optional
import uuid

from sqlalchemy import Column, String, Boolean, UUID, func, or_, ForeignKey, Index
from sqlalchemy.orm import relationship, joinedload, foreign
from models.base_model import BaseModel
from typings.agent import ConfigInput, AgentInput
from models.agent_config import AgentConfigModel
from exceptions import AgentNotFoundException
from models.user import UserModel
from sqlalchemy import Column, DateTime, UUID, ForeignKey
from datetime import datetime
from models.base_model import RootBaseModel

class AgentModel(BaseModel):
    """
    Represents an agent entity.

    Attributes:
        id (UUID): Unique identifier of the agent.
        name (str): Name of the agent.
        role (str): Role of the agent.
        description (str): Description of the agent.
        is_deleted (bool): Flag indicating if the agent has been soft-deleted.
        is_template (bool): Flag indicating if the agent is a template.
        user_id (UUID): ID of the user associated with the agent.
        account_id (UUID): ID of the account associated with the agent.
        is_public (bool): Flag indicating if the agent is a system agent.
        configs: Relationship with agent configurations.
    """ 
    # __abstract__ = True
    __tablename__ = 'agent'
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    role = Column(String) 
    parent_id = Column(UUID, ForeignKey('agent.id', ondelete='CASCADE'), nullable=True, index=True) 
    workspace_id = Column(UUID, ForeignKey('workspace.id', ondelete='CASCADE'), nullable=True, index=True) 
    agent_type = Column(String) # Later add as Enum
    description = Column(String)
    is_deleted = Column(Boolean, default=False, index=True)
    is_template = Column(Boolean, default=False, index=True)
    is_memory = Column(Boolean, default=True)
    avatar = Column(String)
    account_id = Column(UUID, ForeignKey('account.id', ondelete='CASCADE'), nullable=True, index=True)    
    is_public = Column(Boolean, default=False, index=True)
    
    configs = relationship("AgentConfigModel", back_populates="agent", cascade="all, delete", lazy='select')
    chat_messages = relationship("ChatMessage", back_populates="agent", cascade="all, delete", lazy='select')
    team_agents = relationship("TeamAgentModel", back_populates="agent", cascade="all, delete", lazy='select')
    account = relationship("AccountModel", cascade="all, delete", lazy='select')
    
    
    created_by = Column(UUID, ForeignKey('user.id', name='fk_created_by', ondelete='CASCADE'), nullable=True, index=True)
    modified_by = Column(UUID, ForeignKey('user.id', name='fk_modified_by', ondelete='CASCADE'), nullable=True, index=True)
    creator = relationship("UserModel", foreign_keys=[created_by], cascade="all, delete", lazy='select')
    
    # Define indexes
    __table_args__ = (
        Index('ix_agent_model_account_id_is_deleted', 'account_id', 'is_deleted'),
        Index('ix_agent_model_created_by_is_deleted', 'created_by', 'is_deleted'),
        Index('ix_agent_model_id_is_deleted', 'id', 'is_deleted'),
    )
    
    def __repr__(self) -> str:
        return (
            f"Agent(id={self.id}, "
            f"name='{self.name}', role='{self.role}', description='{self.description}', "
            f"is_deleted={self.is_deleted}, is_template={self.is_template}, user_id={self.created_by}, "
            f"account_id={self.account_id}, is_public={self.is_public})"
        )

    @classmethod
    def create_agent(cls, db, agent, configs: List[ConfigInput], user, account):
        """
        Creates a new agent with the provided configuration.

        Args:
            db: The database object.
            agent_with_config: The object containing the agent and configuration details.

        Returns:
            Agent: The created agent.

        """
        db_agent = AgentModel(
                         created_by=user.id, 
                         account_id=account.id,
                         )
        cls.update_model_from_input(db_agent, agent)
        db.session.add(db_agent)
        db.session.flush()  # Flush pending changes to generate the agent's ID
        db.session.commit()

        AgentConfigModel.create_or_update(db, db_agent, configs, user, account)
        
        return db_agent
       
    @classmethod
    def update_agent(cls, db, id, agent, configs: List[ConfigInput], user, account):
        """
        Creates a new agent with the provided configuration.

        Args:
            db: The database object.
            agent_with_config: The object containing the agent and configuration details.

        Returns:
            Agent: The created agent.

        """
        old_agent = cls.get_agent_by_id(db=db, agent_id=id, account=account)
        if not old_agent:
            raise AgentNotFoundException("Agent not found")
        db_agent = cls.update_model_from_input(agent_model=old_agent, agent_input=agent)
        db_agent.modified_by = user.id
        
        db.session.add(db_agent)
        db.session.commit()
        
        AgentConfigModel.create_or_update(db, db_agent, configs, user, account)

        return db_agent
     
    @classmethod
    def update_model_from_input(cls, agent_model: AgentModel, agent_input: AgentInput):
        for field in AgentInput.__annotations__.keys():
            setattr(agent_model, field, getattr(agent_input, field))
        return agent_model  
    
    @classmethod
    def create_agent_from_template(cls, db, template_id, user, account, check_is_template: True):
        """
        Creates a new agent with the provided configuration.

        Args:
            db: The database object.
            agent_with_config: The object containing the agent and configuration details.

        Returns:
            Agent: The crated agent.

        """
        template_agent = cls.get_agent_by_id(db=db, agent_id=template_id, account=account)
        if check_is_template:
            if template_agent is None or not (template_agent.is_public or template_agent.is_template):
                raise AgentNotFoundException("Agent not found")

        new_agent = AgentModel(name=template_agent.name,
                                role=template_agent.role,
                                agent_type=template_agent.agent_type,
                                description=template_agent.description,
                                is_memory=template_agent.is_memory,
                                is_public=False,
                                is_template=False,
                                created_by=user.id, 
                                account_id=account.id,
                                modified_by=None,
                                parent_id=template_agent.id
                                )        
                       
        db.session.add(new_agent)
        db.session.commit() 
        
        
        AgentConfigModel.create_configs_from_template(db=db, 
                                                      configs=template_agent.configs, 
                                                      user=user, 
                                                      agent_id=new_agent.id)     

        return new_agent
     
    @classmethod
    def update_model_from_input(cls, agent_model: AgentModel, agent_input: AgentInput):
        for field in AgentInput.__annotations__.keys():
            setattr(agent_model, field, getattr(agent_input, field))
        return agent_model  

    @classmethod
    def get_agents(cls, db, account):
        agents = (
            db.session.query(AgentModel)
            # .join(AgentConfigModel, AgentModel.id == AgentConfigModel.agent_id)
            .join(UserModel, AgentModel.created_by == UserModel.id)           
            .filter(AgentModel.account_id == account.id, or_(or_(AgentModel.is_deleted == False, AgentModel.is_deleted is None), AgentModel.is_deleted is None))
            # .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            .options(joinedload(AgentModel.creator))
            # .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            # .options(joinedload(UserModel.agents))
            .all()
        )
        return agents

    @classmethod
    def get_template_agents(cls, db):
        agents = (
            db.session.query(AgentModel) 
            .filter(or_(AgentModel.is_deleted == False, AgentModel.is_deleted.is_(None)),
                    AgentModel.is_template == True)
            .options(joinedload(AgentModel.creator))
            .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            .all()
        )
        return agents  

    @classmethod
    def get_public_agents(cls, db):
        agents = (
            db.session.query(AgentModel)
            # .join(AgentConfigModel, AgentModel.id == AgentConfigModel.agent_id)
            .join(UserModel, AgentModel.created_by == UserModel.id)           
            .filter(or_(AgentModel.is_deleted == False, AgentModel.is_deleted.is_(None)),
                    AgentModel.is_public == True)
            .options(joinedload(AgentModel.creator))
            .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            # .options(joinedload(UserModel.agents))
            .all()
        )
        return agents    
    

    @classmethod
    def get_agent_by_id(cls, db, agent_id, account):
        """
            Get Agent from agent_id

            Args:
                session: The database session.
                agent_id(int) : Unique identifier of an Agent.

            Returns:
                Agent: Agent object is returned.
        """
        agent = (
            db.session.query(AgentModel)
            .join(AgentConfigModel, AgentModel.id == AgentConfigModel.agent_id)
            .join(UserModel, AgentModel.created_by == UserModel.id)           
            .filter(AgentModel.id == agent_id, or_(or_(AgentModel.is_deleted == False, AgentModel.is_deleted is None), AgentModel.is_deleted is None))
            .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            .options(joinedload(AgentModel.creator))
            # .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            # .options(joinedload(UserModel.agents))
            .first()
        )
        return agent
    
    @classmethod
    def get_by_parent_id(cls, db, parent_id, account):
        """
            Get Agent from agent_id

            Args:
                session: The database session.
                agent_id(int) : Unique identifier of an Agent.

            Returns:
                Agent: Agent object is returned.
        """
        agent = (
            db.session.query(AgentModel)
            .join(AgentConfigModel, AgentModel.id == AgentConfigModel.agent_id)
            .join(UserModel, AgentModel.created_by == UserModel.id)           
            .filter(AgentModel.parent_id == parent_id, 
                    AgentModel.account_id == account.id, 
                    or_(or_(AgentModel.is_deleted == False, AgentModel.is_deleted is None),
                    AgentModel.is_deleted is None))
            .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            .options(joinedload(AgentModel.creator))
            # .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            # .options(joinedload(UserModel.agents))
            .first()
        )
        return agent
    
    
    
    @classmethod
    def get_agent_by_id_with_account(cls, db, agent_id):
        """
            Get Agent from agent_id

            Args:
                session: The database session.
                agent_id(int) : Unique identifier of an Agent.

            Returns:
                Agent: Agent object is returned.
        """
        # return db.session.query(AgentModel).filter(AgentModel.account_id == account.id, or_(or_(AgentModel.is_deleted == False, AgentModel.is_deleted is None), AgentModel.is_deleted is None)).all()
        agents = (
            db.session.query(AgentModel)
            .join(AgentConfigModel, AgentModel.id == AgentConfigModel.agent_id)
            .join(UserModel, AgentModel.created_by == UserModel.id)           
            .filter(AgentModel.id == agent_id, or_(or_(AgentModel.is_deleted == False, AgentModel.is_deleted is None), AgentModel.is_deleted is None))
            .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            .options(joinedload(AgentModel.creator))
            .options(joinedload(AgentModel.account))
            # .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            # .options(joinedload(UserModel.agents))
            .first()
        )
        return agents

    @classmethod
    def delete_by_id(cls, db, agent_id, account):
        db_agent = db.session.query(AgentModel).filter(AgentModel.id == agent_id, AgentModel.account_id==account.id).first()

        if not db_agent or db_agent.is_deleted:
            raise AgentNotFoundException("Agent not found")

        db_agent.is_deleted = True
        db.session.commit()

    

    