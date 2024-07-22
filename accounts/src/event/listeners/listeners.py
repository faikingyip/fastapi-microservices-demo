import decimal
import json

from src.common.ctx.rmq_listener_context import RMQListenerContext
from src.constants.transaction_statuses import TransactionStatuses
from src.event.publishers.transaction_created_publisher import AccountUpdatedPublisher


def create_user_created_message_received_handler(
    rmq_listener_ctx,
    ops_account,
    loop,
):
    def on_user_created_message_received_handler(
        channel,
        method,
        properties,
        body,
    ):

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


def create_tran_created_msg_received_hndlr(
    rmq_listener_ctx: RMQListenerContext,
    ops_account,
    loop,
):
    def on_transaction_created_message_received_handler(
        channel, method, properties, body
    ):

        print(f"TRANS LISTENER: received new message: {body}")

        async def call_update_account():
            req = json.loads(body)
            print(req)
            async with rmq_listener_ctx.db_man.session_local() as db:
                try:
                    account = await ops_account.update_account(
                        db,
                        user_id=req["user_id"],
                        request={
                            "amount": decimal.Decimal(req["amount"]),
                            "version": req["version"],
                        },
                    )
                finally:
                    await db.close()

            with rmq_listener_ctx.rmq_pub_client as client:
                AccountUpdatedPublisher(client).publish(
                    json.dumps(
                        {
                            "user_id": str(account.user_id),
                            "balance": str(account.balance),
                            "version": account.version,
                            "transaction_id": str(req["transaction_id"]),
                            "status": TransactionStatuses.COMPLETED.value,
                        }
                    )
                )

            print("PUBLISHED IT!!!")

        loop.run_until_complete(call_update_account())

        channel.basic_ack(delivery_tag=method.delivery_tag)

    return on_transaction_created_message_received_handler
