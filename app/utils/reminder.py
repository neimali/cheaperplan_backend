import asyncio        
import httpx
from app.supabase_client import supabase
from .push_utils import receipt_map, cache_lock, PUSH_URL, RECEIPT_URL


def get_all_better_plans():
    res = supabase.rpc("get_all_better_plans").execute()
    print(res)
    
    return res.data

def get_exponentPushTokens(records):
    return list({r["exponent_push_token"] for r in records if r.get("exponent_push_token")})

def delete_expo_token(token: str):
    res = supabase.table("user_profile").delete().eq("exponent_push_token", token).execute()
    
    if res.data is not None:           
        print("deleted", token)
    else:
        print("failed to delete", token, res)



async def send_push(tokens: list[str], title="Cheaper Plan available!", body="GoGoGo"):
    """
    批量推送同一条消息，返回有效 token 列表 & ticket IDs 列表
    """
    msg = {
        "to": tokens,
        "title": title,
        "body": body,
        "sound": "default",
        "data": {
            "route": "/screens/BetterPlanScreen"
        }
    }

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(PUSH_URL, json=msg)
    r.raise_for_status()

    tickets = r.json()["data"]
    receipt_ids = []

    async with cache_lock:
        for token, ticket in zip(tokens, tickets):
            if ticket["status"] == "ok":
                rid = ticket["id"]
                receipt_map[rid] = token
                receipt_ids.append(rid)
                print("valid token, push request sent")
            elif ticket.get("details", {}).get("error") == "DeviceNotRegistered":
                print("invalid token, deleted token")
                delete_expo_token(token)
    return receipt_ids


async def fetch_receipts(receipt_ids: list[str]):
    """
    查询异步收据，再次剔除失效 token
    """
    if not receipt_ids:
        return

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(RECEIPT_URL, json={"ids": receipt_ids})
    r.raise_for_status()

    async with cache_lock:
        for rid, info in r.json()["data"].items():
            token = receipt_map.pop(rid, None)
            if info["status"] == "ok" or not token:
                print("push succeed", token)
                continue
            print("Receipt error:", info.get("message"))
            if info.get("details", {}).get("error") == "DeviceNotRegistered":
                print("push failed on second phrase")
                delete_expo_token(token)



async def push_same_message():
    records = get_all_better_plans()
    if not records:
        print("no records found")
        return

    # Group records by user to send personalized messages
    for record in records:
        token = record.get("exponent_push_token")
        if not token:
            continue
        
        new_plans_count = record["new_plans_count"]
        max_savings = record["max_savings"]
        
        # Create personalized message body
        body = f"We've found {new_plans_count} new plans for you! The cheapest one could save you ${max_savings}/month — that's about ${max_savings * 12} a year."
        
        receipt_ids = await send_push([token], body=body)
        await asyncio.sleep(1)  # Small delay between individual pushes
        await fetch_receipts(receipt_ids)

