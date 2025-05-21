from app.db.base import DatabaseBackend
from app.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
from supabase import create_client, Client

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

class SupabaseDatabase(DatabaseBackend):
    def add_subscription(self, subscription):
        data = {
            "endpoint": subscription.get("endpoint"),
            "keys": subscription.get("keys"),
            "expiration_time": subscription.get("expiration_time"),
            "metadata": subscription.get("metadata"),
        }
        result = supabase.table("subscriptions").upsert(
            data,
            on_conflict="endpoint"
        ).execute()
        return result.data

    def remove_subscription(self, endpoint):
        result = supabase.table("subscriptions").delete().eq("endpoint", endpoint).execute()
        return result.data

    def get_subscriptions(self, metadata_filter=None):
        query = supabase.table("subscriptions").select("*")
        if metadata_filter:
            for key, value in metadata_filter.items():
                query = query.contains("metadata", {key: value})
        result = query.execute()
        return result.data 