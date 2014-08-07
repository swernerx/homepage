profile = Profile(session)
profile.registerPart("swerner", styleName="swerner.Main")
profile.setHashAssets(True)
profile.setCopyAssets(True)
profile.setDestinationPath("build")


@task
def build():
    """Generate build version"""
    Build.run(profile)


@task
def content():
    """Generate content files"""
    konstrukteur.build(profile)


@task
def clean():
    core.clean()


@task
def distclean():
    core.distclean()


@task
def sync():
    Console.info("Syncing build to public server...")
    executeCommand("rsync --recursive --verbose --links --perms --times --compress --delete --human-readable build/asset build/css build/en build/de homepage:~/html/", wrapOutput=False)
