import operator
import shutil
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from mealie.core.config import app_dirs
from mealie.db.db_setup import generate_session
from mealie.routes.deps import get_current_user
from mealie.schema.migration import MigrationFile, Migrations
from mealie.schema.snackbar import SnackResponse
from mealie.services.migrations import migration
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/api/migrations", tags=["Migration"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=List[Migrations])
def get_all_migration_options():
    """ Returns a list of avaiable directories that can be imported into Mealie """
    response_data = []
    migration_dirs = [
        app_dirs.MIGRATION_DIR.joinpath("nextcloud"),
        app_dirs.MIGRATION_DIR.joinpath("chowdown"),
    ]
    for directory in migration_dirs:
        migration = Migrations(type=directory.stem)
        for zip in directory.iterdir():
            if zip.suffix == ".zip":
                migration_zip = MigrationFile(name=zip.name, date=zip.stat().st_ctime)
                migration.files.append(migration_zip)
        response_data.append(migration)

        migration.files.sort(key=operator.attrgetter("date"), reverse=True)

    return response_data


@router.post("/{import_type}/{file_name}/import")
def import_migration(import_type: migration.Migration, file_name: str, session: Session = Depends(generate_session)):
    """ Imports all the recipes in a given directory """
    file_path = app_dirs.MIGRATION_DIR.joinpath(import_type.value, file_name)
    return migration.migrate(import_type, file_path, session)


@router.delete("/{import_type}/{file_name}/delete")
def delete_migration_data(import_type: migration.Migration, file_name: str):
    """ Removes migration data from the file system """

    remove_path = app_dirs.MIGRATION_DIR.joinpath(import_type.value, file_name)

    if remove_path.is_file():
        remove_path.unlink()
    elif remove_path.is_dir():
        shutil.rmtree(remove_path)
    else:
        SnackResponse.error("File/Folder not found.")

    return SnackResponse.error(f"Migration Data Remove: {remove_path.absolute()}")


@router.post("/{import_type}/upload")
def upload_nextcloud_zipfile(import_type: migration.Migration, archive: UploadFile = File(...)):
    """ Upload a .zip File to later be imported into Mealie """
    dir = app_dirs.MIGRATION_DIR.joinpath(import_type.value)
    dir.mkdir(parents=True, exist_ok=True)
    dest = dir.joinpath(archive.filename)

    with dest.open("wb") as buffer:
        shutil.copyfileobj(archive.file, buffer)

    if dest.is_file:
        return SnackResponse.success("Migration data uploaded")
    else:
        return SnackResponse.error("Failure uploading file")
