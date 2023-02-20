import csv, dataclasses, datetime, io, re
from typing import ClassVar, Optional

BANK_POSB = 0
DATE_FORMAT_STRPTIME_POSB = "%d %b %Y"
DATE_FORMAT_STRPTIME_OCBC = "%d/%m/%Y"
HEADER_COMMENTS_RE_POSB = "^({})".format("|".join([
    "Account Details For:,", "Statement as at:,", "Currency:",
    "Available Balance:,", "Ledger Balance:,", "Transaction Date,"]))
HEADER_COMMENTS_RE_OCBC = "^({})".format("|".join([
    "Account details for:,", "Available Balance,",
    "Ledger Balance,", "Transaction History", "Transaction date,"]))


@dataclasses.dataclass
class Transaction:
    # Assuming a base account in specified during import, these are the
    # mandatory GnuCash CSV import columns. N.B. order matters in cls.fields
    fields: ClassVar[list[str]] = ["date", "description", "deposit", "withdrawal"]
    date: datetime.date
    description: str
    deposit: Optional[float]
    withdrawal: Optional[float]

    def __iter__(self):
        r"""Implement as iterable, so it works with dict, then csv.DictWriter"""
        yield from list(map(lambda x: (x, getattr(self, x)), self.fields))


def parse_posb(rows: list[str]) -> list[Transaction]:
    r"""Parse a POSB transaction CSV, as if from a readlines."""
    rm_empties = filter(lambda x: x.strip() != "", rows)
    rm_header_comments = filter(
        lambda x: not re.search(HEADER_COMMENTS_RE_POSB, x), rm_empties)
    transactions = map(parse_row_posb, rm_header_comments)
    return list(transactions)


def parse_ocbc(rows: list[str]) -> list[Transaction]:
    r"""Parse an OCBC transaction CSV, as if from a readlines."""
    rm_empties = filter(lambda x: x.strip() != "", rows)
    rm_header_comments = filter(
        lambda x: not re.search(HEADER_COMMENTS_RE_OCBC, x), rm_empties)
    transactions = parse_rows_ocbc(rm_header_comments)
    return list(transactions)


def parse_row_posb(row: str) -> Transaction:
    r"""Parse a single non-header row from a POSB transaction CSV.

    A POSB CSV record has 10 fields. The CSV header describes only the first
    nine fields: Transaction Date, Value Date, Statement Code, Reference,
    Debit Amount, Credit Amount, Client Reference, Additional Reference,
    Misc Reference.

    Numeric values seem to never be comma-delimited."""

    splitted = row.strip().split(",")
    # While most rows have 10 values, I have seen some rare rows with an empty
    # 11th column.
    if len(splitted) == 11: splitted = splitted[0:10]

    date, _, code, _, depo, withd, ref_clien, ref_add, ref_misc, _ = splitted
    date = datetime.datetime.strptime(date, DATE_FORMAT_STRPTIME_POSB).date()
    description = "Interest" if code == "ATINT" else "; ".join(
        filter(lambda x: x != "", [ref_clien.strip(), ref_add.strip(), ref_misc.strip()]))
    # Some descriptions have more than one consecutive space, possible for
    # padding? Replace all occurrences with just one space.
    description_collapse = re.sub("\s+", " ", description)
    deposit = float(depo) if depo.strip() != "" else None
    withdraw = float(withd) if withd.strip() != "" else None
    return Transaction(
        date=date, description=description_collapse,
        deposit=deposit, withdrawal=withdraw)


def parse_rows_ocbc(rows: list[str]) -> list[str]:
    r"""Merge rows so that each transaction is represented by only one row.

    OCBC CSVs are psychotic: transactions can be split into at least two rows if
    their descriptions exceed some unspecified length. Also, numeric values are
    sometimes comma-delimited."""

    # Use csv.reader to parse quoted numeric values (quoted because they
    # contain commas.)
    splitted = map(lambda x: next(csv.reader(io.StringIO(x))), rows)
    parsed = []  # parsed is a list of dictionaries
    for row in splitted:
        if row[0] != "":
            parsed.append({
                "date": datetime.datetime.strptime(row[0], DATE_FORMAT_STRPTIME_OCBC).date(),
                "description": row[2],
                "deposit": float(row[4].replace(",", "")) if row[4] != "" else None,
                "withdrawal": float(row[3].replace(",", "")) if row[3] != "" else None})
        else:
            parsed[-1]["description"] += row[2]
    return list(map(lambda xs: Transaction(**xs), parsed))
