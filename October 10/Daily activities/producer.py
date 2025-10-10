import pika
import json

#connect to rabbitMQ
connection= pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#create a queue_declare(idempotent - create only if not existing)
channel.queue_declare(queue="student_tasks")

#prepare a message
task= {
    "student_id" : 101,
    "action" : "generate_cerificate",
    "email" : "rahul@example.com"
}
#publish the message to the queue
channel.basic_publish(
    exchange='',
    routing_key='student_tasks',
    body=json.dumps(task),
)

print("Task sen to queue", task)
connection.close()


