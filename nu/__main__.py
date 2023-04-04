import argparse, csv, sys
import nu

def main():
    parser = argparse.ArgumentParser(description="Ning's utilities")
    parser.set_defaults(func=lambda x: x)
    subparsers = parser.add_subparsers()

    parser_gnucash = subparsers.add_parser(
        "gnucash", help="Tidy a bank's CSV file for import into GnuCash")
    parser_gnucash.add_argument("file", type=str, help='"-" to read from stdin')
    parser_gnucash.add_argument(
        "--bank", choices=["auto", "posb", "ocbc"], default="auto")
    parser_gnucash.set_defaults(func=gnucash_do)

    parser_tbot = subparsers.add_parser(
        "tbot", help="Telegram bot actions")
    parser_tbot.add_argument(
        "--bot-token", "-b", type=str, default=None, required=False,
        help="Bot token to use. If not given, infer from $XDG_CACHE_HOME/nu/")
    parser_tbot.add_argument(
        "--chat-id", "-c", type=int, default=None, required=False,
        help="Chat ID to target. If not given, infer from $XDG_CACHE_HOME/nu/")
    parser_tbot.add_argument(
        "--save", "-s", action="store_true",
        help="If current bot token and/or chat ID should be cached for next time")
    parser_tbot.add_argument("message", type=str)
    parser_tbot.set_defaults(func=tbot_do)

    parser_pdfpw = subparsers.add_parser(
        "pdfpw", help="Password-protect one or more PDF files")
    parser_pdfpw.add_argument("pdfs", nargs="+")
    parser_pdfpw.set_defaults(func=pdfpw_do)

    args = parser.parse_args()
    args.func(args)


def gnucash_do(args):
    # Get input from file or stdin
    if args.file == "-":
        lines = sys.stdin.readlines()
    else:
        with open(args.file if args.file != "-" else sys.stdin) as csvfile:
            lines = csvfile.readlines()

    # Choose parser
    if args.bank == "auto":
        parse_bank_fn = nu.gnucash.parse_posb if lines[0] == "\n" else nu.gnucash.parse_ocbc
    elif args.bank == "ocbc":
        parse_bank_fn = nu.gnucash.parse_ocbc
    elif args.bank == "posb":
        parse_bank_fn = nu.gnucash.parse_posb
    else:
        raise ValueError(f"Unrecognised value for option bank: {args.bank}")

    # A list of nu.gnucash.Transaction objects
    transactions = parse_bank_fn(lines)
    # A list of dictionaries; keys are field names, values are field values
    transactions_dict = list(map(dict, transactions))
    for trans in transactions_dict: trans["date"] = trans["date"].isoformat()
    writer = csv.DictWriter(
        sys.stdout, fieldnames=nu.gnucash.Transaction.fields)
    writer.writeheader()
    writer.writerows(transactions_dict)


def tbot_do(args):
    token = args.bot_token if args.bot_token is not None else nu.tbot.get_last_token()
    chat_id =  args.chat_id if args.chat_id is not None else nu.tbot.get_last_chat_id()
    nu.tbot.send_message(token, chat_id, message, args.save)


def pdfpw_do(args):
    nu.pdfpw.add_password(args.pdfs)


if __name__ == "__main__":
    main()
