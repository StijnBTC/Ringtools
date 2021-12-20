from abc import ABC, abstractmethod
class LNClient(ABC):

    @abstractmethod
    def get_edge(self, channel_id):
        pass

    @abstractmethod
    def get_node_channels(self, pub_key):
        pass

    @abstractmethod
    def get_node_alias(self, pub_key):
        pass

    @abstractmethod
    def get_node(self, pub_key):
        pass
