
from fastapi import  Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter

import schema, models
from utils import get_db
from sqlalchemy.orm import Session
from config import get_settings
from fastapi_utils.cbv import cbv
from fastapi_utils.api_model import APIMessage
from starlette.status import HTTP_400_BAD_REQUEST

router = InferringRouter()
settings = get_settings()


@cbv(router)
class TaskView:
    session: Session = Depends(get_db)

    @router.get("/tasks")
    def get_tasks(self) -> list[models.Tasks]:
        task_orm = self.session.query(models.Tasks).all()
        return schema.Task.from_orm(task_orm)

    @router.post("/tasks")
    def create_task(self, task: schema.Task) -> schema.Task:
        task_orm = models.Tasks(**task.dict())
        self.session.add(task_orm)
        self.session.commit()
        return schema.Task.from_orm(task_orm)

    @router.get("/task/{task_id}")
    def read_task(self, task_id) -> schema.Task:
        task_orm = self.session.query(models.Tasks).get(task_id)
        return schema.Task.from_orm(task_orm)

    @router.put("/item/{item_id}")
    def update_item(self, task_id, task: schema.Task) -> schema.Task:
        task_orm = self.session.query(models.Tasks).get(task_id)

        task_orm.title = task.title
        task_orm.description = task.description
        task_orm.assigned_to = task.assigned_to

        self.session.add(task_orm)
        self.session.commit()
        return schema.Task.from_orm(task_orm)

    @router.post("/item/{item_id}/assign")
    def assign_task(self, task_id, assignee: schema.TaskAssign) -> schema.Task:
        task_orm = self.session.query(models.Tasks).filter(models.Tasks.assigned_to == assignee.assigned_to)
        if task_orm.count() < settings.MAX_ASSIGN_VALUE:
            task_orm.assigned_to = assignee.assigned_to
            self.session.add(task_orm)
            self.session.commit()
            return schema.Task.from_orm(task_orm)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail=f"Cant assign more than {settings.MAX_ASSIGN_VALUE} to user")

    @router.delete("/task/{task_id}")
    def delete_task(self, task_id) -> APIMessage:
        task = self.session.query(models.Tasks).get(task_id)
        self.session.delete(task)
        self.session.commit()
        return APIMessage(detail=f"Deleted task {task_id}")


@cbv(router)
class UserView:
    session: Session = Depends(get_db)

    @router.get("user/{user_id}/tasks")
    def get_user_tasks(self, user_id) -> list[Tasks]:
        user = self.session.query(models.User).get(user_id)
        return self.session.query(models.Tasks).filter(
            models.Tasks.assigned_to == user)

    @router.post("/users")
    def create_user(self, user: schema.UserCreate) -> schema.User:
        user_orm = models.User(**user.dict())
        self.session.add(user_orm)
        self.session.commit()
        return schema.User.from_orm(user_orm)

    @router.get("/users/{users_id}")
    def read_user(self, user_id) -> schema.Task:
        user_orm = self.session.query(models.User).get(user_id)
        return schema.Task.from_orm(user_orm)

    @router.put("/user/{user_id}")
    def update_user(self, user_id, user: schema.User) -> Tasks:
        user_orm = self.session.query(models.User).get(user_id)

        user_orm.email = user.email
        user_orm.username = user.user_name

        self.session.add(user_orm)
        self.session.commit()
        return schema.User.from_orm(user_orm)

    @router.delete("/user/{user_id}")
    def delete_task(self, user_id) -> APIMessage:
        user = self.session.query(models.Tasks).get(user_id)
        self.session.delete(user)
        self.session.commit()
        return APIMessage(detail=f"Deleted user {user_id}")
