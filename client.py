import grpc
import task_pb2
import task_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = task_pb2_grpc.TaskManagerStub(channel)

    while True:
        print("\n1 - Показать задачи")
        print("2 - Изменить статус задачи")
        print("0 - Выход")

        choice = input("Выбор: ")

        if choice == "1":
            user_id = int(input("Введите user_id: "))

            responses = stub.GetTasksForUser(
                task_pb2.UserRequest(user_id=user_id)
            )

            print("\nЗадачи:\n")

            for task in responses:
                status = "✅" if task.completed else "❌"
                print(f"{task.id}. {task.title} {status}")

        elif choice == "2":
            user_id = int(input("User ID: "))
            task_number = int(input("Номер задачи: "))
            status_input = input("Выполнено? (1/0): ")

            completed = True if status_input == "1" else False

            response = stub.UpdateTaskStatus(
                task_pb2.UpdateTaskRequest(
                    user_id=user_id,
                    task_number=task_number,
                    completed=completed
                )
            )

            print(response.message)

        elif choice == "0":
            break

        else:
            print("Неверный ввод")


if __name__ == '__main__':
    run()
