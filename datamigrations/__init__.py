def run_upgrade_scripts(app, from_version, to_version):
    for script_id in range(from_version, to_version):
        script_name = '%03d' % (script_id + 1)
        run_upgrade_script(app, script_name)

def run_upgrade_script(app, script_name):
    try:
        cur_script = __import__('datamigrations.%s' % script_name)
    except ImportError:
        # return if the script doesn't exist
        return

    print "Running %s.upgrade" % script_name
    script = getattr(cur_script, script_name)
    script.upgrade(app)

def run_downgrade_scripts(app, from_version, to_version):
    for script_id in reversed(range(to_version, from_version)):
        script_name = '%03d' % (script_id + 1)
        run_downgrade_script(app, script_name)

def run_downgrade_script(app, script_name):
    try:
        cur_script = __import__('datamigrations.%s' % script_name)
    except ImportError:
        # return if the script doesn't exist
        return

    print "Running %s.downgrade" % script_name
    script = getattr(cur_script, script_name)
    script.downgrade(app)

