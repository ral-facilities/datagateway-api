from argparse import ArgumentParser
from getpass import getpass

from icat.client import Client
from icat.entity import Entity
from icat.exception import ICATObjectExistsError
from icat.query import Query

from datagateway_api.common.config import Config


def get_password(password_file: "str | None") -> str:
    """
    Load the user's password from `password_file` if provided, otherwise prompt for it.

    Args:
        password_file (str): Optional path of file containing the user's password.

    Returns:
        str: The user's password

    """
    if password_file is None:
        return getpass()
    else:
        with open(password_file) as f:
            return f.readline().strip()


def create(
    entity: Entity,
    allow_existing: bool = False,
    fetch_existing: bool = False,
) -> Entity:
    try:
        entity.create()
    except ICATObjectExistsError as e:
        print(f"Ignoring: {e.message}")
        if fetch_existing:
            return entity.client.search(
                query=Query(
                    client=entity.client,
                    entity=entity.BeanName,
                    conditions={"name": [f"='{entity.name}'"]},  # noqa: B907
                ),
            )[0]

    return entity


def setup() -> None:
    parser = ArgumentParser(prog="datagateway_api_setup")
    parser.add_argument(
        "--url",
        type=str,
        default="https://localhost:8181",
        help="The url address of the ICAT server.",
    )
    parser.add_argument(
        "-a",
        "--authenticator",
        type=str,
        default="ldap",
        help="The authentication mechanism to use for ICAT login.",
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        required=True,
        help="The username used for ICAT login.",
    )
    parser.add_argument(
        "-p",
        "--password-file",
        type=str,
        help=(
            "Location of file containing password for ICAT login. If not "
            "provided, the password will need to be provided by prompt."
        ),
    )
    parser.add_argument(
        "--allow-existing",
        action="store_true",
        help=("Iterates over each Entity and if it already exists, suppresses the ICATObjectAlreadyExists error."),
    )
    args = parser.parse_args()

    client = Client(url=args.url, checkCert=False)
    client.login(
        auth=args.authenticator,
        credentials={
            "username": args.username,
            "password": get_password(args.password_file),
        },
    )

    (grouping,) = client.search(
        query=(
            "SELECT ug.grouping FROM UserGroup ug WHERE ug.user.name = "  # noqa: S608
            f"{Config.config.datagateway_api.use_reader_for_performance.reader_username!r}"
        ),
    )

    entities = [
        client.new(obj="Rule", crudFlags="R", what="User", grouping=grouping),
        client.new(obj="Rule", crudFlags="R", what="InvestigationUser", grouping=grouping),
        client.new(obj="Rule", crudFlags="R", what="InstrumentScientist", grouping=grouping),
        client.new(obj="Rule", crudFlags="R", what="Instrument", grouping=grouping),
        client.new(obj="Rule", crudFlags="R", what="InvestigationInstrument", grouping=grouping),
        client.new(obj="Rule", crudFlags="R", what="Investigation", grouping=grouping),
        # client.new(obj="Rule", crudFlags="R", what="Dataset", grouping=grouping),  # Should already exist
        # client.new(obj="Rule", crudFlags="R", what="Datafile", grouping=grouping),  # Should already exist
        client.new(obj="Rule", crudFlags="R", what="DataPublication", grouping=grouping),
        client.new(obj="Rule", crudFlags="R", what="DataCollection", grouping=grouping),
        client.new(obj="Rule", crudFlags="R", what="DataCollectionDataset", grouping=grouping),
    ]

    if args.allow_existing:
        for entity in entities:
            create(entity=entity, allow_existing=args.allow_existing)
    else:
        client.createMany(entities)


if __name__ == "__main__":
    setup()
