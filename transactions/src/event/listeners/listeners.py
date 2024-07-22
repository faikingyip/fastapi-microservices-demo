import decimal
import json

from src.common.ctx.rmq_listener_context import RMQListenerContext


def create_acc_updated_msg_received_hndlr(
    rmq_listener_ctx: RMQListenerContext,
    ops_transaction,
    loop,
):
    def on_account_updated_msg_received_handler(
        channel,
        method,
        properties,
        body,
    ):

        print(f"ACCOUNT UPDATED LISTENER: received new message: {body}")

        async def call_update_account():
            req = json.loads(body)

            # "user_id": str(account.user_id),
            # "balance": str(account.balance),
            # "version": account.version,
            # "transaction_id": str(req["transaction_id"]),
            # "status": TransactionStatuses.COMPLETED.value,

            async with rmq_listener_ctx.db_man.session_local() as db:
                try:
                    tran = await ops_transaction.update_transaction(
                        db,
                        transaction_id=req["transaction_id"],
                        request={
                            "status": req["status"],
                        },
                    )
                finally:
                    await db.close()

            print("RECEIVED IT!!!")

        loop.run_until_complete(call_update_account())

        channel.basic_ack(delivery_tag=method.delivery_tag)

    return on_account_updated_msg_received_handler
