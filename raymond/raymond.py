from elasticsearch import exceptions

class Raymond:
    def __init__(self, discord_client, es):
        self.client = discord_client
        self.es = es

    def get_client(self):
        return self.client

    def set_user(self, member_id, doc):
        body = {
            'doc': doc,
            'doc_as_upsert': True
        }
        res = self.es.update(index='users', id=member_id, body=body)
        print(f'Elasticsearch response: {res}')
        print(f'Member {member_id} {res["result"]}')
        return res['result']

    def get_user(self, member_id):
        try:
            return self.es.get(index='users', id=member_id)
        except exceptions.NotFoundError as ex:
            print(ex)

    def delete_user(self, member_id):
        try:
            return self.es.delete(index='users', id=member_id)
        except exceptions.NotFoundError as ex:
            print(ex)

    def set_island(self, member_id, doc):
        body = {
            'doc': doc,
            'doc_as_upsert': True
        }
        res = self.es.update(index='islands', id=member_id, body=body)
        print(f'Elasticsearch response: {res}')
        print(f'Island {member_id} {res["result"]}')
        return res['result']

    def get_island(self, member_id):
        try:
            return self.es.get(index='islands', id=member_id)
        except exceptions.NotFoundError as ex:
            print(ex)