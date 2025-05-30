from app.db.base import DatabaseBackend
from app.dependencies import get_supabase_client

class SupabaseDatabase(DatabaseBackend):
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def add_subscription(self, subscription):
        data = {
            "endpoint": subscription.get("endpoint"),
            "keys": subscription.get("keys"),
            "expiration_time": subscription.get("expiration_time"),
            "metadata": subscription.get("metadata"),
        }
        result = self.supabase.table("subscriptions").upsert(
            data,
            on_conflict="endpoint"
        ).execute()
        return result.data

    def remove_subscription(self, endpoint):
        result = self.supabase.table("subscriptions").delete().eq("endpoint", endpoint).execute()
        return result.data

    def get_subscriptions(self, metadata_filter=None):
        query = self.supabase.table("subscriptions").select("*")
        if metadata_filter:
            for key, value in metadata_filter.items():
                query = query.contains("metadata", {key: value})
        result = query.execute()
        return result.data 