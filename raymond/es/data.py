from elasticsearch import Elasticsearch


es = Elasticsearch()


def build_get_by_name_query(name):
    return {
        "query": {
            "match": {
                "Name": {
                    "query": name,
                    "operator": "and"
                }
            }
        }
    }


def get_by_name(index, name, return_attributes=None, image_attribute=None):
    result = es.search(index=index, body=build_get_by_name_query(name))['hits']['hits']
    if len(result) == 0:
        return None
    source = result[0]['_source']
    ret_attr = {}
    if return_attributes:
        for attr in return_attributes:
            ret_attr[attr] = source[attr]
    data = {
        'Name': source['Name'],
        'Attributes': ret_attr
    }
    if image_attribute:
        data['Image Link'] = source[image_attribute]
    return data


def build_get_by_multiple_fields_query(fields):
    must_queries = [{"term": {k: v}} for k,v in fields.items()]
    return {
        "query": {
            "bool": {
                "must": must_queries
            }
        }
    }

def get_multiple_by_name(index, name, return_attributes=None):
    result = es.search(index=index, body=build_get_by_name_query(name))['hits']['hits']
    if len(result) == 0:
        return None
    records = [result[i]['_source'] for i in range(len(result))]
    data = []
    if return_attributes:
        for record in records:
            ret_attr = {}
            for attr in return_attributes:
                ret_attr[attr] = record[attr]
            data.append(ret_attr)
    return data

def get_by_fields(index, fields, return_attributes=None, image_attribute=None):
    result = es.search(index=index, body=build_get_by_multiple_fields_query(fields))['hits']['hits']
    if len(result) == 0:
        return None
    records = [result[i]['_source'] for i in range(len(result))]
    results = []
    for record in records:
        ret_attr = {}
        if return_attributes:
            for attr in return_attributes:
                ret_attr[attr] = record[attr]
        data = {
            'Name': record['Name'],
            'Attributes': ret_attr
        }
        if image_attribute:
            data['Image Link'] = record[image_attribute]
        results.append(data)
    return results

def build_get_by_wildcard_query(attr, value):
    query = {
        "size": 100,
        "query": {
            "wildcard": {
                attr: {
                    "value": "*{}*".format(value)
                }
            }
        }
    }
    return query


def get_by_wildcard(index, attr, value, return_attributes=None):
    result = es.search(index=index, body=build_get_by_wildcard_query(attr, value))['hits']['hits']
    if len(result) == 0:
        return None
    records = [result[i]['_source'] for i in range(len(result))]
    data = []
    if return_attributes:
        for record in records:
            ret_attr = {}
            for attr in return_attributes:
                ret_attr[attr] = record[attr]
            data.append(ret_attr)
    return data


def build_get_not_matching_query(attr, value):
    return {
        "size": 100,
        "query": {
            "bool": {
                "must_not": {
                    "match": {attr: value}
                }
            }
        }
    }


def get_not_matching(index, attr, value, return_attributes=None):
    result = es.search(index=index, body=build_get_not_matching_query(attr, value))['hits']['hits']
    if len(result) == 0:
        return None
    records = [result[i]['_source'] for i in range(len(result))]
    data = []
    if return_attributes:
        for record in records:
            ret_attr = {}
            for attr in return_attributes:
                ret_attr[attr] = record[attr]
            data.append(ret_attr)
    return data
