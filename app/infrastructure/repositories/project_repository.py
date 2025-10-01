from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models.project import Project as DomainProject
from app.domain.repositories import AbstractProjectRepository
from app.infrastructure.orm.project import Project as ORMProject

class SqlAlchemyProjectRepository(AbstractProjectRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, project_id: int) -> Optional[DomainProject]:
        project_orm = self.session.query(ORMProject).filter(ORMProject.id == project_id).first()
        if project_orm:
            return DomainProject.model_validate(project_orm)
        return None

    def list(self) -> List[DomainProject]:
        projects_orm = self.session.query(ORMProject).all()
        return [DomainProject.model_validate(p) for p in projects_orm]

    def add(self, project: DomainProject) -> DomainProject:
        project_orm = ORMProject(**project.model_dump())
        self.session.add(project_orm)
        self.session.commit()
        self.session.refresh(project_orm)
        return DomainProject.model_validate(project_orm)
    
    def update(self, project: DomainProject) -> DomainProject:
        project_orm = self.session.query(ORMProject).filter(ORMProject.id == project.id).first()

        if not project_orm:
            raise ValueError(f"Project with id {project.id} not found")
        
        project_data = project.model_dump(exclude_unset=True)
        for key, value in project_data.items():
            setattr(project_orm, key, value)
        
        self.session.commit()
        self.session.refresh(project_orm)
        return DomainProject.model_validate(project_orm)

    def delete(self, project_id: int) -> None:
        project_orm = self.session.query(ORMProject).filter(ORMProject.id == project_id).first()
        if project_orm:
            self.session.delete(project_orm)
            self.session.commit()
