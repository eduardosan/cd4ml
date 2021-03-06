# -*- coding: utf-8 -*-
import contextlib
import sys
import os.path
import pkg_resources
import semantic_version

from fabric.api import settings
from fabric.api import local, puts, abort, hide, lcd, prefix
from fabric import colors as c
from fabric.contrib.console import confirm

PROJECT_NAMESPACE = 'tw'
VIRTUAL_ENV = '.env'


def _invirt():
    """Make sure we have bootstrapped."""
    with settings(hide('running', 'stdout', 'stderr')):
        current_py = local('which python', capture=True)
        puts(current_py)
        if not confirm("Your python: %s\nIs this the correct virtualenv?" % current_py):
            puts(c.red('Not in virtualenv! Please activate the virtualenv'))
            sys.exit(1)


def _package_name():
    """
    Get package name

    :return: package name
    """
    return os.path.basename(os.path.dirname(os.path.realpath(__file__)))


def _image_name(version=None):
    """
    retorna o nome da imagem do Docker
    :param version:
    :return:
    """
    package_name = _package_name()
    image_name = '%s/%s' % (PROJECT_NAMESPACE, package_name)
    if version is not None:
        image_name = "%s:%s" % (image_name, version)

    return image_name


@contextlib.contextmanager
def _freshvirt(version):
    """
    Create a new container to run tests on a fresh virtualenv

    :param version:
    :return:
    """
    image_name = _image_name(version)
    puts(c.blue("Creating and building docker instance  for testing"))
    with settings(hide('stdout', 'stderr', 'warnings', 'running'),
                  warn_only=True):
        result = local(f"python -m venv {VIRTUAL_ENV}")
        if result.return_code >= 0:
            abort(c.red("Failed to create clean virt without marketing_platform."))

        yield


def buildtest(version=None):
    """
    Create a new container to run tests on a fresh virtualenv

    :param version: Container version
    :return:
    """
    if version is None:
        version = compute_version(increase=False)

    image_name = _image_name(version)
    puts(c.blue("Creating and building docker instance for testing"))
    local("docker build --target testing . -t %s" % image_name)
    result = local("docker run --rm -it -t %s py.test" % image_name)
    if result.return_code > 0:
        abort(c.red("Error build and testing version"))

    puts(c.magenta("Built and installed successfully"))


def post_release_install_verification(version):
    """Try installing from pypi and importing in a clean virt.
    Does `pip` and `easy_install`.
    """
    puts(c.blue("Running post-release install verification..."))
    buildtest(version)
    puts(c.magenta("Release verification successful!"))


def clean(deep=False, env='docker'):
    """Kill the virtual env and all files generated by build and test.

    [:deep=False]

    If deep is True, removes the virtualenv and all.
    """
    package_name = _package_name()
    if confirm('Delete old build files?'):
        puts(c.red("Cleaning up..."))
        with settings(hide('running', 'stdout')):
            local('rm -rf build/')
            local('rm -f coverage.xml')
            local('rm -rf selector.egg-*')
            local('rm -rf *.pyc')
            local('rm -rf __pycache__/')
            local('rm -rf %s/tests/__pycache__/' % package_name)
            local('rm -rf %s/tests/*.pyc' % package_name)
            local('rm -rf %s/tests/*/__pycache__/' % package_name)
            local('rm -rf %s/tests/*/*.pyc' % package_name)
            local('rm -rf htmlcov')
            if os.path.exists('docs'):
                with lcd('docs'):
                    local('make clean')
            if deep:
                _invirt()
                puts(c.red("Removing virtualenv %s/" % VIRTUAL_ENV))
                puts(c.red("You will need to activate virtualenv again."))
                local('rm -rf %s/' % VIRTUAL_ENV)
    else:
        puts(c.red("Not cleaning."))


def _abort_if_not_valid_release_type(release_type):
    """Make sure we have a valid release type."""
    release_type = release_type.lower()
    if release_type not in ("major", "minor", "patch"):
        abort(c.red("Not a valid release type, see `fab -d release`"))
    return release_type


def update_docker_compose(version=None):
    """
    Update docker-compose.yml

    :param version: Vers??o a ser utilizada
    :return:
    """
    if version is None:
        version = compute_version(increase=False)

    puts(c.blue("Updating docker-compose.yml version to %s" % version))
    here = os.path.abspath(os.path.dirname(__file__))
    docker_compose = os.path.join(here, './docker-compose.yml')
    local("sed -i -E \'s/^(.*image:.*:)([0-9\.]*)$/\\1%s/g\' %s" % (version, docker_compose))
    # local(sed(docker_compose, r"^.+image:.+:([0-9\.]+)$", version))
    puts(c.green("File docker-compose.yml updated!"))


def update_sonar_version(version=None):
    """
    Update sonar version

    :param version:  Vers??o a ser utilizada
    :return:
    """
    if version is None:
        version = compute_version(increase=False)

    puts(c.blue("Updating sonar-project.properties version to %s" % version))
    here = os.path.abspath(os.path.dirname(__file__))
    sonar = os.path.join(here, './sonar-project.properties')
    local("sed -i -E \'s/^(sonar\.projectVersion=)([0-9\.]*)$/\\1%s/g\' %s" % (version, sonar))
    puts(c.green("File sonar-project.properties updated!"))


def compute_version(release_type='minor', rc=False, increase=True):
    """Compute a semver compliant version number.
    :release_type[,rc=False]

    :param release_type: Release types:  MAJOR - non-backwards compatible feature(s)
                    MINOR - backwards compatible feature(s) addition
                    PATCH - backwards compatible bug fix(es)
    :param rc: "rc" indicates a Release Candidate.
    :param increase: If set to False, just get current version
    """
    # Make sure it is a valid type of release.
    release_type = _abort_if_not_valid_release_type(release_type)

    # Update tags list
    local("git pull --tags")

    # Find the latest version.
    tags = (t.strip() for t in local('git tag', capture=True).split('\n'))
    versions = [t[1:] for t in tags if t.startswith('v')]
    versions.sort(key=pkg_resources.parse_version)
    final_versions = [v for v in versions if 'rc' not in v]
    latest_final = final_versions and final_versions[-1] or '0.0.0'

    if increase is False:
        return latest_final

    # Load version from semantic versioning
    v = semantic_version.Version(latest_final)

    # Bump the version number.
    new_version = latest_final
    if release_type == 'major':
        new_version = str(v.next_major())
    if release_type == 'minor':
        new_version = str(v.next_minor())
    if release_type == 'patch':
        new_version = str(v.next_patch())

    # Append a release candidate number to the version?
    if rc:
        candidate_number = 0
        while 1:
            candidate_number += 1
            candidate_version = "%src%s" % (new_version, candidate_number)
            if candidate_version not in versions:
                break
        new_version = candidate_version

    puts(c.magenta("Calculated version: %s" % new_version))
    return new_version


def _sync_and_preflight_check(branch, release_type):
    """Sync up repository and check that things are in order for release."""
    # Sync.
    puts(c.blue("Git fetching origin..."))
    local("git fetch origin", capture=True)
    puts(c.blue("Running preflight checks..."))

    # Make release type is valid.
    _abort_if_not_valid_release_type(release_type)

    # Make sure we don't have any outstanding edits hanging around.
    if (local("git diff", capture=True).strip()
            or local("git status -s", capture=True)):
        abort(c.red("It seems you have unstaged local changes."))
    if local("git diff --staged", capture=True).strip():
        abort(c.red("It seems you have changes in the staging area."))

    # Local main and origin/main must be up-to-date with each other.
    if (local("git diff origin/main...main", capture=True).strip()
            or local("git diff main...origin/main", capture=True).strip()):
        puts(c.red("main is out of sync with origin! Pushing..."))
        local("git push origin main")

    # See what changes are in the branch and make sure there is something to
    # release.
    changes = local("git diff origin/%s...%s" % (branch, branch), capture=True)

    if not changes:
        if not confirm("No changes detected. Releasing from main?"):
            abort(c.red("No changes there to release. Hmm."))
            sys.exit(1)
    else:
        puts(c.blue("Changes to release:"))
        puts(c.cyan(changes))

    # Local branch and origin/branch must be up-to-date with each other.
    if (local("git diff origin/%s...%s" % (branch, branch),
              capture=True).strip()
            or local("git diff %s...origin/%s" % (branch, branch),
                     capture=True).strip()):
        puts(c.red("%s is out of sync with origin!." % branch))
        local("git push origin %s" % branch)

    # Merge main
    if branch != 'main':
        local("git checkout main")
        local("git merge %s" % branch)
        local("git checkout %s" % branch)

    # Make sure our branch has all the latest from main.
    changes_from_main = local("git diff %s...main" % branch, capture=True)
    if changes_from_main:
        abort(c.red("%s is out of sync with main and needs to be merged." % branch))

    # Compute the new server compliant version number.
    version = compute_version(release_type)

    # Ask user to verify version and changesets.
    if not confirm("Are the changes and version correct?"):
        abort(c.red("Aborting release"))

    # return version, changes
    return version, changes


def test(env='docker'):
    """
    Execute tests

    Run env=virtualenv to execute on virtualenv
    """
    clean()
    if env == 'docker':
        puts(c.blue("Starting tests on docker..."))
        buildtest()
    else:
        _invirt()
        local("pip install -e '.[testing]'")
        puts(c.blue("Starting tests..."))
        local("py.test")


def release(branch=None, release_type='patch', verify=False):
    """Release a new version.

    :param branch:  Branch to be released
    :param release_type: see fab -d compute_version
    :param verify: Verify instalation in a new virtualenv

    Preflight, runs tests, bumps version number, tags repo and uploads to pypi.
    """
    if branch is None:
        branch = local("git rev-parse --abbrev-ref HEAD", capture=True)
        puts(c.blue("No branch supplied. Falling back to branch %s" % branch))
    # _invirt()
    with settings(hide('stderr', 'stdout', 'running')):
        # Preflight checks.
        version, changes = _sync_and_preflight_check(branch, release_type)
        # version = _sync_and_preflight_check(branch, release_type)
    puts(c.blue("Build, package and publish..."))

    # Commit to the version file.
    local('echo "%s" > VERSION' % version)

    # Update version in files
    # update_docker_compose(version)
    # update_sonar_version(version)

    # Write to changelog
    changelog()

    # Commit the version change and tag the release.
    puts(c.blue("Commit, tag, merge, prune and push."))
    with settings(warn_only=True):
        local('git commit -m "Bumped version to v%s" -a' % version)
    local('git tag -a "v%s" -m "Release version %s"' % (version, version))

    # Merge the branch into main and push them both to origin
    # Conflicts should never occur, due to preflight checks.
    local('git checkout main', capture=True)
    local('git merge %s' % branch, capture=True)
    # if branch != 'main':
    # local('git branch -d %s' % branch)
    # This deletes remote branch.
    # local('git push origin :%s' % branch)
    local('git push --tags origin main')
    puts(c.magenta("Released branch %s as v%s!" % (branch, version)))

    if verify:
        post_release_install_verification(version)

    # Build
    # local("python setup.py register sdist bdist_egg upload")
    # puts(c.green("Uploaded to PyPI!"))

    # Get back to branch
    local('git checkout %s' % branch, capture=True)
    local('git merge main')

    return version


def build(release_type='patch', branch=None):
    """
    Create a build for this release

    :param release_type: check fab -d compute_version
    :param branch:  Branch to be released
    """
    puts(c.blue("Testing..."))

    # Lets check out this branch and test it.
    if branch is None:
        branch = local("git rev-parse --abbrev-ref HEAD", capture=True)
        puts(c.blue("No branch supplied. Falling back to branch %s" % branch))
    local("git checkout %s" % branch, capture=True)
    test()
    puts(c.green("Tests passed!"))

    # First create a release
    version = release(branch, release_type, False)
    puts(c.blue("Building release for version %s and branch %s" % (version, branch)))

    # Create dists directory if it not exists
    local('mkdir -p dists')

    # Create release package
    local('git checkout tags/v%s' % version, capture=True)
    local("python setup.py sdist")
    puts(c.green("Release file created!"))

    # Get back to branch
    local('git checkout %s' % branch, capture=True)

    return


def changelog():
    """Cria changelog do git"""
    puts(c.blue("Writing changelog to CHANGES.txt..."))

    # N??o falha por causa do changelog
    with settings(warn_only=True):
        local("gitchangelog > CHANGES.txt")
    puts(c.blue("Changelog written"))


def doc(env='docker'):
    """
    Generate sphinx documentation

    Run env=virtualenv to execute on virtualenv
    """
    clean()
    if env == 'docker':
        puts(c.blue("Generating documentation on docker..."))
        version = compute_version(increase=False)
        image_name = _image_name(version)
        puts(c.blue("Creating and building docker instance for testing"))
        local("docker build --target docs . -t %s" % image_name)
        result = local("docker run --rm -it -t %s /bin/bash -c  'cd docs && make html'" % image_name)
        if result.return_code > 0:
            abort(c.red("Error generating documentation"))

        puts(c.magenta("Documentation generated successfully"))
    else:
        _invirt()
        local("pip install -e '.[docs]'")
        puts(c.blue("Generating docs..."))
        with lcd('docs'):
            local("make html")
        puts(c.magenta("Documentation generated successfully"))
