import logging
# from typing import Dict, Str  # noqa

logger = logging.getLogger(__name__)

# Plain example
class CertLogicService(object):
    def __init__(self, request) -> None:
        self.request = request

    def issue_cert(self) -> None:
        # book = Book.objects.get(id=id)
        # author = AuthorInterface.get_author(id=book.author_id)
        logger.info("??? issue_cert")
        print("???? issue cert rpint")

        return "done"
