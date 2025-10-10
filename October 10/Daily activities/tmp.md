### what is RabbitMQ
- RabbitMQ is an open-source message broker software that facilitates communication between different parts of a system by sending messages between producers and consumers. It implements the Advanced Message Queuing Protocol (AMQP), which allows applications to communicate asynchronously by passing messages through queues.

### why use a queue in real time systems
Using a queue in real-time systems is super helpful for several reasons. Here’s why queues are often used in these kinds of systems:

- 1. Decoupling Components
Queues let different parts of a system work independently.
For example, if one part produces data faster than another can process it, the queue acts as a buffer.
This decoupling means the producer and consumer don’t have to be online or ready at the same time.

- 2. Load Leveling (Handling Bursts)
Real-time systems often get bursts of data or requests.
A queue can smooth out these spikes by holding the excess messages and feeding them to the consumer at a manageable rate.
This prevents system overload and keeps everything running smoothly.

- 3. Reliability and Fault Tolerance
If a consumer temporarily fails or slows down, the queue stores messages safely.
Once the consumer is back, it can pick up where it left off.
This improves system resilience and ensures messages aren’t lost.

- 4. Asynchronous Processing
Real-time systems often need to react quickly to events.
Queues allow producers to send messages immediately without waiting for consumers to finish processing.
This helps maintain low latency and keeps the system responsive.

- 5. Prioritization and Ordering
Some queue systems let you prioritize certain messages or ensure strict processing order.
This is crucial in real-time systems where the timing or sequence of events matters.

### usecases
- Real-time chat and messaging apps
- order processing in e-commerce
- IoT and sensor data collection
- background task processingmicroservices communication
- financial transactions and trading
- real-time notifications and alerts
- gaming servers
