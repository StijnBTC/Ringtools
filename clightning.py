from os.path import expanduser

from pyln.client import LightningRpc
import argparse
from lnclient import LNClient

class CLightning(LNClient):
    def __init__(self, clrpc):
        self.rpc = LightningRpc(clrpc)

    # TODO: handle invalid channel ids
    def get_edge(self, channel_id):
        response = self.rpc.listchannels(short_channel_id=channel_id)['channels']
        return self.convert_cl_to_lnd(response)

    def get_node_channels(self, pub_key):
        response =self.rpc.listchannels(source=pub_key)['channels']

        output = argparse.Namespace()
        output.channels = []
        for r in response:
            output.channels.append(self.get_edge(r['short_channel_id']))
        return output

    def get_node_alias(self, pub_key):
        return self.get_node(pub_key).alias

    def get_node(self, pub_key):
        return argparse.Namespace(**self.rpc.listnodes(pub_key)['nodes'][0])

    def convert_cl_to_lnd(self, d):
        output = argparse.Namespace()
        output.channel_id = d[0]['short_channel_id']
        output.node1_pub = d[0]['source']
        output.node2_pub = d[0]['destination']

        output.node1_policy = argparse.Namespace()
        output.node2_policy = argparse.Namespace()

        output.node1_policy.disabled = not d[0]['active']

        if (len(d) > 1):
            output.node2_policy.disabled =  not d[1]['active']

        output.node1_policy.fee_base_msat = d[0]['base_fee_millisatoshi']
        output.node1_policy.fee_rate_milli_msat = d[0]['fee_per_millionth']  

        if (len(d) > 1):
            output.node2_policy.fee_base_msat = d[1]['base_fee_millisatoshi']   
            output.node2_policy.fee_rate_milli_msat = d[1]['fee_per_millionth'] 

        return output