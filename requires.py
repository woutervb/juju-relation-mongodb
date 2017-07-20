#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class MongoDBClient(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:mongodb}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')

    @hook('{requires:mongodb}-relation-changed')
    def changed(self):
        if self.connection_strings():
            self.set_state('{relation_name}.database.available')
            self.set_state('{relation_name}.available')
        else:
            self.set_state('{relation_name}.removed')

    @hook('{requires:mongodb}-relation-{broken,departed}')
    def broken_departed(self):
        self.remove_state('{relation_name}.connected')

    @hook('{requires:mongodb}-relation-broken')
    def broken(self):
        self.set_state('{relation_name}.removed')

    def connection_strings(self):
        """
        Get the connection strings for each conversation if available, or [].
        """
        connection_strings = []
        for conv in self.conversations():
            data = {
                'hostname': conv.get_remote('hostname'),
                'port': conv.get_remote('port'),
            }
            if all(data.values()):
                connection_strings.append(str.format('{hostname}:{port}', **data))
        return connection_strings
