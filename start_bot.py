from program import main
import polib
import pathlib


def prepare():
    lst = sorted(pathlib.Path.cwd().glob("**/*.po"))
    for pth in lst:
        if pth.suffix == '.po':
            po = polib.pofile(str(pth))
            po.save_as_mofile(str(pth).replace(".po", ".mo"))

if __name__ == '__main__':
    prepare()
    main()
