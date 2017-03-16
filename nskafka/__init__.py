__title__ = 'kafka'
from .version import __version__
__author__ = 'Dana Powers'
__license__ = 'Apache License 2.0'
__copyright__ = 'Copyright 2016 Dana Powers, David Arthur, and Contributors'

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())


from nskafka.consumer import KafkaConsumer
from nskafka.producer import KafkaProducer
from nskafka.conn import BrokerConnection
from nskafka.protocol import (
    create_message, create_gzip_message, create_snappy_message)
from nskafka.partitioner import RoundRobinPartitioner, HashedPartitioner, Murmur2Partitioner
from nskafka.structs import TopicPartition

# To be deprecated when KafkaProducer interface is released
from nskafka.client import SimpleClient
from nskafka.producer import SimpleProducer, KeyedProducer

# deprecated in favor of KafkaConsumer
from nskafka.consumer import SimpleConsumer, MultiProcessConsumer


import warnings
class KafkaClient(SimpleClient):
    def __init__(self, *args, **kwargs):
        warnings.warn('The legacy KafkaClient interface has been moved to'
                      ' kafka.SimpleClient - this import will break in a'
                      ' future release', DeprecationWarning)
        super(KafkaClient, self).__init__(*args, **kwargs)


__all__ = [
    'KafkaConsumer', 'KafkaProducer', 'KafkaClient', 'BrokerConnection',
    'SimpleClient', 'SimpleProducer', 'KeyedProducer',
    'RoundRobinPartitioner', 'HashedPartitioner',
    'create_message', 'create_gzip_message', 'create_snappy_message',
    'SimpleConsumer', 'MultiProcessConsumer',
]
