from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict, List, Type

from auth.domain import events

from . import services

if TYPE_CHECKING:
    from . import unit_of_work


def handle(
    event: events.Event,
    uow: unit_of_work.AbstractUnitOfWork,
):
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            results.append(handler(event, uow=uow))
            queue.extend(uow.collect_new_events())
    return results


HANDLERS = {
    events.UserSignupRequested: [services.signup],
    events.UserSigninRequested: [services.signin],
    # events.UserCreated: [services.get_by_email],
}  # type: Dict[Type[events.Event], List[Callable]]
