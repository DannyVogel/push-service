class DatabaseBackend:
    def add_subscription(self, subscription):
        raise NotImplementedError

    def remove_subscription(self, endpoint):
        raise NotImplementedError

    def get_subscriptions(self, space_id=None):
        raise NotImplementedError 