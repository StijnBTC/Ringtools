import codecs
import os
from functools import lru_cache
from os.path import expanduser

import grpc

from grpc_gen import router_pb2 as lnrouter
from grpc_gen import router_pb2_grpc as lnrouterrpc
from grpc_gen import lightning_pb2 as ln
from grpc_gen import lightning_bp2_grpc as lnrpc

MESSAGE_SIZE_MB = 50 * 1024 * 1024


class Lnd:
    def __init__(self, lnd_dir, server):
        os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
        lnd_dir = expanduser(lnd_dir)
        combined_credentials = self.get_credentials(lnd_dir)
        channel_options = [
            ("grpc.max_message_length", MESSAGE_SIZE_MB),
            ("grpc.max_receive_message_length", MESSAGE_SIZE_MB),
        ]
        grpc_channel = grpc.secure_channel(
            server, combined_credentials, channel_options
        )
        self.stub = lnrpc.LightningStub(grpc_channel)
        self.router_stub = lnrouterrpc.RouterStub(grpc_channel)

    @staticmethod
    def get_credentials(lnd_dir):
        with open(f"{lnd_dir}/tls.cert", "rb") as f:
            tls_certificate = f.read()
        ssl_credentials = grpc.ssl_channel_credentials(tls_certificate)
        with open(f"{lnd_dir}/data/chain/bitcoin/mainnet/readonly.macaroon", "rb") as f:
            macaroon = codecs.encode(f.read(), "hex")
        auth_credentials = grpc.metadata_call_credentials(
            lambda _, callback: callback([("macaroon", macaroon)], None)
        )
        combined_credentials = grpc.composite_channel_credentials(
            ssl_credentials, auth_credentials
        )
        return combined_credentials

    # TODO: handle invalid channel ids
    @lru_cache(maxsize=None)
    def get_edge(self, channel_id):
        return self.stub.GetChanInfo(ln.ChanInfoRequest(chan_id=channel_id))


    @lru_cache(maxsize=None)
    def get_node_channels(self, pubkey):
        return self.stub.GetNodeInfo(ln.NodeInfoRequest(
            
            pub_key=pubkey, include_channels=True))

    @lru_cache(maxsize=None)
    def get_node_alias(self, pub_key):
        return self.stub.GetNodeInfo(
            ln.NodeInfoRequest(pub_key=pub_key, include_channels=False)
        ).node.alias

    @lru_cache(maxsize=None)
    def get_node(self, pub_key):
        return self.stub.GetNodeInfo(
            ln.NodeInfoRequest(pub_key=pub_key, include_channels=False)
        ).node
