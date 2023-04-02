def add_password(pdfs):
    password = getpass.getpass()
    assert password == getpass.getpass(prompt="Confirm: ")
    for pdf in pdfs:
        # Without -dNOPAUSE, user must hit <RET> each page.
        # Without -DBATCH, gs remains in REPL mode after job done
        ps_gs = subprocess.Popen([
                "gs", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
                "-dQUIET", "-sOutputFile=-",
                f"-sOwnerPassword={password}", f"-sUserPassword={password}", pdf],
            stdout=subprocess.PIPE)
        ps_sponge = subprocess.Popen(["sponge", pdf], stdin=ps_gs.stdout)
        ps_sponge.wait()
