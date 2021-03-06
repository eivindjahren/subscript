import os
import shutil

import pytest
import rstcheck

from ert_shared.plugins.plugin_manager import ErtPluginManager

import subscript.hook_implementations.jobs

EXPECTED_JOBS = {
    "CSV2OFMVOL": "subscript/config_jobs/CSV2OFMVOL",
    "ECLCOMPRESS": "subscript/config_jobs/ECLCOMPRESS",
    "ECLDIFF2ROFF": "subscript/config_jobs/ECLDIFF2ROFF",
    "ECLGRID2ROFF": "subscript/config_jobs/ECLGRID2ROFF",
    "ECLINIT2ROFF": "subscript/config_jobs/ECLINIT2ROFF",
    "ECLRST2ROFF": "subscript/config_jobs/ECLRST2ROFF",
    "INTERP_RELPERM": "subscript/config_jobs/INTERP_RELPERM",
    "MERGE_RFT_ERTOBS": "subscript/config_jobs/MERGE_RFT_ERTOBS",
    "OFMVOL2CSV": "subscript/config_jobs/OFMVOL2CSV",
    "PRTVOL2CSV": "subscript/config_jobs/PRTVOL2CSV",
    "SUNSCH": "subscript/config_jobs/SUNSCH",
}

# Avoid category inflation. Add to this list when it makes sense:
ACCEPTED_JOB_CATEGORIES = ["modeling", "utility"]


def test_hook_implementations():
    """Test that we have the correct set of jobs installed,
    nothing more, nothing less"""
    plugin_m = ErtPluginManager(plugins=[subscript.hook_implementations.jobs])

    installable_jobs = plugin_m.get_installable_jobs()
    for wf_name, wf_location in EXPECTED_JOBS.items():
        assert wf_name in installable_jobs
        assert installable_jobs[wf_name].endswith(wf_location)
        assert os.path.isfile(installable_jobs[wf_name])

    assert set(installable_jobs.keys()) == set(EXPECTED_JOBS.keys())

    expected_workflow_jobs = {}
    installable_workflow_jobs = plugin_m.get_installable_workflow_jobs()
    for wf_name, wf_location in expected_workflow_jobs.items():
        assert wf_name in installable_workflow_jobs
        assert installable_workflow_jobs[wf_name].endswith(wf_location)

    assert set(installable_workflow_jobs.keys()) == set(expected_workflow_jobs.keys())


def test_job_config_syntax():
    """Check for syntax errors made in job configuration files"""
    src_path = os.path.join(os.path.dirname(__file__), "../src")
    for _, job_config in EXPECTED_JOBS.items():
        # Check (loosely) that double-dashes are enclosed in quotes:
        with open(os.path.join(src_path, job_config)) as f_handle:
            for line in f_handle.readlines():
                if not line.strip().startswith("--") and "--" in line:
                    assert '"--' in line and " --" not in line


@pytest.mark.integration
def test_executables():
    """Test executables listed in job configurations exist in $PATH"""
    src_path = os.path.join(os.path.dirname(__file__), "../src")
    for _, job_config in EXPECTED_JOBS.items():
        with open(os.path.join(src_path, job_config)) as f_handle:
            executable = f_handle.readlines()[0].split()[1]
            assert shutil.which(executable)


def test_hook_implementations_job_docs():
    """For each installed job, we require the associated
    description string to be nonempty, and valid RST markup"""

    plugin_m = ErtPluginManager(plugins=[subscript.hook_implementations.jobs])

    installable_jobs = plugin_m.get_installable_jobs()

    docs = plugin_m.get_documentation_for_jobs()

    assert set(docs.keys()) == set(installable_jobs.keys())

    for job_name in installable_jobs.keys():
        desc = docs[job_name]["description"]
        assert desc != ""
        assert not list(rstcheck.check(desc))
        category = docs[job_name]["category"]
        assert category != "other"
        assert category.split(".")[0] in ACCEPTED_JOB_CATEGORIES
