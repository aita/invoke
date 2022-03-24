from invoke import task


@task
def install_packages(c):
    c.run("sudo pacman -Syu --noconfirm")
    c.run("sudo pacman -S --needed --noconfirm - < pkglist.txt")

    c.run("yay -Sy --needed --noconfirm --nocleanmenu --nodiffmenu - < pkglist-aur.txt")


@task
def setup_dotfiles(c):
    if c.run("test -L $HOME/.pam_environment", warn=True).ok:
        c.run("rm $HOME/.pam_environment")
    elif c.run("test -f $HOME/.pam_environment", warn=True).ok:
        c.run("mv $HOME/.pam_environment $HOME/.pam_environment.bak")
    c.run("cp $PWD/dotfiles/.pam_environment $HOME/.pam_environment")

    c.run("rm -rf ~/.config/fish")
    c.run("ln -s $PWD/dotfiles/fish ~/.config/fish")


@task
def setup_git(c):
    c.run('git config --global user.name "Ryo Aita"')
    c.run('git config --global user.email "792803+aita@users.noreply.github.com"')


@task
def setup_python(c):
    c.run("python -m pip install --upgrade pip")
    c.run("python -m pip install -r requirements.txt")


@task(
    setup_dotfiles,
    setup_git,
    setup_python,
)
def setup(c):
    pass


@task(
    install_packages,
    setup,
)
def all(c):
    pass
