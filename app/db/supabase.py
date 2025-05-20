from app.db.base import DatabaseBackend
import os
from supabase import create_client, Client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

class SupabaseDatabase(DatabaseBackend):
    def add_subscription(self, subscription):
        data = {
            "endpoint": subscription.get("endpoint"),
            "keys": subscription.get("keys"),
            "expiration_time": subscription.get("expiration_time"),
            "metadata": subscription.get("metadata"),
        }
        result = supabase.table("subscriptions").insert(data).execute()
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