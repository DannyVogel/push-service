from app.db.supabase import SupabaseDatabase

db = SupabaseDatabase()

def add_subscription(subscription):
    return db.add_subscription(subscription)

def remove_subscription(endpoint):
    return db.remove_subscription(endpoint)

def get_subscriptions(space_id=None):
    return db.get_subscriptions(space_id) 