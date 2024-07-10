from rabbitmq.producer import RabbitMQProducer

producer_instance = RabbitMQProducer()

def get_producer() -> RabbitMQProducer:
    return producer_instance