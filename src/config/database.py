"""
Database configuration module for PrTune application.

This module provides SQLAlchemy configuration using environment variables
for PostgreSQL database connectivity.
"""

import os
from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseConfig:
    """Database configuration class that manages SQLAlchemy settings."""
    
    def __init__(self):
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_name = os.getenv("DB_NAME", "prtune")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "")
        
        # Alternative: Use DATABASE_URL if provided
        self.database_url = os.getenv("DATABASE_URL")
        
        # SQLAlchemy settings
        self.echo = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"
        self.pool_size = int(os.getenv("SQLALCHEMY_POOL_SIZE", "10"))
        self.max_overflow = int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", "20"))
        
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
    
    def get_connection_string(self) -> str:
        """
        Generate PostgreSQL connection string from environment variables.
        
        Returns:
            str: SQLAlchemy compatible connection string
        """
        if self.database_url:
            return self.database_url
            
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    
    def get_engine(self) -> Engine:
        """
        Get or create SQLAlchemy engine instance.
        
        Returns:
            Engine: SQLAlchemy engine instance
        """
        if self._engine is None:
            connection_string = self.get_connection_string()
            self._engine = create_engine(
                connection_string,
                echo=self.echo,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_pre_ping=True,  # Enables connection health checks
                pool_recycle=300     # Recycle connections after 5 minutes
            )
        return self._engine
    
    def get_session_factory(self) -> sessionmaker:
        """
        Get or create SQLAlchemy session factory.
        
        Returns:
            sessionmaker: SQLAlchemy session factory
        """
        if self._session_factory is None:
            engine = self.get_engine()
            self._session_factory = sessionmaker(
                bind=engine,
                autocommit=False,
                autoflush=False
            )
        return self._session_factory
    
    def get_session(self) -> Session:
        """
        Create a new database session.
        
        Returns:
            Session: SQLAlchemy session instance
        """
        session_factory = self.get_session_factory()
        return session_factory()


# Global database configuration instance
db_config = DatabaseConfig()

# Convenience functions
def get_engine() -> Engine:
    """Get the global SQLAlchemy engine instance."""
    return db_config.get_engine()

def get_session() -> Session:
    """Get a new database session."""
    return db_config.get_session()