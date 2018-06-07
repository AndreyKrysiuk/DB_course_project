from mongoengine import *


class ClusterElementModel(Document):
    title = StringField(min_length=3, required=True, unique=True)
    cluster = IntField(required=True)


def add_cluster(title, cluster):
    clusterEl = ClusterElementModel()

    exist = ClusterElementModel.objects(title=title)

    if exist:
        print("THIS CLUSTER ELEMENT ALREADY EXIST")
        return

    if title is None or cluster is None:
        return

    clusterEl.title = title
    clusterEl.cluster = cluster

    clusterEl.save()


def get_all_cluster_elements():
    return ClusterElementModel.objects()


def get_ordered_elements():
    return ClusterElementModel.objects.order_by('cluster')


def get_elements_by_cluster(cluster):
    return ClusterElementModel.objects(cluster=cluster)