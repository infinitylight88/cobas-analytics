from api.database.session import SessionLocal

from api.services.base_service import BaseService

from api.database.models import ArchiveFile



class ArchiveService:

    @staticmethod
    def all():

        db = SessionLocal()

        try:

            return db.query(
                ArchiveFile
            ).order_by(
                ArchiveFile.archive_start.desc()
            ).all()

        finally:

            db.close()



class ArchiveService(BaseService):


    def get_all(self):

        return (
            self.db
            .query(ArchiveFile)
            .order_by(
                ArchiveFile.imported_at.desc()
            )
            .all()
        )


    def get_by_id(self, archive_id):

        return (
            self.db
            .query(ArchiveFile)
            .filter(
                ArchiveFile.archive_id == archive_id
            )
            .first()
        )