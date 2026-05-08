from notices.models.notice import Notice


def create_notice(session, data: Notice):

    category = Notice(
        **data.model_dump(),
    )

    session.add(category)
    session.commit()
    session.refresh(category)

    return category
    