import decimal
import json


def create_user_created_message_received_handler(rmq_listener_ctx, ops_account, loop):
    def on_user_created_message_received_handler(channel, method, properties, body):

        print(f"USER LISTENER: received new message: {body}")

        async def call_create_account():
            async with rmq_listener_ctx.db_man.session_local() as db:
                try:
                    return await ops_account.create_account(
                        db,
                        user_id=json.loads(body)["user_id"],
                    )
                finally:
                    await db.close()

        loop.run_until_complete(call_create_account())

        channel.basic_ack(delivery_tag=method.delivery_tag)

    return on_user_created_message_received_handler


def create_transaction_created_message_received_handler(
    rmq_listener_ctx, ops_account, loop
):
    def on_transaction_created_message_received_handler(
        channel, method, properties, body
    ):

        print(f"TRANS LISTENER: received new message: {body}")

        async def call_update_account():
            async with rmq_listener_ctx.db_man.session_local() as db:
                try:
                    req = json.loads(body)
                    return await ops_account.update_account(
                        db,
                        user_id=req["user_id"],
                        request={
                            "amount": decimal.Decimal(req["amount"]),
                            "version": req["version"],
                        },
                    )
                finally:
                    await db.close()

        loop.run_until_complete(call_update_account())

        channel.basic_ack(delivery_tag=method.delivery_tag)

    return on_transaction_created_message_received_handler
