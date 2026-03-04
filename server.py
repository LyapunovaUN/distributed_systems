import grpc
from concurrent import futures

import task_pb2
import task_pb2_grpc


# 🧠 База данных: у каждого пользователя свой список задач
tasks_db = {
    1: [
        {"title": "Купить продукты", "completed": False},
        {"title": "Сделать лабораторную", "completed": True},
    ],
    2: [
        {"title": "Пойти в зал", "completed": False},
        {"title": "Сделать ДЗ", "completed": False},
    ],
    3: [
        {"title": "Прочитать книгу", "completed": True},
        {"title": "Сделать проект", "completed": False},
    ],
    4: [
        {"title": "Позвонить другу", "completed": True},
        {"title": "Убраться", "completed": False},
    ],
    5: [
        {"title": "Сходить в магазин", "completed": True},
        {"title": "Посмотреть лекцию", "completed": False},
    ],
    6: [
        {"title": "Написать код", "completed": False},
        {"title": "Пройти тест", "completed": True},
    ],
    7: [
        {"title": "Погулять", "completed": False},
        {"title": "Приготовить еду", "completed": True},
    ],
    8: [
        {"title": "Сделать зарядку", "completed": False},
        {"title": "Почитать новости", "completed": True},
    ],
    9: [
        {"title": "Поработать", "completed": False},
        {"title": "Отдохнуть", "completed": True},
    ],
    10: [
        {"title": "Сдать лабу", "completed": False},
        {"title": "Подготовиться к экзамену", "completed": False},
    ],
}


class TaskManager(task_pb2_grpc.TaskManagerServicer):

    def GetTasksForUser(self, request, context):
        user_id = request.user_id
        print(f"Запрос задач для user_id = {user_id}")

        user_tasks = tasks_db.get(user_id, [])

        for i, task in enumerate(user_tasks, start=1):  # 👈 нумерация с 1
            yield task_pb2.Task(
                id=i,
                title=task["title"],
                completed=task["completed"]
            )

    def UpdateTaskStatus(self, request, context):
        user_id = request.user_id
        task_number = request.task_number

        user_tasks = tasks_db.get(user_id)

        if not user_tasks:
            return task_pb2.UpdateTaskResponse(
                message="Пользователь не найден"
            )

        if task_number < 1 or task_number > len(user_tasks):
            return task_pb2.UpdateTaskResponse(
                message="Неверный номер задачи"
            )

        # 👇 меняем статус
        user_tasks[task_number - 1]["completed"] = request.completed

        return task_pb2.UpdateTaskResponse(
            message="Статус обновлён"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_pb2_grpc.add_TaskManagerServicer_to_server(
        TaskManager(), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()

    print("Сервер запущен на порту 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
