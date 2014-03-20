@task
def build(regenerate = False):
	"""Generate build version"""

	profile = Profile(session)
	profile.registerPart("swerner", styleName="swerner.Main")
	profile.setHashAssets(True)
	profile.setCopyAssets(True)

	konstrukteur.build(profile, regenerate)

	Build.run(profile)
