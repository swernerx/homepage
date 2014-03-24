@task
def build(regenerate=False):
	"""Generate build version"""

	profile = Profile(session)
	profile.registerPart("swerner", styleName="swerner.Main")
	profile.setHashAssets(True)
	profile.setCopyAssets(True)

	konstrukteur.build(profile, regenerate)

	Build.run(profile)


@task
def sync():
  Console.info("Syncing build to public server...")
  executeCommand("rsync --recursive --verbose --links --perms --times --compress --delete --human-readable build/asset build/css build/en build/de homepage:~/html/", wrapOutput=False)
